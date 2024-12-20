import os
import uuid
import logging
from flask import request, jsonify, render_template
from werkzeug.utils import secure_filename
from .services.pdf_processor import process_pdf_with_metadata, get_page_numbers, get_text_statistics
from .models.vector_store import PostgresVectorStore
from .services.llm_adapter import LLMAdapter
from ..config import UPLOAD_FOLDER
import markdown
import re

vector_store = PostgresVectorStore()
llm_adapter = LLMAdapter()

CHUNK_SIZE = 2000
CHUNK_OVERLAP = 400

documents = {}

def init_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/upload', methods=['POST'])
    def upload_file():
        if 'files' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        files = request.files.getlist('files')
        if not files or files[0].filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        uploaded_documents = []
        
        for file in files:
            if file and file.filename.lower().endswith('.pdf'):
                try:
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    
                    chunks = process_pdf_with_metadata(file_path, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP)
                    document_id = str(uuid.uuid4())
                    vector_store.add_documents(chunks, document_id)
                    
                    num_pages = get_page_numbers(file_path)
                    stats = get_text_statistics(chunks)
                    
                    documents[document_id] = {
                        'id': document_id,
                        'filename': filename,
                        'path': file_path,
                        'num_pages': num_pages,
                        'stats': stats
                    }
                    
                    uploaded_documents.append(documents[document_id])
                except Exception as e:
                    logging.error(f"Error processing file {filename}: {str(e)}")
                    return jsonify({'error': f'Error processing file {filename}: {str(e)}'}), 500
            else:
                return jsonify({'error': f'Invalid file type for {file.filename}. Please upload PDFs only.'}), 400
        
        return jsonify({
            'message': 'Files uploaded and processed successfully',
            'documents': uploaded_documents
        }), 200

    @app.route('/search', methods=['POST'])
    def search():
        query = request.json.get('query')
        if not query:
            return jsonify({'error': 'No query provided'}), 400

        try:
            similar_chunks = vector_store.search(query)
            context = "\n\n".join(similar_chunks)

            prompt = (
                f"Based on the following context, answer the question: {query}\n\n"
                f"Context:\n{context}"
            )
            response = llm_adapter.generate_response(prompt)

            html_response = markdown.markdown(response)

            highlighted_chunks = highlight_text(similar_chunks, query)

            return jsonify({'answer': html_response, 'context': highlighted_chunks}), 200
        except Exception as e:
            logging.error(f"Error during search: {str(e)}")
            return jsonify({'error': 'An error occurred during the search process.'}), 500

    @app.route('/suggestions', methods=['POST'])
    def get_suggestions():
        query = request.json.get('query')
        logging.info(f"Received suggestion request for query: {query}")
        if not query or len(query) < 2:
            logging.info("Query too short, returning empty suggestions")
            return jsonify({'suggestions': []}), 200

        try:
            logging.info(f"Calling vector_store.get_suggestions with query: {query}")
            suggestions = vector_store.get_suggestions(query)
            logging.info(f"Generated suggestions: {suggestions}")
            response = jsonify({'suggestions': suggestions})
            logging.info(f"Sending response: {response.get_data(as_text=True)}")
            return response, 200
        except Exception as e:
            logging.error(f"Error fetching suggestions: {str(e)}")
            return jsonify({'error': 'An error occurred while fetching suggestions.'}), 500

    @app.route('/documents', methods=['GET'])
    def get_documents():
        try:
            return jsonify(list(documents.values())), 200
        except Exception as e:
            logging.error(f"Error fetching documents: {str(e)}")
            return jsonify({'error': 'An error occurred while fetching the document list.'}), 500

    @app.route('/documents/<document_id>', methods=['DELETE'])
    def delete_document(document_id):
        if document_id in documents:
            try:
                document = documents.pop(document_id)
                os.remove(document['path'])
                vector_store.remove_document(document_id)
                return '', 204
            except Exception as e:
                logging.error(f"Error deleting document {document_id}: {str(e)}")
                return jsonify({'error': f'An error occurred while deleting the document: {str(e)}'}), 500
        else:
            return jsonify({'error': 'Document not found'}), 404

def highlight_text(chunks, query):
    query_terms = re.findall(r'\w+', query.lower())
    highlighted_chunks = []

    for chunk in chunks:
        highlighted_chunk = chunk
        for term in query_terms:
            pattern = re.compile(re.escape(term), re.IGNORECASE)
            highlighted_chunk = pattern.sub(f'<mark>{term}</mark>', highlighted_chunk)
        highlighted_chunks.append(highlighted_chunk)

    return highlighted_chunks