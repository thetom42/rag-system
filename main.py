import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from pdf_processor import process_pdf
from vector_store import VectorStore
from llm_adapter import LLMAdapter
from config import UPLOAD_FOLDER
import markdown

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

vector_store = VectorStore()
llm_adapter = LLMAdapter()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.lower().endswith('.pdf'):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        chunks = process_pdf(file_path)
        vector_store.add_documents(chunks)
        return jsonify({
            'message': 'File uploaded and processed successfully'
        }), 200
    else:
        return jsonify({
            'error': 'Invalid file type. Please upload a PDF.'
        }), 400


@app.route('/search', methods=['POST'])
def search():
    query = request.json.get('query')
    if not query:
        return jsonify({'error': 'No query provided'}), 400

    similar_chunks = vector_store.search(query)
    context = " ".join(similar_chunks)

    prompt = (
        f"Based on the following context, answer the question: {query}\n\n"
        f"Context: {context}"
    )
    response = llm_adapter.generate_response(prompt)

    # Convert the response from Markdown to HTML
    html_response = markdown.markdown(response)

    return jsonify({'answer': html_response, 'context': similar_chunks}), 200


if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
