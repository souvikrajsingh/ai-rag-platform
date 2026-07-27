from pydantic import BaseModel

class Source(BaseModel):
    source: str
    page: int | str



class QueryRequest(BaseModel):
    question:str

class QueryResponse(BaseModel):
    answer:str
    sources: list[Source]

class IngestResponse(BaseModel):
    message:str
    chunks_added:int
    filename:str