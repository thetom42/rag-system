import psycopg2
from psycopg2 import sql
from pgvector.psycopg2 import register_vector
import numpy as np
from sentence_transformers import SentenceTransformer
from rag_system.config import EMBEDDING_MODEL, PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD
import logging

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
            cur.execute('''
                CREATE TABLE IF NOT EXISTS documents (
                    id SERIAL PRIMARY KEY,
                    document_id TEXT,
                    content TEXT,
                    embedding vector(384)
                )
            ''')
            cur.execute("CREATE INDEX IF NOT EXISTS embedding_idx ON documents USING ivfflat (embedding vector_cosine_ops)")
            self.conn.commit()

    def add_documents(self, documents, document_id=None):
        embeddings = self.model.encode([doc.split('\n\n')[-1] for doc in documents])  # Encode only the content part
        with self.conn.cursor() as cur:
            for doc, emb in zip(documents, embeddings):
                cur.execute(
                    "INSERT INTO documents (document_id, content, embedding) VALUES (%s, %s, %s)",
                    (document_id, doc, emb.tolist())
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

    def get_suggestions(self, query, limit=5):
        query_embedding = self.model.encode([query])[0]
        logging.info(f"Encoded query: {query}")
        logging.info(f"Query embedding shape: {query_embedding.shape}")
        with self.conn.cursor() as cur:
            sql_query = """
            SELECT DISTINCT
                substring(content from '(?i)\\y\\w*' || %s || '\\w*\\y') as suggestion
            FROM documents
            WHERE embedding <-> %s::vector < 0.5
            LIMIT %s
            """
            logging.info(f"Executing SQL query: {sql_query}")
            logging.info(f"Query parameters: {query}, {query_embedding.tolist()}, {limit}")
            cur.execute(sql_query, (query, query_embedding.tolist(), limit))
            results = cur.fetchall()
        logging.info(f"Raw results from database: {results}")
        suggestions = [result[0] for result in results if result[0]]
        logging.info(f"Filtered suggestions: {suggestions}")
        return suggestions

    def remove_document(self, document_id):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM documents WHERE document_id = %s", (document_id,))
        self.conn.commit()

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()