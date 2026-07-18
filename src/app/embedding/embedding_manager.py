from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from src.app.config.settings import settings

class EmbeddingManager:
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    def embed(self, documents: list[Document]):
        texts = [doc.page_content for doc in documents]
        vectors = self.embedding_model.embed_documents(texts)
        return vectors