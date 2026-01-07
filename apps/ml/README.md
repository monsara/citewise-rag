# CiteWise RAG - ML Service

FastAPI service that handles all RAG logic: document processing, embeddings, retrieval, and answer generation.

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your settings
```

## Configuration

Edit `.env` file:

```bash
# For local-only setup (no API keys needed)
LLM_PROVIDER=ollama
EMBEDDING_PROVIDER=local

# For OpenAI (faster, higher quality)
LLM_PROVIDER=openai
EMBEDDING_PROVIDER=openai
OPENAI_API_KEY=your-key-here
```

## Run

```bash
# Make sure infrastructure is running first
cd ../../infra
docker-compose up -d

# Start FastAPI
uvicorn main:app --reload --port 8000
```

API will be available at: http://localhost:8000

Docs: http://localhost:8000/docs

## Project Structure

```
ml/
├── main.py                    # FastAPI app
├── config.py                  # Configuration
├── models/
│   ├── embeddings.py         # Embedding providers
│   └── llm.py                # LLM providers
├── services/
│   ├── document_processor.py # Document upload & chunking
│   ├── vector_store.py       # Weaviate operations
│   ├── retriever.py          # Vector search
│   └── generator.py          # Answer generation
├── database/
│   └── postgres.py           # PostgreSQL operations
└── utils/
    ├── chunking.py           # Text splitting
    └── tracing.py            # Query tracing
```

## API Endpoints

### Documents

- `POST /documents/upload` - Upload TXT/MD file
- `GET /documents` - List all documents
- `GET /documents/{id}` - Get document details

### Query (Main RAG)

- `POST /query` - Ask a question
  ```json
  {
    "query": "What is Python?",
    "top_k": 5,
    "llm_provider": "ollama",
    "embedding_provider": "local"
  }
  ```

### Tracing

- `GET /traces` - List recent queries
- `GET /traces/{id}` - Get query trace details

### Health

- `GET /health` - Health check
- `GET /` - API info

## Testing

```bash
# Test document upload
curl -X POST "http://localhost:8000/documents/upload" \
  -F "file=@test.txt"

# Test query
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is this document about?"}'
```
