from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pathlib import Path

from src.app.api.schemas import QueryRequest, QueryResponse, IngestResponse
from src.app.api.dependencies import rag_service, ingestion_service
from src.app.util.hash_manager import HashManager


router = APIRouter()


@router.get("/health")
def health():
    return {"status": "healthy"}


@router.get("/documents")
def documents():
    raw_directory = Path("data/raw")
    indexed_files = HashManager().load_hashes()
    files = []

    if raw_directory.exists():
        pdf_paths = (
            path
            for path in raw_directory.iterdir()
            if path.is_file() and path.suffix.lower() == ".pdf"
        )
        for path in sorted(pdf_paths, key=lambda item: item.name.lower()):
            files.append(
                {
                    "name": path.name,
                    "size_bytes": path.stat().st_size,
                    "indexed": path.name in indexed_files,
                }
            )

    return {"documents": files}


@router.get("/documents/{filename}")
def preview_document(filename: str):
    raw_directory = Path("data/raw").resolve()
    if Path(filename).name != filename or Path(filename).suffix.lower() != ".pdf":
        raise HTTPException(status_code=404, detail="Document not found.")

    file_path = (raw_directory / filename).resolve()
    if file_path.parent != raw_directory or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Document not found.")

    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename=file_path.name,
        content_disposition_type="inline",
    )


@router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    result = rag_service.ask(request.question)

    return QueryResponse(
        answer=result["answer"],
        sources=result["sources"],
    )


@router.post("/ingest", response_model=IngestResponse)
def ingest(file: UploadFile = File(...)):
    result = ingestion_service.ingest(file)
    return IngestResponse(
        message=result["message"],
        chunks_added=result["chunks_added"],
        filename=result["filename"],
    )