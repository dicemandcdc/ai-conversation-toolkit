# Schema folder overview

## Purpose
This folder contains data‑model artefacts for the AI Conversation Management Toolkit.  
It stores the JSON schema used to validate exported conversation files and the PostgreSQL DDL script that creates the `conversations` and `messages` tables.

## Files
- **brave_leo_export_schema.json** – Draft‑07 JSON Schema that defines the required structure of a Brave Leo export (fields: `exported_at`, `source`, `message_count`, `messages`).
- **postgresql_schema.sql** – SQL DDL that creates the `conversations` and `messages` tables, indexes, and comments. Includes future‑proof columns `session_id`, `thread_id`, `metadata`, `message_metadata`, `message_order`.

## How to use
1. **Validate a JSON export**  
   ```bash
   ajv validate -s schema/brave_leo_export_schema.json -d path/to/export.json
