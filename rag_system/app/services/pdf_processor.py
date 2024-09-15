import io
import PyPDF2
from PyPDF2 import PdfReader
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from typing import List, Tuple, Dict

nltk.download('punkt_tab', quiet=True)


# Rest of the file content remains the same
def process_pdf(file_path: str,
                chunk_size: int = 1000,
                overlap: int = 200) -> List[str]:
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

    return create_semantic_chunks(text, chunk_size, overlap)


def create_semantic_chunks(text: str, chunk_size: int,
                           overlap: int) -> List[str]:
    sentences = sent_tokenize(text)
    words = [
        word for sentence in sentences for word in word_tokenize(sentence)
    ]
    chunks = []

    start = 0
    while start < len(words):
        chunk_words = words[start:start + chunk_size]
        chunk_text = ' '.join(chunk_words)

        # Adjust chunk to end at a sentence boundary
        last_period = chunk_text.rfind('.')
        if last_period != -1 and last_period != len(chunk_text) - 1:
            chunk_text = chunk_text[:last_period + 1]

        chunks.append(chunk_text)

        # Move the start index for the next chunk, considering overlap
        start += chunk_size - overlap

    return chunks


def get_page_numbers(file_path: str) -> int:
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        return len(reader.pages)


def extract_metadata(file_path: str) -> Tuple[str, str, int]:
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        info = reader.metadata
        title = info.title if info.title else "Untitled"
        author = info.author if info.author else "Unknown"
        num_pages = len(reader.pages)
    return title, author, num_pages


def create_chunk_with_metadata(chunk: str, metadata: Dict[str, str]) -> str:
    return f"Title: {metadata['title']}\nAuthor: {metadata['author']}\nPage: {metadata['page']}\nSection: {metadata['section']}\n\n{chunk}"


def process_pdf_with_metadata(file_path: str,
                              chunk_size: int = 1000,
                              overlap: int = 200) -> List[str]:
    title, author, num_pages = extract_metadata(file_path)

    try:
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            full_text = ""
            for page in reader.pages:
                full_text += page.extract_text() + "\n"

            chunks = create_semantic_chunks(full_text, chunk_size, overlap)

            chunks_with_metadata = []
            for chunk_num, chunk in enumerate(chunks, 1):
                metadata = {
                    "title": title,
                    "author": author,
                    "page": f"Multiple",
                    "section": f"Chunk {chunk_num}/{len(chunks)}"
                }
                chunks_with_metadata.append(
                    create_chunk_with_metadata(chunk, metadata))

        return chunks_with_metadata
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        raise


def get_text_statistics(chunks: List[str]) -> Dict[str, int]:
    total_words = sum(len(chunk.split()) for chunk in chunks)
    total_characters = sum(len(chunk) for chunk in chunks)
    return {
        "num_chunks": len(chunks),
        "total_words": total_words,
        "total_characters": total_characters,
        "avg_chunk_size": total_characters // len(chunks) if chunks else 0
    }
