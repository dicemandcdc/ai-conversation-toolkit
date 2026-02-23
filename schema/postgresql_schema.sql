-- postgresql_schema.sql
-- Version 1.0 – Initial schema for Brave Leo export
-- This DDL creates the tables that store exported conversations.
-- It aligns with schema/brave_leo_export_schema.json (Draft‑07).

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Table that stores each exported conversation as a JSONB document.
CREATE TABLE conversations (
    id               UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    platform         VARCHAR(50) NOT NULL,                     -- e.g., 'Brave Leo'
    exported_at      TIMESTAMPTZ NOT NULL,                     -- ISO‑8601 timestamp
    source           VARCHAR(50) NOT NULL,                     -- redundant with platform, kept for legacy queries
    message_count    INTEGER NOT NULL CHECK (message_count >= 0),
    messages         JSONB NOT NULL,                           -- array of message objects
    metadata         JSONB,                                     -- optional extra data
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Index to speed up look‑ups by export time and platform
CREATE INDEX idx_conversations_exported_at ON conversations (exported_at DESC);
CREATE INDEX idx_conversations_platform   ON conversations (platform);

-- Optional: a view that expands the JSON messages into a relational form
CREATE VIEW conversation_messages AS
SELECT
    c.id                               AS conversation_id,
    (msg->>'role')::TEXT               AS role,
    (msg->>'id')::INTEGER              AS message_id,
    (msg->>'text')::TEXT               AS text,
    jsonb_array_elements(c.messages)   AS msg
FROM conversations c;
