from src.app.ingestion.document_loader import DocumentLoader
from src.app.ingestion.text_splitter import TextSplitter
from src.app.retrieval.vector_store import VectorStore
from fastapi import HTTPException, UploadFile
from pathlib import Path
import shutil
from src.app.util.hash_manager import HashManager


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
        self.hash_manager = HashManager()


    # validating if the file is a PDF or not
    def _validate_pdf(self, file: UploadFile) -> None:
        if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
            raise HTTPException(
                status_code=415,
                detail="Only PDF files are supported.",
            )

        file_header = file.file.read(1024)
        file.file.seek(0)

        #checking the first 1024 bytes for the PDF header if not present, throw an exception
        if b"%PDF-" not in file_header:
            raise HTTPException(
                status_code=415,
                detail="The uploaded file is not a valid PDF.",
            )


    #check if the file with the same hash(content) already exists
    def _match_hash(self, file: UploadFile) -> str:
        incoming_file_hash = self.hash_manager.calculate_hash(file.file)

        existing_hashes = self.hash_manager.load_hashes()
        if incoming_file_hash in existing_hashes.values():
            raise HTTPException(
                status_code=409,
                detail="This file has already been uploaded.",
            )

        return incoming_file_hash

    
    def _save_uploaded_file(self, file: UploadFile) -> str:
            upload_path = Path("data/raw") / Path(file.filename).name
            upload_path.parent.mkdir(parents=True, exist_ok=True)

            with open(upload_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            return str(upload_path)

    def ingest(self, file: UploadFile):
        self._validate_pdf(file)
        incoming_file_hash = self._match_hash(file)

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

        existing_hashes = self.hash_manager.load_hashes()
        existing_hashes[file.filename] = incoming_file_hash
        self.hash_manager.save_hashes(existing_hashes)

        return {
            "message": "Ingestion Successful!",
            "chunks_added": len(chunks),
            "filename": file.filename,
        }
    
    