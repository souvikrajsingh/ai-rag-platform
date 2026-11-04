from src.app.retrieval.vector_store import VectorStore
from src.app.services.rag_service import RAGService

vector_store = VectorStore()

# Create RAG Service
rag_service = RAGService(vector_store)

# Ask a question
query = "What is Elon Musk?"

answer = rag_service.ask(query)

print("\n=== Final Answer ===")
print(answer)