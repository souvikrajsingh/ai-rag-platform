# 📚 AI RAG Platform with FastAPI, Pinecone & Gemini

A production-inspired Retrieval-Augmented Generation (RAG) application built in Python using FastAPI, LangChain, Pinecone, and Google's Gemini API.

The application ingests PDF documents, generates vector embeddings, upserts them to Pinecone, retrieves relevant context using semantic search, and generates grounded answers using a Large Language Model (LLM). The frontend is maintained separately in the private [ai-rag-frontend repository](https://github.com/souvikrajsingh/ai-rag-frontend).

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
GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=ai-rag-platform
AWS_REGION=ap-southeast-2
COGNITO_USER_POOL_ID=ap-southeast-2_xzPp5w9xV
COGNITO_CLIENT_ID=5dupvtu5sq09n8glj6pp3r1ut9
COGNITO_CLIENT_SECRET=your_cognito_app_client_secret
SESSION_SECRET_KEY=generate_a_random_secret
SESSION_COOKIE_SECURE=false
SESSION_COOKIE_SAME_SITE=lax
FRONTEND_URL=http://localhost:5173
FRONTEND_ORIGINS=http://localhost:5173
```

Use your own provider keys and keep this file private; it is ignored by Git.
The Gemini, Groq, and Pinecone keys are required when the app starts. Do not
put spaces before or after the `=` sign.

In the Cognito user pool, enable the authorization code grant and the `openid`,
`email`, and `phone` scopes for this app client. Add
`http://localhost:8000/auth/callback` as an allowed callback URL. The app's
`/login` route starts OIDC sign-in and `/logout` clears the local session.
Generate `SESSION_SECRET_KEY` with
`python -c 'import secrets; print(secrets.token_urlsafe(32))'`; keep it stable
between restarts and private. Set `SESSION_COOKIE_SECURE=true` when serving the
app over HTTPS. The backend API redirects `/` to `FRONTEND_URL` and allows
credentialed browser requests only from the comma-separated `FRONTEND_ORIGINS`.
For separate HTTPS Render services, set `SESSION_COOKIE_SECURE=true` and
`SESSION_COOKIE_SAME_SITE=none`; set both frontend values to the exact deployed
frontend origin. Register the backend's public `/auth/callback` URL in Cognito
and set the matching `AWS_REGION`, pool, and client values.

Enable self-service sign-up in the Cognito user pool's sign-up experience.
Signed-out visitors see **Sign in with Cognito** and **Create an account**;
the latter opens Cognito's managed sign-up page. After sign-in, API requests
require the session and use a Pinecone namespace derived from the Cognito user
`sub`, so uploads and searches are isolated per account. Existing shared
filename-based Pinecone namespaces are left untouched and hidden; users must
re-upload those documents after signing in. The local upload manifest is also
partitioned per user under `data/user_uploads/`.

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

# 🌐 Run the API and frontend

After creating `.env` and building the vector index, start the FastAPI API
from the repository root:

```bash
uv run uvicorn src.app.api.main:app --reload
```

Clone the private frontend repository in a separate directory and start Vite:

```bash
git clone https://github.com/souvikrajsingh/ai-rag-frontend.git
cd ai-rag-frontend
npm ci
npm run dev
```

With the default Vite proxy, the frontend talks to the API on `localhost:8000`.
Open the Vite URL it prints (normally):

```
http://localhost:5173/
```

Signed-out users are sent to the frontend sign-in page. The API and interactive
Swagger UI are available at:

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

Docker builds only the FastAPI backend. The frontend is deployed separately
from the private frontend repository. You do not need to install Python or
`uv` to build and run the API image; you do need Docker Desktop (or Docker
Engine) and API keys for the external services.

1. Clone the repository and move into its directory:

   ```bash
   git clone https://github.com/souvikrajsingh/ai-rag-platform.git
   cd ai-rag-platform
   ```

2. Create a `.env` file in the repository root with your own keys:

   ```env
   gemini_api_key=your_gemini_api_key
   GROQ_API_KEY=your_groq_api_key
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_INDEX_NAME=ai-rag-platform
   AWS_REGION=ap-southeast-2
   COGNITO_USER_POOL_ID=your_user_pool_id
   COGNITO_CLIENT_ID=your_app_client_id
   COGNITO_CLIENT_SECRET=your_app_client_secret
   SESSION_SECRET_KEY=generate_a_random_secret
   SESSION_COOKIE_SECURE=false
   SESSION_COOKIE_SAME_SITE=lax
   FRONTEND_URL=http://localhost:5173
   FRONTEND_ORIGINS=http://localhost:5173
   ```

   Do not commit `.env` or share its contents. Docker reads it when the
   container starts; the keys are not built into the image.

3. Create the Pinecone index by following
   [Create and Populate the Pinecone Index](#-create-and-populate-the-pinecone-index)
   above. This setup step requires Python and `uv`; it creates the index in
   your Pinecone account. Other users need their own keys and index.

4. Build the Docker image from the repository root:

   ```bash
   docker build -t ai-rag-platform .
   ```

5. Start the app:

   ```bash
   docker run -d --name ai-rag-platform \
     -p 8000:8000 \
     --env-file .env \
     -v rag-data:/app/data \
     ai-rag-platform
   ```

   The named `rag-data` volume preserves the app's local document metadata
   across container restarts and replacements. The vector data itself is
   stored in Pinecone.

6. Configure `FRONTEND_URL=http://localhost:5173` and
   `FRONTEND_ORIGINS=http://localhost:5173` for local development. Run the
   frontend separately as described above. The API health check and interactive
   API docs are at [http://localhost:8000/health](http://localhost:8000/health)
   and [http://localhost:8000/docs](http://localhost:8000/docs).

To stop the container, run `docker stop ai-rag-platform`. Start it again with
`docker start ai-rag-platform`. To see startup logs, use
`docker logs -f ai-rag-platform`.

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
* ✅ Cognito authentication and per-user document isolation
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
