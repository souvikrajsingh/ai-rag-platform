from fastapi import APIRouter, File, UploadFile

from src.app.api.schemas import QueryRequest, QueryResponse, IngestResponse
from src.app.api.dependencies import rag_service, ingestion_service, vector_store
from src.app.util.hash_manager import HashManager


router = APIRouter()


@router.get("/health")
def health():
    return {"status": "healthy"}


@router.get("/documents")
def documents():
    indexed_files = HashManager().load_hashes()
    pinecone_namespaces = vector_store.namespaces()
    files = [
        {
            "name": filename,
            "size_bytes": None,
            "indexed": filename in pinecone_namespaces,
        }
        for filename in indexed_files
    ]
    return {"documents": sorted(files, key=lambda item: item["name"].lower())}


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