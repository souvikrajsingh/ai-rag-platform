from src.app.retrieval.vector_store import VectorStore
from src.app.services.rag_service import RAGService
from src.app.ingestion.ingestion_service import IngestionService
from src.app.ingestion.document_loader import DocumentLoader
from src.app.ingestion.text_splitter import TextSplitter

document_loader = DocumentLoader()
text_splitter = TextSplitter()
vector_store = VectorStore()

ingestion_service = IngestionService(document_loader, text_splitter,vector_store)
rag_service = RAGService(vector_store)
