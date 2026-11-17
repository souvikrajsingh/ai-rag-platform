# AI RAG Platform

A multi-user Retrieval-Augmented Generation (RAG) application built with
FastAPI, Pinecone, and Google Gemini. It accepts PDF uploads, indexes the
extracted text per authenticated user, retrieves relevant context, and produces
answers grounded in the uploaded documents.

The API is designed to be used with the separately maintained
[AI RAG Frontend](https://github.com/souvikrajsingh/ai-rag-frontend).

## Features

- PDF ingestion and text chunking
- Pinecone serverless vector storage with integrated embeddings
- Cognito OIDC authentication
- Per-user Pinecone namespaces and upload manifests
- Context-aware Gemini answers with source metadata
- FastAPI health, document, ingestion, and query endpoints
- Interactive Swagger documentation
- Docker deployment support
- CORS and secure session-cookie configuration

## Architecture

```text
Browser / Frontend
        |
        | OIDC login, session cookie, JSON / multipart requests
        v
FastAPI API
  |-- Authentication (Amazon Cognito)
  |-- PDF ingestion
  |-- Text splitting
  |-- Pinecone vector search
  `-- Gemini response generation
        |
        v
Pinecone index + local per-user upload manifests
```

Each Cognito `sub` maps to a dedicated Pinecone namespace. A user's document
list, duplicate detection, uploads, and searches are isolated from all other
users.

## Project Structure

```text
src/app/
├── api/
│   ├── auth.py
│   ├── dependencies.py
│   ├── main.py
│   ├── route.py
│   └── schemas.py
├── config/
│   └── settings.py
├── ingestion/
│   ├── document_loader.py
│   ├── ingestion_service.py
│   └── text_splitter.py
├── llm/
│   ├── llm_manager.py
│   └── prompt_builder.py
├── retrieval/
│   └── vector_store.py
├── services/
│   └── rag_service.py
└── util/
    └── hash_manager.py

scripts/
├── test_hash_manager.py
└── test_loader.py

data/
└── user_uploads/       # Created at runtime; ignored by Git

Dockerfile
pyproject.toml
uv.lock
```

## Requirements

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)
- A Google Gemini API key
- A Pinecone API key and index
- An Amazon Cognito user pool and app client
- Docker, if you prefer the container workflow

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/souvikrajsingh/ai-rag-platform.git
cd ai-rag-platform
```

### 2. Install dependencies

```bash
uv sync --locked
```

### 3. Configure environment variables

Create a `.env` file in the repository root:

```env
gemini_api_key=your_gemini_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=ai-rag-platform
PINECONE_EMBEDDING_MODEL=llama-text-embed-v2

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

Generate a stable session secret with:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Keep `.env` private. `.env`, local upload manifests, caches, and virtual
environments are excluded from Git.

### 4. Configure the Pinecone index

Create a serverless index named `PINECONE_INDEX_NAME` with the integrated
`llama-text-embed-v2` embedding model. The recommended creation settings are:

- Cloud: AWS
- Region: `us-east-1`
- Index name: `ai-rag-platform`
- Embedding model: `llama-text-embed-v2`
- Metric: cosine

The API upserts text records and asks Pinecone to embed and search them; it
does not run a local embedding model.

### 5. Configure Cognito

In the Cognito app client:

- Enable the authorization code grant
- Enable `openid`, `email`, and `phone` scopes
- Enable self-service sign-up if account creation should be available
- Add `http://localhost:8000/auth/callback` as an allowed callback URL

Set `AWS_REGION` to the region containing the user pool. Register the deployed
backend callback URL in Cognito for hosted deployments.

For HTTPS cross-origin deployments, use:

```env
SESSION_COOKIE_SECURE=true
SESSION_COOKIE_SAME_SITE=none
FRONTEND_URL=https://your-frontend.example
FRONTEND_ORIGINS=https://your-frontend.example
```

`FRONTEND_ORIGINS` accepts a comma-separated list of exact allowed origins.

## Running the API

Start the backend from the repository root:

```bash
uv run uvicorn src.app.api.main:app --reload
```

Available local URLs:

- Frontend redirect: `http://localhost:8000/`
- Health: `http://localhost:8000/health`
- Swagger: `http://localhost:8000/docs`
- Cognito login: `http://localhost:8000/login`
- Cognito sign-up: `http://localhost:8000/signup`

## Running the Frontend

Clone the frontend into a separate directory:

```bash
git clone https://github.com/souvikrajsingh/ai-rag-frontend.git
cd ai-rag-frontend
npm ci
npm run dev
```

Open the URL printed by Vite, normally `http://localhost:5173`. The frontend
handles sign-in and redirects authenticated users to `/chat`.

## API Endpoints

All document and query endpoints require an authenticated session.

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/health` | API health check |
| `GET` | `/documents` | List the user's uploaded filenames |
| `POST` | `/ingest` | Upload and index a PDF |
| `POST` | `/query` | Ask a question about indexed PDFs |
| `GET` | `/login` | Start Cognito OIDC sign-in |
| `GET` | `/signup` | Start Cognito sign-up |
| `GET` | `/logout` | Clear the local session |

Example query:

```bash
curl -b cookies.txt \
  -H "Content-Type: application/json" \
  -d '{"question":"Explain what embeddings are."}' \
  http://localhost:8000/query
```

Example response:

```json
{
  "answer": "Embeddings are numeric representations...",
  "sources": [
    {
      "source": "python-overview.pdf",
      "page": 10
    }
  ]
}
```

Only PDF files with extractable text are supported. Scanned PDFs require OCR
before ingestion.

## Running with Docker

Create `.env` first, then build and run the backend:

```bash
docker build -t ai-rag-platform .
docker run -d --name ai-rag-platform \
  -p 8000:8000 \
  --env-file .env \
  -v rag-data:/app/data \
  ai-rag-platform
```

The named `rag-data` volume preserves local per-user upload manifests. Pinecone
stores the vector data. Stop and restart the container with:

```bash
docker stop ai-rag-platform
docker start ai-rag-platform
docker logs -f ai-rag-platform
```

The Docker image uses `${PORT:-8000}` for its listening port. On platforms that
require port `10000`, set `PORT=10000` at runtime.

## Utility Scripts

Run the hash manager check:

```bash
uv run python scripts/test_hash_manager.py
```

To run the direct LLM query example, set `COGNITO_USER_SUB` and execute:

```bash
COGNITO_USER_SUB="your-cognito-sub" uv run python scripts/test_loader.py
```

## Testing

There is currently no formal pytest suite. Run the utility scripts and API
health, authentication, ingestion, and query flows when validating a change.

## Security

- Never commit `.env` or provider credentials
- Rotate any API key that has been exposed or committed
- Use a unique, stable session secret in production
- Enable HTTPS and secure cookies for deployed environments
- Register only trusted frontend origins in `FRONTEND_ORIGINS`

## Tech Stack

- Python 3.14
- FastAPI
- Pydantic Settings
- Authlib
- Amazon Cognito OIDC
- LangChain
- Google Gemini
- Pinecone integrated embeddings
- Docker
- uv

## License

This project is intended for learning and educational purposes.
