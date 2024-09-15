import PyPDF2

def process_pdf(file_path):
    chunks = []
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text = page.extract_text()
            # Simple chunking strategy: split by paragraphs
            page_chunks = text.split('\n\n')
            chunks.extend(page_chunks)
    return chunks
