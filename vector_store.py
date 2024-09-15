import psycopg2
from psycopg2 import sql
from pgvector.psycopg2 import register_vector
import numpy as np
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL, PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD

class PostgresVectorStore:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.conn = psycopg2.connect(
            host=PGHOST,
            port=PGPORT,
            dbname=PGDATABASE,
            user=PGUSER,
            password=PGPASSWORD
        )
        self._create_extension()
        self._create_table()

    def _create_extension(self):
        with self.conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
            self.conn.commit()

    def _create_table(self):
        with self.conn.cursor() as cur:
            register_vector(cur)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id SERIAL PRIMARY KEY,
                    content TEXT,
                    embedding vector(384)
                )
            """)
            cur.execute("CREATE INDEX IF NOT EXISTS embedding_idx ON documents USING ivfflat (embedding vector_cosine_ops)")
            self.conn.commit()

    def add_documents(self, documents):
        embeddings = self.model.encode(documents)
        with self.conn.cursor() as cur:
            for doc, emb in zip(documents, embeddings):
                cur.execute(
                    "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
                    (doc, emb.tolist())
                )
        self.conn.commit()

    def search(self, query, k=3):
        query_embedding = self.model.encode([query])[0]
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT content FROM documents ORDER BY embedding <-> %s::vector LIMIT %s",
                (query_embedding.tolist(), k)
            )
            results = cur.fetchall()
        return [result[0] for result in results]

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()
