import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL


class VectorStore:

    def __init__(self):
        self.embeddings = []
        self.documents = []
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.index = None

    def add_documents(self, documents):
        new_embeddings = self.model.encode(documents)
        self.embeddings.extend(new_embeddings)
        self.documents.extend(documents)
        self._update_index()

    def _update_index(self):
        if self.index is None:
            self.index = faiss.IndexFlatL2(
                self.model.get_sentence_embedding_dimension())
        self.index = faiss.IndexFlatL2(self.embeddings[0].shape[0])
        self.index.add(
            np.array(self.embeddings, dtype=np.float32).reshape(
                -1, self.model.get_sentence_embedding_dimension()))

    def search(self, query, k=3):
        query_embedding = self.model.encode([query])
        if self.index is None or len(self.embeddings) == 0:
            return []
        distances, indices = self.index.search(
            np.array(query_embedding, dtype=np.float32).reshape(1, -1), k)
        return [self.documents[i] for i in indices[0]]
