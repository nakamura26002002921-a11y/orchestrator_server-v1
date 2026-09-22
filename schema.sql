# schema.sql
# ============================================================
# Usage:
#   npx wrangler d1 execute server-approval --remote --file=schema.sql
# ============================================================

CREATE TABLE IF NOT EXISTS requests (
    id TEXT PRIMARY KEY,
    status TEXT NOT NULL CHECK (status IN ('承認待ち', '承認済み')),
    purpose TEXT NOT NULL,
    command TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_requests_status ON requests(status);
