from typing import Any

from fastapi import APIRouter, Depends, File, UploadFile

from src.app.api.auth import namespace_for_user, require_authenticated_user
from src.app.api.schemas import QueryRequest, QueryResponse, IngestResponse
from src.app.api.dependencies import rag_service, ingestion_service, vector_store
from src.app.util.hash_manager import HashManager


router = APIRouter()


@router.get("/health")
def health():
    return {"status": "healthy"}


@router.get("/documents")
def documents(user: dict[str, Any] = Depends(require_authenticated_user)):
    namespace = namespace_for_user(user["sub"])
    indexed_files = HashManager(namespace).load_hashes()
    namespace_is_indexed = vector_store.has_namespace(namespace)
    files = [
        {
            "name": filename,
            "size_bytes": None,
            "indexed": namespace_is_indexed,
        }
        for filename in indexed_files
    ]
    return {"documents": sorted(files, key=lambda item: item["name"].lower())}


@router.post("/query", response_model=QueryResponse)
def query(
    request: QueryRequest,
    user: dict[str, Any] = Depends(require_authenticated_user),
):
    namespace = namespace_for_user(user["sub"])
    result = rag_service.ask(request.question, namespace)

    return QueryResponse(
        answer=result["answer"],
        sources=result["sources"],
    )


@router.post("/ingest", response_model=IngestResponse)
def ingest(
    file: UploadFile = File(...),
    user: dict[str, Any] = Depends(require_authenticated_user),
):
    namespace = namespace_for_user(user["sub"])
    result = ingestion_service.ingest(file, namespace)
    return IngestResponse(
        message=result["message"],
        chunks_added=result["chunks_added"],
        filename=result["filename"],
    )