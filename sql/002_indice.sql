CREATE INDEX IF NOT EXISTS trechos_embedding_idx
ON trechos USING hnsw (embedding vector_cosine_ops)