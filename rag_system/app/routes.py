import os
from flask import request, jsonify, render_template
from werkzeug.utils import secure_filename
from .services.pdf_processor import process_pdf_with_metadata, get_page_numbers, get_text_statistics
from .models.vector_store import PostgresVectorStore
from .services.llm_adapter import LLMAdapter
from ..config import UPLOAD_FOLDER
import markdown

vector_store = PostgresVectorStore()
llm_adapter = LLMAdapter()

# Increased chunk size and overlap for better context retention
CHUNK_SIZE = 2000
CHUNK_OVERLAP = 400

def init_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/upload', methods=['POST'])
    def upload_file():
        print("Upload route called")  # Debug print
        if 'file' not in request.files:
            print("No file part in request")  # Debug print
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            print("No selected file")  # Debug print
            return jsonify({'error': 'No selected file'}), 400
        if file and file.filename.lower().endswith('.pdf'):
            try:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                print(f"File saved to {file_path}")  # Debug print
                chunks = process_pdf_with_metadata(file_path, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP)
                vector_store.add_documents(chunks)
                num_pages = get_page_numbers(file_path)
                stats = get_text_statistics(chunks)
                return jsonify({
                    'message': 'File uploaded and processed successfully',
                    'chunks': chunks[:3],
                    'num_pages': num_pages,
                    'stats': stats
                }), 200
            except Exception as e:
                print(f"Error processing file: {str(e)}")  # Debug print
                return jsonify({'error': f'Error processing file: {str(e)}'}), 500
        else:
            print("Invalid file type")  # Debug print
            return jsonify({'error': 'Invalid file type. Please upload a PDF.'}), 400

    @app.route('/search', methods=['POST'])
    def search():
        query = request.json.get('query')
        if not query:
            return jsonify({'error': 'No query provided'}), 400

        similar_chunks = vector_store.search(query)
        context = "\n\n".join(similar_chunks)

        prompt = (
            f"Based on the following context, answer the question: {query}\n\n"
            f"Context:\n{context}"
        )
        response = llm_adapter.generate_response(prompt)

        # Convert the response from Markdown to HTML
        html_response = markdown.markdown(response)

        return jsonify({'answer': html_response, 'context': similar_chunks}), 200
