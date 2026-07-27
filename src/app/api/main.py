from fastapi import FastAPI
from src.app.api.route import router

app = FastAPI(title="RAG");
app.include_router(router)