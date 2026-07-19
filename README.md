# 📚 RAG Pipeline with LangChain, FAISS & Gemini

A production-inspired Retrieval-Augmented Generation (RAG) application built in Python using LangChain, FAISS, Sentence Transformers, and Google's Gemini API.

The project ingests PDF documents, generates embeddings, stores them in a FAISS vector database, retrieves relevant context using semantic search, and generates answers using a Large Language Model (LLM).

---

## ✨ Features

- 📄 PDF document ingestion
- ✂️ Recursive text chunking
- 🧠 Sentence Transformer embeddings
- 🔎 Semantic similarity search with FAISS
- 💾 Persistent FAISS vector store
- ⚡ Incremental indexing using SHA-256 file hashing
- 🤖 Gemini LLM integration
- 📝 Prompt building with retrieved context
- 🏗️ Modular, production-style project structure

---

## 🏛️ Architecture

```
                    +----------------+
                    |   PDF Files    |
                    +-------+--------+
                            |
                            v
                 +---------------------+
                 |  Document Loader    |
                 +----------+----------+
                            |
                            v
                 +---------------------+
                 |    Text Splitter    |
                 +----------+----------+
                            |
                            v
                 +---------------------+
                 | Embedding Manager   |
                 +----------+----------+
                            |
                            v
                 +---------------------+
                 |    FAISS Index      |
                 +----------+----------+
                            |
          +-----------------+-----------------+
          |                                   |
          |                                   |
          v                                   v
 Incremental Indexing                 Similarity Search
     (Hash Manager)                          |
                                              v
                                   +------------------+
                                   | Prompt Builder   |
                                   +--------+---------+
                                            |
                                            v
                                   +------------------+
                                   | Gemini LLM       |
                                   +--------+---------+
                                            |
                                            v
                                       Final Answer
```

---

## 📂 Project Structure

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
│       ├── config/
│       ├── embedding/
│       ├── ingestion/
│       ├── llm/
│       ├── retrieval/
│       ├── services/
│       └── util/
│
├── .env
├── requirements.txt
└── README.md
```

---

## 🚀 Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd RAG
```

---

### 2. Create a virtual environment

macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure environment variables

Create a `.env` file.

```env
GEMINI_API_KEY=your_api_key_here
```

---

## 📥 Index Documents

Place PDFs inside

```
data/raw/
```

Run

```bash
python scripts/index_documents.py
```

The script will:

- Load PDFs
- Split text into chunks
- Generate embeddings
- Create or update the FAISS index
- Store SHA-256 hashes of indexed documents
- Skip unchanged files on future runs

---

## 💬 Ask Questions

Run

```bash
python scripts/test_loader.py
```

Example:

```
Query:
What is a Python dictionary?

Answer:
A Python dictionary is a mutable mapping that stores key-value pairs...
```

---

## 🔄 Incremental Indexing

The project avoids re-indexing unchanged documents.

Workflow:

```
PDF

↓

Calculate SHA-256 Hash

↓

Hash Exists?

    │
 ┌──┴──┐
 │     │
Yes    No
 │      │
Skip   Index
 │      │
 └──┬───┘
    │
Save Updated Hashes
```

Benefits:

- Faster indexing
- Reduced embedding API usage
- Avoids unnecessary FAISS updates

---

## 🛠️ Technologies

- Python
- LangChain
- FAISS
- Sentence Transformers
- Google Gemini API
- Pydantic Settings

---

## 📌 Current Status

Implemented:

- ✅ Document Loader
- ✅ Recursive Text Splitter
- ✅ Embedding Manager
- ✅ FAISS Vector Store
- ✅ Similarity Search
- ✅ Prompt Builder
- ✅ Gemini Integration
- ✅ RAG Service
- ✅ Vector Store Persistence
- ✅ Incremental Indexing

Planned:

- ⏳ FastAPI REST API
- ⏳ Streaming responses
- ⏳ Chat history / memory
- ⏳ Metadata filtering
- ⏳ Hybrid Search
- ⏳ Docker support
- ⏳ AWS deployment

---

## 📖 Learning Goals

This project is being built to understand:

- Retrieval-Augmented Generation (RAG)
- Embeddings
- Vector Databases
- Semantic Search
- LLM Integration
- Production AI Engineering practices

---

## 📄 License

This project is intended for learning and educational purposes.