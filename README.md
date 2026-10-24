# 📚 AI RAG Platform with FastAPI, FAISS & Gemini

A production-inspired Retrieval-Augmented Generation (RAG) application built in Python using FastAPI, LangChain, FAISS, and Google's Gemini API.

The application ingests PDF documents, generates vector embeddings, stores them in a FAISS vector database, retrieves relevant context using semantic search, and generates grounded answers using a Large Language Model (LLM).

The project follows a modular architecture inspired by production AI systems, separating ingestion, retrieval, prompting, LLM interaction, API endpoints, and configuration into independent components.

---

# ✨ Features

* 📄 PDF document ingestion
* ✂️ Recursive text chunking
* 🧠 Embedding generation
* 🔎 Semantic similarity search with FAISS
* 💾 Persistent FAISS vector store
* ⚡ Incremental indexing using SHA-256 file hashing
* 🤖 Google Gemini integrationfopen
* 📝 Prompt construction with retrieved context
* 🌐 FastAPI REST API
* 📑 Interactive Swagger UI (`/docs`)
* 🐳 Docker support
* 🏗️ Production-inspired modular architecture

---
# 🏛️ Architecture

```
                         +--------------------+
                         |    PDF Documents   |
                         +---------+----------+
                                   |
                                   ▼
                     +---------------------------+
                     |     Document Loader       |
                     +------------+--------------+
                                  |
                                  ▼
                     +---------------------------+
                     |      Text Splitter        |
                     +------------+--------------+
                                  |
                                  ▼
                     +---------------------------+
                     |    Embedding Manager      |
                     +------------+--------------+
                                  |
                                  ▼
                     +---------------------------+
                     |       FAISS Index         |
                     +------------+--------------+
                                  |
             +--------------------+----------------------+
             |                                           |
             ▼                                           ▼
      Incremental Indexing                    Similarity Search
        (SHA-256 Hashing)                            |
                                                      ▼
                                           +----------------------+
                                           |    Prompt Builder    |
                                           +----------+-----------+
                                                      |
                                                      ▼
                                           +----------------------+
                                           |    Gemini LLM        |
                                           +----------+-----------+
                                                      |
                                                      ▼
                                             RAG Service Layer
                                                      |
                                                      ▼
                                               FastAPI Endpoint
                                                      |
                                                      ▼
                                              JSON API Response
```

---

# 📂 Project Structure

```
RAG/
│
├── data/
│   ├── raw/                   # Source PDFs
│   ├── vector_store/          # Generated FAISS index (not committed)
│   └── indexed_files.json     # Generated file hashes (not committed)
│
├── scripts/
│   ├── index_documents.py
│   ├── test_hash_manager.py
│   └── test_loader.py
│
├── src/
│   └── app/
│       ├── api/
│       │   ├── dependencies.py
│       │   ├── main.py
│       │   ├── route.py
│       │   └── schemas.py
│       │
│       ├── config/
│       ├── embedding/
│       ├── ingestion/
│       ├── llm/
│       ├── retrieval/
│       ├── services/
│       └── util/
│
├── Dockerfile
├── pyproject.toml
├── uv.lock
└── README.md
```

---

# 🚀 Getting Started

## 1. Clone the repository

```bash
git clone https://github.com/souvikrajsingh/ai-rag-platform.git
cd ai-rag-platform
```

---

## 2. Install Python and uv

Python 3.14 or newer is required. Install `uv` with Python's package manager:

```bash
python3.14 -m pip install uv
```

On Windows, use the Python launcher:

```bash
py -3.14 -m pip install uv
```

---

## 3. Install project dependencies

Dependencies are declared in `pyproject.toml` and pinned by `uv.lock`. From the
repository root, run:

```bash
uv sync --locked
```

---

## 4. Configure environment variables

Create a `.env` file in the repository root:

```env
gemini_api_key=your_gemini_api_key
```

