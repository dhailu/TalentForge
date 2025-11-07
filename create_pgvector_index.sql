CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS resume_metadata (
  id SERIAL PRIMARY KEY,
  filename TEXT,
  blob_path TEXT,
  text_content TEXT,
  embedding vector(1536),
  uploaded_at TIMESTAMP DEFAULT NOW()
);

-- Index (run after you have inserted some rows)
CREATE INDEX IF NOT EXISTS idx_resumes_embedding
  ON resume_metadata USING ivfflat (embedding vector_l2_ops) WITH (lists = 100);
