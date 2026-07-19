# AI RAG Platform

A Retrieval-Augmented Generation (RAG) application built using Python, LangChain, FAISS, Hugging Face Embeddings, and Google Gemini.

The project demonstrates an end-to-end RAG pipeline capable of ingesting PDF documents, generating semantic embeddings, performing vector similarity search, and answering user questions using a Large Language Model.

---

## Features

- PDF document ingestion
- Recursive text chunking
- Semantic embeddings using Hugging Face
- FAISS vector database
- Semantic similarity search
- Prompt engineering layer
- Google Gemini LLM integration
- Modular and scalable architecture

---

## Tech Stack

- Python 3.14
- LangChain
- FAISS
- Hugging Face Embeddings
- Google Gemini
- Pydantic Settings
- UV Package Manager

---

## Project Structure

```text
src/
└── app/
    ├── config/
    │   └── settings.py
    │
    ├── ingestion/
    │   ├── document_loader.py
    │   └── text_splitter.py
    │
    ├── embedding/
    │   └── embedding_manager.py
    │
    ├── retrieval/
    │   └── vector_store.py
    │
    ├── llm/
    │   ├── prompt_builder.py
    │   └── llm_manager.py
    │
    └── api/

scripts/
    test_loader.py

data/
    raw/
```

---

## RAG Pipeline

```text
                 INDEXING

PDF
 │
 ▼
Document Loader
 │
 ▼
Text Splitter
 │
 ▼
Embedding Model
 │
 ▼
FAISS Vector Store


══════════════════════════════════


                 QUERYING

User Question
 │
 ▼
Similarity Search
 │
 ▼
Relevant Chunks
 │
 ▼
Prompt Builder
 │
 ▼
Gemini LLM
 │
 ▼
Generated Answer
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/ai-rag-platform.git
```

Move into the project

```bash
cd ai-rag-platform
```

Create a virtual environment

```bash
uv venv
```

Activate it

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

Install dependencies

```bash
uv sync
```

---

## Environment Variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=your_api_key_here
```

---

## Running the Project

Run the test script

```bash
PYTHONPATH=. uv run python scripts/test_loader.py
```

---

## Current Workflow

The application performs the following steps:

1. Load a PDF document.
2. Split the document into overlapping chunks.
3. Generate embeddings for each chunk.
4. Store embeddings inside a FAISS vector index.
5. Perform semantic similarity search.
6. Build a prompt using the retrieved chunks.
7. Send the prompt to Gemini.
8. Return the generated answer.

---

## Example Query

```
What is a Python dictionary?
```

Example Response

```
A Python dictionary is a built-in data structure that stores data as key-value pairs...
```

---

## Dependencies

- langchain
- langchain-community
- langchain-google-genai
- sentence-transformers
- faiss-cpu
- pypdf
- pydantic-settings
- fastapi
- uvicorn

---

## Future Improvements

- FastAPI REST API
- Save/Load FAISS Index
- Multi-document support
- Metadata-based filtering
- Source citations
- Chat history / memory
- Streaming responses
- Docker support
- AWS Deployment
- CI/CD Pipeline
- Hybrid Search (BM25 + Vector Search)
- Reranking
- Evaluation framework

---

## Learning Goals

This repository was built to gain hands-on experience with:

- Retrieval-Augmented Generation (RAG)
- Vector Databases
- Embedding Models
- Prompt Engineering
- Large Language Models
- LangChain
- AI System Design
- Production-ready Python Architecture

---

## License

MIT License