Keep this file private; it is ignored by Git. Both settings are currently
required when the app starts. Gemini is used for answer generation; the OpenAI
key is required by the current settings but is not used by the request path.

---

# 📚 Build the Vector Index

The FAISS index and indexed-file hash list are generated locally and are not
included in a fresh clone. The API loads the index during startup, so build it
before starting the API. The repository includes PDFs under `data/raw/`; the
indexing script processes those PDFs and downloads the embedding model on its
first run.

```bash
uv run python scripts/index_documents.py
```

This creates `data/vector_store/` and `data/indexed_files.json`. Re-run the
command after adding PDFs to `data/raw/`; unchanged files are skipped.

## Add more documents

Place additional PDF files inside:

```
data/raw/
```

# 💬 Query from Python

With the index built, run the example query:

```bash
uv run python scripts/test_loader.py
```

Example:

```
Question:
What is Retrieval-Augmented Generation?

Answer:
Retrieval-Augmented Generation (RAG) combines information retrieval with
large language models to generate grounded responses...
```

---

# 🌐 Run the API

After creating `.env` and building the vector index, start the FastAPI server
from the repository root:

```bash
uv run uvicorn src.app.api.main:app --reload
```

The API and interactive Swagger UI are available at:

```
http://localhost:8000/
http://localhost:8000/docs
```

The health check is at `http://localhost:8000/health`. Use `/ingest` to upload a
PDF or `/query` to ask a question about indexed documents.

Example request:

```json
{
  "question": "Explain what embeddings are."
}
```

Example response:

```json
{
  "answer": "...",
  "sources": [
    {
      "source": "python_overview.pdf",
      "page": 10
    }
  ]
}
```

---

# 🐳 Run with Docker

Docker needs a vector index in the build context. Create `.env` and run the
indexing command from the previous section before building the image:

```bash
uv run python scripts/index_documents.py
docker build -t ai-rag-platform .
```

Start the container, passing the local environment variables:

```bash
docker run --env-file .env -p 8000:8000 ai-rag-platform
```

The API will be available at:

```
http://localhost:8000
```

Swagger UI:

```
http://localhost:8000/docs
```

---

# 🔄 Incremental Indexing

The indexing script avoids re-indexing documents that have not changed. Run
`uv run python scripts/index_documents.py` after adding PDFs to `data/raw/`.

```
PDF

↓

Generate SHA-256 Hash

↓

Hash Exists?

    │
 ┌──┴─────┐
 │         │
Yes       No
 │         │
Skip     Index
 │         │
 └────┬────┘
      │
Update Hash Store
```

Benefits:

* Faster indexing
* Reduced embedding generation
* Lower API usage
* Efficient updates

---

# 🛠️ Tech Stack

* Python
* FastAPI
* LangChain
* FAISS
* Google Gemini
* Pydantic Settings
* Docker

---

# 📌 Current Status

### Completed

* ✅ PDF Document Loader
* ✅ Recursive Text Splitter
* ✅ Embedding Manager
* ✅ FAISS Vector Store
* ✅ Similarity Search
* ✅ Prompt Builder
* ✅ Gemini Integration
* ✅ RAG Service Layer
* ✅ Persistent Vector Store
* ✅ Incremental Indexing
* ✅ FastAPI REST API
* ✅ Swagger Documentation
* ✅ Docker Containerisation

### Planned

* ⏳ Streaming responses
* ⏳ Metadata filtering
* ⏳ Hybrid search
* ⏳ Authentication
* ⏳ Conversation memory
* ⏳ AWS deployment
* ⏳ CI/CD pipeline

---

# 🎯 Learning Objectives

This project explores the end-to-end development of a Retrieval-Augmented Generation system, including:

* Retrieval-Augmented Generation (RAG)
* Embeddings and semantic search
* Vector databases
* Prompt engineering
* LLM integration
* FastAPI application development
* Docker containerisation
* Production-inspired software architecture

---

# 📄 License

This project is intended for learning and educational purposes.
