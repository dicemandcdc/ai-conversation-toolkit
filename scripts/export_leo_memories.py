#!/usr/bin/env python3
"""
ACM-47: export_leo_memories.py
Exports Brave Leo AI memories to persistent storage.
Supports --target (mongodb | postgresql | json), --dry-run, --verify, --limit.
"""

import argparse
import logging
import os
import sys
import json
import uuid
from datetime import datetime, timezone
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

# ── Logging Setup ──────────────────────────────────────────────────────────────
LOG_DIR = "/var/log/health_checks"
LOG_FILE = os.path.join(LOG_DIR, "memory_export.log")

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)

# ── Argument Parser ────────────────────────────────────────────────────────────
def parse_args():
    parser = argparse.ArgumentParser(
        description="Export Brave Leo AI memories to persistent storage."
    )
    parser.add_argument(
        "--target",
        choices=["mongodb", "postgresql", "json"],
        default="mongodb",
        help="Storage target (default: mongodb)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate capture without writing to storage",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Confirm successful storage write after export",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Cap memory count per run (optional safety valve)",
    )
    parser.add_argument(
        "--input",
        type=str,
        default=None,
        help="Path to pre-exported JSON file (Option B capture path)",
    )
    return parser.parse_args()

SPRINT_CONTEXT = "Sprint 3"

def normalize_input(raw: dict) -> list:
    """
    Handles multiple possible JSON shapes from brave_leo_export.js.
    Ensures capture_memories() always receives a consistent list.
    """
    # Shape 1: { "memories": [ { "memory_text": "..." } ] }
    if "memories" in raw and isinstance(raw["memories"], list):
        return raw["memories"]

    # Shape 2: [ "memory text 1", "memory text 2" ] — flat list of strings
    if isinstance(raw, list) and all(isinstance(i, str) for i in raw):
        return [{"memory_text": i} for i in raw]

    # Shape 3: [ { "text": "..." } ] — list of dicts with "text" key
    if isinstance(raw, list) and all(isinstance(i, dict) for i in raw):
        return [{"memory_text": i.get("text", i.get("memory_text", ""))} for i in raw]

    log.warning("[NORMALIZER] Unrecognized input shape — returning empty list.")
    return []

def capture_memories(args) -> list[dict]:
    """
    Reads memories from a pre-exported JSON file (Option B capture path).
    File produced by brave_leo_export.js run manually in DevTools.
    """
    input_path = args.input or os.path.expanduser(
        "~/ai-conversations/memories/raw_export.json"
    )

    if not os.path.exists(input_path):
        log.error(f"Input file not found: {input_path}")
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    raw_memories = normalize_input(raw)

    if args.limit:
        raw_memories = raw_memories[: args.limit]
        log.info(f"[LIMIT] Capped at {args.limit} memories.")

    now = datetime.now(timezone.utc).isoformat()
    structured = []

    for item in raw_memories:
        text = item.get("memory_text", "").strip()
        if not text:
            continue

        record = {
            "memory_id": str(uuid.uuid4()),
            "captured_at": now,
            "source": "Brave Leo AI",
            "sprint_context": SPRINT_CONTEXT,
            "memory_text": text,
            "tags": item.get("tags", []),
            "word_count": len(text.split()),
        }
        structured.append(record)
        log.info(f"Captured memory [{record['memory_id'] [:8]}...]: {text[:60]}...")

    log.info(f"Total memories captured: {len(structured)}")
    return structured

# ── Memory Router ───────────────────────────────────────────────────────────
def write_memories(memories: list[dict], args):
    """Routes to the correct storage writer based on --target flag."""
    writers = {
        "mongodb":    write_to_mongodb,
        "postgresql": write_to_postgresql,
        "json":       write_to_json,
    }
    writer = writers[args.target]
    writer(memories, args)

