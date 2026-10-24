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
    
    # saved the FAISS index from RAM to on disk
    def save(self, path : str):
        self.vector_store.save_local(path)
    
    # Spins up the old index if any 

    def load (self, path:str):
        from pathlib import Path
        if (Path(path) / "index.faiss").exists():
            self.vector_store = FAISS.load_local(
                path,
                self.embedding_model,
                allow_dangerous_deserialization=True
            )

    def add (self, documents: list[Document]):
        if self.vector_store is None:
            self.vector_store = FAISS.from_documents(documents , self.embedding_model)
        else:
            self.vector_store.add_documents(documents)
