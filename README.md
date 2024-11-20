# RAG System

A simplified RAG (Retrieval-Augmented Generation) system using Flask and Python, featuring in-memory vector storage, configurable LLM providers, and real-time search capabilities.

## Project Context

This project serves as a demonstration of using the Replit AI Agent for full-stack application development. It showcases how AI-assisted development can efficiently create a functional RAG system with various features and integrations.

### Development Journey

The project was developed iteratively following these key steps:

1. **Initial Prototype**
   - Set up Flask web application
   - Implemented basic PDF upload and text extraction
   - Created initial vector storage mechanism
   - Established basic search functionality

2. **PostgreSQL/pgvector Integration**
   - Integrated persistent vector storage
   - Implemented database schema for documents and embeddings
   - Added vector similarity search capabilities

3. **Advanced Chunking Strategies**
   - Developed semantic-aware text chunking
   - Implemented overlap between chunks
   - Added metadata retention for context

4. **Multiple Document Support**
   - Added multi-file upload capability
   - Implemented document management system
   - Created document listing and deletion features

5. **Real-time Frontend Features**
   - Added search suggestions with debouncing
   - Implemented result highlighting
   - Created loading indicators
   - Enhanced user interface responsiveness

6. **Documentation**
   - Created comprehensive documentation
   - Added usage instructions
   - Documented API and configurations

### Development Process Highlights

The development process was highly interactive and iterative:

1. **Feature Implementation**
   - Features were developed incrementally with continuous feedback
   - Each component was tested individually before integration
   - Improvements were made based on user feedback

2. **Testing Process**
   - Upload functionality was tested with various PDF formats
   - Search capabilities were verified with different query types
   - Real-time features were tested for responsiveness
   - Database operations were validated for correctness

3. **Issue Resolution**
   - Database schema issues were identified and fixed during vector storage integration
   - Template loading errors were resolved through proper path configuration
   - PDF processing errors were handled with robust error management
   - Search performance was optimized through index improvements

### Sample Development Interactions

Here are some real examples of how the AI agent and user collaborated during development:

1. **Database Schema Fix**
```
User: ERROR:root:Error processing file Mixture-of-Experts.pdf: column "document_id" of relation "documents" does not exist
Agent: The error indicates an issue with the database schema. I'll update the _create_table method to include the document_id column...
User: Confirmed it works
```

2. **Search Suggestions Implementation**
```
User: The suggestions array remains empty as I type
Agent: Let's investigate by adding more detailed logging in the suggestions functionality...
```

These interactions demonstrate the iterative development process and how issues were identified and resolved through collaboration between the AI agent and user.

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

## Interface Overview

[Screenshot of the interface will be added here.]

The interface is organized into four main sections:
1. **Upload Section**: Allows users to select and upload multiple PDF files
2. **Document List**: Displays uploaded documents with options to delete them
3. **Search Interface**: Features a search box with real-time suggestions as you type
4. **Results Area**: Shows the generated answer and relevant context with highlighted search terms

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