# ── MongoDB Writer ─────────────────────────────────────────────────────────────
def write_to_mongodb(memories: list[dict], args):
    host     = os.environ.get("MONGO_HOST", "192.168.56.101")
    port     = int(os.environ.get("MONGO_PORT", 27017))
    user     = os.environ.get("MONGO_USER")      # from env — no hardcoding
    password = os.environ.get("MONGO_PASSWORD")  # from env — no hardcoding
    db_name  = os.environ.get("MONGO_DB", "ai_conversation_toolkit")
    coll     = os.environ.get("MONGO_COLLECTION", "leo_memories")

    uri = f"mongodb://{user}:{password}@{host}:{port}/{db_name}?authSource={db_name}"

    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        try:
            log.info(f"[MongoDB] Connection attempt {attempt}/{max_attempts}...")
            client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            client.admin.command("ping")  # verify connection
            collection = client[db_name] [coll]
            result = collection.insert_many(memories)
            log.info(f"[MongoDB] Inserted {len(result.inserted_ids)} records.")

            if args.verify:
                count = collection.count_documents(
                    {"memory_id": {"$in": [m["memory_id"] for m in memories]}}
                )
                log.info(f"[VERIFY] Confirmed {count}/{len(memories)} records in MongoDB.")

            client.close()
            return

        except (ConnectionFailure, OperationFailure) as e:
            log.warning(f"[MongoDB] Attempt {attempt} failed: {e}")
            if attempt == max_attempts:
                log.error("[MongoDB] All retry attempts exhausted. Falling back to JSON.")
                write_to_json(memories, args)  # automatic fallback

# ── PostgreSQL Writer ──────────────────────────────────────────────────────────
def write_to_postgresql(memories: list[dict], args):
    try:
        import psycopg2
    except ImportError:
        log.error("[PostgreSQL] psycopg2 not installed. Run: pip3 install psycopg2-binary")
        sys.exit(1)

    host     = os.environ.get("PG_HOST", "localhost")
    port     = os.environ.get("PG_PORT", "5432")
    user     = os.environ.get("PG_USER")
    password = os.environ.get("PG_PASSWORD")
    db_name  = os.environ.get("PG_DB", "ai_conversation_toolkit")

    try:
        conn = psycopg2.connect(
            host=host, port=port, user=user,
            password=password, dbname=db_name
        )
        cur = conn.cursor()

        for memory in memories:
            cur.execute("""
                INSERT INTO leo_memories
                    (memory_id, captured_at, source, sprint_context,
                     memory_text, tags, word_count)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (memory_id) DO NOTHING
            """, (
                memory["memory_id"],
                memory["captured_at"],
                memory["source"],
                memory["sprint_context"],
                memory["memory_text"],
                memory["tags"],
                memory["word_count"],
            ))

        conn.commit()
        log.info(f"[PostgreSQL] Inserted {len(memories)} records.")

        if args.verify:
            cur.execute("SELECT COUNT(*) FROM leo_memories")
            count = cur.fetchone()[0]
            log.info(f"[VERIFY] Total records in PostgreSQL: {count}")

        cur.close()
        conn.close()

    except Exception as e:
        log.error(f"[PostgreSQL] Write failed: {e}")
        log.error("[PostgreSQL] Falling back to JSON.")
        write_to_json(memories, args)

# ── Flat JSON Writer ───────────────────────────────────────────────────────────
def write_to_json(memories: list[dict], args):
    output_dir = os.path.expanduser("~/ai-conversations/memories")
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"leo_memories_{timestamp}.json")

    payload = {
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "source": "Brave Leo AI",
        "memory_count": len(memories),
        "memories": memories,
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    log.info(f"[JSON] Wrote {len(memories)} memories to {output_file}")

    if args.verify:
        with open(output_file, "r", encoding="utf-8") as f:
            verified = json.load(f)
        count = verified.get("memory_count", 0)
        log.info(f"[VERIFY] Confirmed {count} memories in {output_file}")

# ── Entry Point ────────────────────────────────────────────────────────────────
def main():
    args = parse_args()
    log.info("=== ACM-47 export_leo_memories.py START ===")
    log.info(f"Target: {args.target} | Dry-run: {args.dry_run} | Verify: {args.verify}")

    # Stubs — filled in Steps 2 and 3
    memories = capture_memories(args)
    if not args.dry_run:
        write_memories(memories, args)
    else:
        log.info(f"[DRY-RUN] {len(memories)} memories captured. No write performed.")

    log.info("=== ACM-47 export_leo_memories.py END ===")

if __name__ == "__main__":
    main()

