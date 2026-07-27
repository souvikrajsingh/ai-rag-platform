from src.app.ingestion.document_loader import DocumentLoader
from src.app.ingestion.text_splitter import TextSplitter
from src.app.retrieval.vector_store import VectorStore
from fastapi import UploadFile
from pathlib import Path
import shutil



class IngestionService:
    def __init__(
        self,
        document_loader: DocumentLoader,
        text_splitter: TextSplitter,
        vector_store: VectorStore,
    ):
        self.document_loader = document_loader
        self.text_splitter = text_splitter
        self.vector_store = vector_store

    def _save_uploaded_file(self, file: UploadFile) -> str:
            upload_path = Path("data/raw") / file.filename
    
            with open(upload_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
    
            return str(upload_path)

    def ingest(self, file: UploadFile):
        # Save uploaded file
        path = self._save_uploaded_file(file)

        # Load the document
        documents = self.document_loader.load(path)

        # Split into chunks
        chunks = self.text_splitter.split(documents)

        # Add to vector store
        self.vector_store.add(chunks)

        # Persist updated FAISS index
        self.vector_store.save("data/vector_store")

        return {
            "message": "Ingestion Successful!",
            "chunks_added": len(chunks),
            "filename": file.filename,
        }
    
    