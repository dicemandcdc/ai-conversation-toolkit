-- ============================================================
-- AI Conversation Management Toolkit — PostgreSQL DDL
-- ACM-27 | Assignee: Flora Cruz
-- NOTE: session_id, thread_id, metadata, message_metadata,
--       and message_order are intentionally included now to
--       support future conversation reconstruction (ACM-24)
--       and avoid costly schema migrations later.
-- ============================================================

-- TABLE: conversations
-- Stores one record per exported Brave Leo conversation file.
CREATE TABLE IF NOT EXISTS conversations (
    id             SERIAL          PRIMARY KEY,
    source         VARCHAR(50)     NOT NULL,           -- e.g. "Brave Leo"
    exported_at    TIMESTAMPTZ     NOT NULL,           -- from JSON exported_at
    message_count  INTEGER,                            -- from JSON message_count
    created_at     TIMESTAMPTZ     DEFAULT NOW(),
    session_id     UUID,                               -- ACM-24: multi-session reconstruction
    thread_id      VARCHAR(100),                       -- ACM-24: thread continuity
    metadata       JSONB                               -- flexible; no migration needed for new fields
);

-- TABLE: messages
-- Stores individual messages linked to a conversation.
CREATE TABLE IF NOT EXISTS messages (
    id                  SERIAL      PRIMARY KEY,
    conversation_id     INTEGER     NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role                VARCHAR(20) NOT NULL,          -- "user" or "leo"
    message_order       INTEGER     NOT NULL,          -- preserves exact conversation sequence (ACM-24)
    text                TEXT        NOT NULL,          -- message content
    created_at          TIMESTAMPTZ DEFAULT NOW(),
    token_count         INTEGER,                       -- future FinOps AI cost tracking
    message_metadata    JSONB                          -- flexible; no migration needed for new fields
);

-- INDEXES
CREATE INDEX IF NOT EXISTS idx_conversations_source      ON conversations(source);
CREATE INDEX IF NOT EXISTS idx_conversations_exported_at ON conversations(exported_at);
CREATE INDEX IF NOT EXISTS idx_messages_conversation_id  ON messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_messages_role             ON messages(role);
