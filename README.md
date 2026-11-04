# 📚 AI RAG Platform with FastAPI, Pinecone & Gemini

A production-inspired Retrieval-Augmented Generation (RAG) application built in Python using FastAPI, LangChain, Pinecone, and Google's Gemini API.

The application ingests PDF documents, generates vector embeddings, upserts them to Pinecone, retrieves relevant context using semantic search, and generates grounded answers using a Large Language Model (LLM).

The project follows a modular architecture inspired by production AI systems, separating ingestion, retrieval, prompting, LLM interaction, API endpoints, and configuration into independent components.

---

# ✨ Features

* 📄 PDF document ingestion
* ✂️ Recursive text chunking
* 🧠 Pinecone-managed embedding generation
* 🔎 Semantic similarity search with Pinecone
* 💾 Persistent Pinecone vector index
* 🤖 Google Gemini integrationfopen
* 📝 Prompt construction with retrieved context
* 🌐 FastAPI REST API
* 📑 Interactive Swagger UI (`/docs`)
* 🐳 Docker support
* 🏗️ Production-inspired modular architecture

---
# 🏛️ Architecture

<img width="1800" height="1080" alt="ai-rag-platform" src="https://github.com/user-attachments/assets/4e48299d-7246-4c2a-bd71-da019998933a" />


---

# 📂 Project Structure

```
RAG/
│
├── data/
│   └── pinecone_indexed_files.json # Generated Pinecone file hashes (not committed)
│
├── scripts/
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
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=ai-rag-platform
```

Keep this file private; it is ignored by Git. The Gemini and Pinecone keys are
required when the app starts.

---

# 📚 Create and Populate the Pinecone Index

Create the Pinecone index once with the configured name and the
`llama-text-embed-v2` integrated embedding model:

```bash
uv run python script.py
```

The script uses the AWS `us-east-1` serverless region. The API expects this
index to exist. Pinecone creates embeddings when text is
upserted and embeds queries during search; the app does not load a local
embedding model. If the index already exists with the old vector-only
configuration, delete it in Pinecone Console before running the script.

The SHA-256 file hashes are stored locally in
`data/pinecone_indexed_files.json` to track uploaded filenames and detect
duplicate uploads. Upload PDFs through the app or API; they are processed in
memory and their extracted text chunks and metadata are upserted to Pinecone.
Original PDF files are not retained locally.

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

# 🌐 Run the app

After creating `.env` and building the vector index, start the FastAPI server
from the repository root:

```bash
uv run uvicorn src.app.api.main:app --reload
```

The React UI source is in `src/frontend`. Its production build is included with
the app. To rebuild it after making frontend changes:

```bash
cd src/frontend
npm ci
npm run build
```

For frontend development with the FastAPI API running on port 8000, run
`npm run dev` from `src/frontend` and open the Vite URL it prints.

The web app is available at:

```
http://localhost:8000/
```

Upload PDFs from the document library, choose automatic ingestion or ingest
queued files with the button, and ask questions in the chat panel. The REST API
and interactive Swagger UI are also available at:

```
http://localhost:8000/health
http://localhost:8000/docs
```

Use `/ingest` to upload a PDF, `/documents` to list uploaded filenames with
their Pinecone index status, or `/query` to ask a question about indexed
documents. Original PDFs are not retained, so they cannot be previewed after
ingestion.

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

Create the Pinecone index and `.env` before starting the container:

```bash
uv run python script.py
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

---

# 🛠️ Tech Stack

* Python
* FastAPI
* LangChain
* Pinecone
* Google Gemini
* Pydantic Settings
* Docker

---

# 📌 Current Status

### Completed

* ✅ PDF Document Loader
* ✅ Recursive Text Splitter
* ✅ Pinecone-managed Embeddings
* ✅ Pinecone Vector Store
* ✅ Similarity Search
* ✅ Prompt Builder
* ✅ Gemini Integration
* ✅ RAG Service Layer
* ✅ Persistent Pinecone Index
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
