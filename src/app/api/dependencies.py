from src.app.embedding.embedding_manager import EmbeddingManager
from src.app.retrieval.vector_store import VectorStore
from src.app.services.rag_service import RAGService


embedding_manager = EmbeddingManager()

vector_store = VectorStore(
    embedding_model=embedding_manager.embedding_model
)

vector_store.load("data/vector_store")

rag_service = RAGService(vector_store)