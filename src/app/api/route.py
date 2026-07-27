from fastapi import APIRouter, UploadFile, File
from src.app.api.schemas import QueryRequest, QueryResponse, IngestResponse
from src.app.api.dependencies import rag_service, ingestion_service


router = APIRouter()

@router.get("/")
def root():
    return {"message": "Welcome to my AI RAG API!"}


@router.get("/health")
def health():
    return {"status": "healthy"}

@router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):

    result = rag_service.ask(request.question)

    return QueryResponse(
        answer= result["answer"],
        sources= result["sources"]
    )

@router.post("/ingest", response_model=IngestResponse)
def ingest(file: UploadFile = File(...)):
    result = ingestion_service.ingest(file)
    return IngestResponse(
        message= result["message"],
        chunks_added= result["chunks_added"],
        filename= result["filename"],
    )