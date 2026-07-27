from fastapi import APIRouter
from src.app.api.schemas import QueryRequest, QueryResponse
from src.app.api.dependencies import rag_service

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