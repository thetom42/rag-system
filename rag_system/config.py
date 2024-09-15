import os

# Environment variables for configuration
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', '/tmp/uploads')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
EMBEDDING_MODEL = os.environ.get('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
LLM_PROVIDER = os.environ.get('LLM_PROVIDER', 'openai')

# Chunking configuration
CHUNK_SIZE = int(os.environ.get('CHUNK_SIZE', 1000))
CHUNK_OVERLAP = int(os.environ.get('CHUNK_OVERLAP', 200))

# PostgreSQL configuration
PGHOST = os.environ.get('PGHOST')
PGPORT = os.environ.get('PGPORT')
PGDATABASE = os.environ.get('PGDATABASE')
PGUSER = os.environ.get('PGUSER')
PGPASSWORD = os.environ.get('PGPASSWORD')
DATABASE_URL = os.environ.get('DATABASE_URL')
