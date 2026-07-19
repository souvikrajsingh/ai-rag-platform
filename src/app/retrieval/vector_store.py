from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

class VectorStore:

    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self.vector_store = None

    def create(self, documents: list[Document]):
        self.vector_store = FAISS.from_documents(
            documents,
            self.embedding_model
        )
        return self.vector_store
    
    def search(self, query: str, k: int = 3):
        return self.vector_store.similarity_search(
            query=query,
            k=k
        )
    