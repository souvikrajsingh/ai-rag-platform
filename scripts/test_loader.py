import os

from src.app.retrieval.vector_store import VectorStore
from src.app.api.auth import namespace_for_user
from src.app.services.rag_service import RAGService

vector_store = VectorStore()

# Create RAG Service
rag_service = RAGService(vector_store)

# Ask a question
query = "What is Elon Musk?"
user_sub = os.environ.get("COGNITO_USER_SUB")
if not user_sub:
    raise RuntimeError("Set COGNITO_USER_SUB to the Cognito sub for this account.")

answer = rag_service.ask(query, namespace_for_user(user_sub))

print("\n=== Final Answer ===")
print(answer)