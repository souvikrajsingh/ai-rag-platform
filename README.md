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
* 🤖 Google Gemini integration
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
│   ├── raw/
│   ├── vector_store/
│   └── indexed_files.json
│
├── scripts/
│   ├── index_documents.py
│   └── test_loader.py
│
├── src/
│   └── app/
│       ├── api/
│       │   ├── dependencies.py
│       │   ├── routes.py
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
├── requirements.txt
├── .env
└── README.md
```

---

# 🚀 Getting Started

## 1. Clone the repository

```bash
git clone <repository-url>
cd RAG
```

---

## 2. Create a virtual environment

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure environment variables

Create a `.env` file.

```env
openai_api_key=YOUR_OPENAI_KEY
gemini_api_key=YOUR_GEMINI_KEY
```

---

# 📥 Index Documents

Place PDF files inside:

```
data/raw/
```

Run:

```bash
python scripts/index_documents.py
```

The indexing pipeline:

* Loads PDF documents
* Splits documents into chunks
* Generates embeddings
* Stores embeddings in FAISS
* Saves document hashes
* Skips unchanged files during future indexing

---

# 💬 Query from Python

Run:

```bash
python scripts/test_loader.py
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

Start the FastAPI server:

```bash
uvicorn src.main:app --reload
```

Open Swagger UI:

```
http://localhost:8000/docs
```

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

Build the image:

```bash
docker build -t ai-rag-platform .
```

Run the container:

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

The system avoids re-indexing documents that have not changed.

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
