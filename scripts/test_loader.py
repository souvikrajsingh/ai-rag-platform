from src.app.embedding.embedding_manager import EmbeddingManager
from src.app.retrieval.vector_store import VectorStore
from src.app.services.rag_service import RAGService

# Create objects
embedding_manager = EmbeddingManager()

vector_store = VectorStore(
    embedding_manager.embedding_model
)

# Load existing FAISS index
vector_store.load("data/vector_store")

# Create RAG Service
rag_service = RAGService(vector_store)

# Ask a question
query = "What is Elon Musk?"

answer = rag_service.ask(query)

print("\n=== Final Answer ===")
print(answer)