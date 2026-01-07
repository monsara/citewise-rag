# Quick Start Guide - CiteWise RAG v0.1

Get the RAG system running in 4 steps.

## Prerequisites

- Python 3.9+
- Node.js 18+
- Docker & Docker Compose
- Ollama (for local LLM)

## Step 1: Start Infrastructure

Start PostgreSQL and Weaviate:

```bash
cd infra
docker-compose up -d

# Check services are running
docker-compose ps
```

You should see `citewise-postgres` and `citewise-weaviate` running.

## Step 2: Install Ollama (Optional, for local LLM)

### macOS / Linux

```bash
curl -fsSL https://ollama.com/install.sh | sh

# Download model
ollama pull llama3.2
```

### Verify Installation

```bash
ollama list
# Should show llama3.2
```

**Skip this if using OpenAI API only.**

## Step 3: Start FastAPI Backend

```bash
cd apps/ml

# Create virtual environment
python -m venv venv

# Activate
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env if needed (optional)
# For local-only setup, defaults are fine
# For OpenAI, add your API key

# Start server
uvicorn main:app --reload --port 8000
```

FastAPI will start at: **http://localhost:8000**

API docs: **http://localhost:8000/docs**

## Step 4: Start Next.js Frontend

```bash
# In a NEW terminal
cd apps/web

# Install dependencies
npm install

# Copy environment template
cp .env.local.example .env.local

# Edit if needed (defaults are fine for local)

# Start dev server
npm run dev
```

Next.js will start at: **http://localhost:3000**

## Usage

### 1. Upload a Document

1. Go to http://localhost:3000/documents
2. Upload a `.txt` or `.md` file
3. Wait for processing (should take 10-30 seconds)

### 2. Ask Questions

1. Go to http://localhost:3000 (Chat tab)
2. Type a question about your document
3. Get answer with source citations!

### 3. Inspect Traces

1. Go to http://localhost:3000/traces
2. Click on any query to see:
   - Retrieved chunks
   - Similarity scores
   - Full answer
   - Processing time

## Troubleshooting

### Backend fails to start

**Check database connection:**
```bash
docker-compose ps
# Make sure postgres and weaviate are up
```

**Check logs:**
```bash
cd apps/ml
python -c "from database.postgres import execute_query; execute_query('SELECT 1')"
```

### Ollama not found

If using local LLM:
```bash
ollama serve
```

Or switch to OpenAI in `.env`:
```
LLM_PROVIDER=openai
OPENAI_API_KEY=your-key-here
```

### Frontend can't reach backend

Check `apps/web/.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Test backend directly:
```bash
curl http://localhost:8000/health
```

### Embeddings are slow

Local embeddings download ~80MB model on first run.

To speed up, use OpenAI embeddings:
```
EMBEDDING_PROVIDER=openai
OPENAI_API_KEY=your-key-here
```

## Testing the System

### Test 1: Upload Sample Document

Create `test.txt`:
```
Python is a high-level programming language.
It was created by Guido van Rossum in 1991.
Python emphasizes code readability.
```

Upload via UI or curl:
```bash
curl -X POST http://localhost:8000/documents/upload \
  -F "file=@test.txt"
```

### Test 2: Query

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Who created Python?"}'
```

Expected answer: "Guido van Rossum [1]"

### Test 3: Provider Switching

In the UI settings panel:
- Switch LLM: Ollama ↔ OpenAI
- Switch Embeddings: Local ↔ OpenAI
- Try different combinations

## Next Steps

1. **Upload more documents** - Try PDFs (coming in v0.2)
2. **Experiment with parameters** - Adjust Top-K, try different providers
3. **Read traces** - Learn how RAG works by inspecting traces
4. **Check docs** - Read `docs/active/DECISIONS.md` and `MVP_SCOPE.md`

## Stopping the System

```bash
# Stop Next.js (Ctrl+C in terminal)
# Stop FastAPI (Ctrl+C in terminal)

# Stop infrastructure
cd infra
docker-compose down

# (Optional) Remove data
docker-compose down -v
```

## Getting Help

- Check logs in terminal where services are running
- Visit API docs: http://localhost:8000/docs
- Review traces in UI for debugging
- Read `docs/active/` for architecture details
