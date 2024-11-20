# RAG System

A simplified RAG (Retrieval-Augmented Generation) system using Flask and Python, featuring in-memory vector storage, configurable LLM providers, and real-time search capabilities.

## Features

- **Document Processing**
  - Multiple PDF document upload support
  - Advanced text chunking strategies
  - Document management (view, delete)
  - Real-time document statistics

- **Vector Search**
  - PostgreSQL with pgvector for persistent storage
  - Efficient similarity search
  - Real-time search suggestions with debouncing

- **User Interface**
  - Interactive search experience
  - Result highlighting
  - Visual loading indicators
  - Document management interface

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```
PGHOST=your_postgres_host
PGPORT=your_postgres_port
PGDATABASE=your_postgres_database
PGUSER=your_postgres_user
PGPASSWORD=your_postgres_password
OPENAI_API_KEY=your_openai_api_key
```

## Usage

1. Start the Flask server:
```bash
python -m rag_system.main
```

2. Open your browser and navigate to `http://localhost:5000`

3. Upload PDF documents using the upload form

4. Use the search functionality to query your documents

## Configuration

The system can be configured through environment variables:

- `EMBEDDING_MODEL`: Model used for text embeddings (default: 'sentence-transformers/all-MiniLM-L6-v2')
- `LLM_PROVIDER`: LLM provider for text generation (default: 'openai')
- `CHUNK_SIZE`: Size of text chunks (default: 2000)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 400)

## Project Structure

```
rag_system/
├── app/
│   ├── models/
│   │   └── vector_store.py    # Vector storage implementation
│   ├── services/
│   │   ├── llm_adapter.py     # LLM integration
│   │   └── pdf_processor.py   # PDF processing logic
│   ├── templates/
│   │   └── index.html        # Main HTML template
│   └── routes.py             # Flask routes
├── static/
│   ├── css/
│   │   └── style.css        # Application styles
│   └── js/
│       └── main.js          # Frontend JavaScript
└── main.py                  # Application entry point
```

## Dependencies

- Flask: Web framework
- PyPDF2: PDF processing
- sentence-transformers: Text embeddings
- pgvector: Vector similarity search
- psycopg2: PostgreSQL adapter
- OpenAI: LLM integration

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## License

MIT License
