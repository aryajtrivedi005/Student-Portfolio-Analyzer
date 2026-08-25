import numpy as np
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rag.knowledge_base import KNOWLEDGE_DOCUMENTS

class VectorStore:
    def __init__(self):
        self.documents = KNOWLEDGE_DOCUMENTS
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.corpus = [f"{doc['title']}\n{doc['content']}" for doc in self.documents]
        if self.corpus:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus)
        else:
            self.tfidf_matrix = None

    def search(self, query: str, top_k: int = 2) -> List[Dict[str, Any]]:
        if self.tfidf_matrix is None or not query.strip():
            return self.documents[:top_k]

        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        top_indices = np.argsort(scores)[::-1][:top_k]

        results = []
        for idx in top_indices:
            results.append({
                "title": self.documents[idx]['title'],
                "content": self.documents[idx]['content'],
                "score": float(scores[idx])
            })
        return results

# Singleton instance
_vector_store = None

def get_vector_store() -> VectorStore:
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore()
    return _vector_store
