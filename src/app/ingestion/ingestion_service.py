from pathlib import Path

from fastapi import HTTPException, UploadFile

from src.app.ingestion.document_loader import DocumentLoader
from src.app.ingestion.text_splitter import TextSplitter
from src.app.retrieval.vector_store import VectorStore
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

    # validating if the file is a PDF or not
    def _validate_pdf(self, file: UploadFile) -> None:
        if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
            raise HTTPException(
                status_code=415,
                detail="Only PDF files are supported.",
            )

        file_header = file.file.read(1024)
        file.file.seek(0)

        # checking the first 1024 bytes for the PDF header
        if b"%PDF-" not in file_header:
            raise HTTPException(
                status_code=415,
                detail="The uploaded file is not a valid PDF.",
            )

    def _match_hash(self, file: UploadFile, hash_manager: HashManager) -> str:
        # check if the same file has already been uploaded by this user
        incoming_file_hash = hash_manager.calculate_hash(file.file)

        existing_hashes = hash_manager.load_hashes()
        if incoming_file_hash in existing_hashes.values():
            raise HTTPException(
                status_code=409,
                detail="This file has already been uploaded.",
            )

        return incoming_file_hash

    def ingest(self, file: UploadFile, namespace: str):
        self._validate_pdf(file)
        hash_manager = HashManager(namespace)
        incoming_file_hash = self._match_hash(file, hash_manager)

        filename = Path(file.filename).name
        documents = self.document_loader.load_stream(file.file, filename)

        chunks = self.text_splitter.split(documents)
        if not chunks:
            raise HTTPException(
                status_code=422,
                detail=(
                    "No extractable text was found in this PDF. It may be a scanned "
                    "document; scanned PDFs need OCR before they can be indexed."
                ),
            )

        self.vector_store.upsert(chunks, namespace)

        existing_hashes = hash_manager.load_hashes()
        existing_hashes[filename] = incoming_file_hash
        hash_manager.save_hashes(existing_hashes)

        return {
            "message": "Ingestion Successful!",
            "chunks_added": len(chunks),
            "filename": filename,
        }
