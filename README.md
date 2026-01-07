# CiteWise RAG

A minimal RAG (Retrieval-Augmented Generation) system optimized for **learning and understanding** how RAG works end-to-end.

> **Philosophy**: Learning > Features | Clarity > Abstraction | Control > Automation

## 🎯 Learning Goals

Understand the complete RAG pipeline:

- Document ingestion → chunking → embedding
- Vector similarity search
- Prompt engineering with retrieved context
- Source citation and tracing

## 📖 Current Status: v0.1 (Basic RAG)

**What's included:**

- ✅ Simple document upload (TXT/MD)
- ✅ Vector search with Weaviate
- ✅ LLM answer generation with citations
- ✅ Query tracing for debugging

**Intentionally excluded:**

- ❌ GraphRAG / Neo4j (future learning)
- ❌ NestJS API layer (keeping it simple)
- ❌ Authentication & users
- ❌ Caching & optimization
- ❌ Production concerns

## 🏗️ Architecture

```
Document Upload → Chunking → Embeddings → Weaviate
                                              ↓
User Question → Embedding → Vector Search → Top-K Chunks
                                              ↓
                            LLM + Context → Answer + Citations
                                              ↓
                                        Query Trace (PostgreSQL)
```

**Components:**

- **Web UI**: Next.js (basic interface)
- **RAG Service**: FastAPI (all RAG logic)
- **Vector DB**: Weaviate
- **Metadata**: PostgreSQL (documents + traces)

## 📂 Project Structure

```
citewise-rag/
├── docs/
│   ├── active/              # Current v0.1 documentation
│   │   ├── DECISIONS.md     # Minimal architectural decisions
│   │   ├── MVP_SCOPE.md     # Learning-focused scope
│   │   └── QUICKSTART.md    # Getting started guide
│   └── reference/           # Future architecture ideas (GraphRAG, etc)
├── apps/
│   ├── web/                 # Next.js UI
│   └── ml/                  # FastAPI RAG service
├── infra/
│   ├── docker-compose.yml   # Weaviate + PostgreSQL
│   └── postgres/
│       └── init.sql         # Database schema
└── data/
    └── sample_docs/         # Test documents
```

## 🚀 Quick Start

### Option 1: Using Groq (Recommended - Free, Fast, Works Online)

```bash
# 1. Get free Groq API key
# Visit: https://console.groq.com/keys
# Sign up (no credit card required)
# Copy your API key

# 2. Start infrastructure
cd infra
docker-compose up -d

# 3. Setup FastAPI with Groq
cd apps/ml
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env file
echo "LLM_PROVIDER=groq" > .env
echo "GROQ_API_KEY=your_api_key_here" >> .env
echo "GROQ_MODEL=llama-3.3-70b-versatile" >> .env

uvicorn main:app --reload --port 8000

# 4. Start Next.js
cd apps/web
npm install
npm run dev
```

### Option 2: Using Ollama (Local, Offline)

```bash
# 1. Start infrastructure
cd infra
docker-compose up -d

# 2. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2

# 3. Start FastAPI
cd apps/ml
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# 4. Start Next.js
cd apps/web
npm install
npm run dev
```

Open http://localhost:3000

## 📝 Core Principles

1. **Answer ONLY from retrieved context** - no hallucination
2. **Every claim needs a citation** - traceable sources [1], [2]
3. **"Not found in sources"** - if info isn't in docs
4. **Traces must be debuggable** - understand every step

## 🔄 LLM Providers

**Supports multiple providers:**

- ⚡ **Groq** (recommended - free, fast, 70B models, works online) ⭐
- 🏠 **Ollama** (local, free, works offline)
- ☁️ **OpenAI** (highest quality, requires paid API key)

**Embeddings:**

- 🏠 **Sentence Transformers** (local, free, all-MiniLM-L6-v2)
- ☁️ **OpenAI Embeddings** (higher quality, text-embedding-3-small)

### Why Groq?

- ✅ **Free tier** - no credit card required
- ✅ **Fast inference** - faster than OpenAI
- ✅ **Large models** - Llama 3.1 70B, Mixtral 8x7B
- ✅ **Works for deployment** - perfect for Vercel/Railway
- ✅ **No local setup** - just API key

## 📚 Documentation

### User Guides

- **[USER_GUIDE.md](docs/active/USER_GUIDE.md)** - Complete interface guide with screenshots
- **[GROQ_SETUP.md](docs/active/GROQ_SETUP.md)** - How to get free Groq API key
- **[QUICKSTART.md](docs/active/QUICKSTART.md)** - Quick setup instructions

### Architecture

- **[MVP_SCOPE.md](docs/active/MVP_SCOPE.md)** - What's included in v0.1
- **[DECISIONS.md](docs/active/DECISIONS.md)** - Architectural decisions
- [`docs/reference/`](docs/reference/) - Advanced concepts (GraphRAG, etc.)

### Related Projects

- [`../rag-python-rag/`](../rag-python-rag/) - Simpler single-file RAG example

## 🛣️ Future Learning Phases

- **v0.2**: Add re-ranking, PDF support, streaming
- **v0.3**: Introduce GraphRAG with Neo4j
- **v0.4**: Multi-user, authentication
- **v0.5**: Production optimizations

---

**Note**: This is a learning project. Production deployment is explicitly out of scope for v0.1.

## 📖 Related Projects

- [`rag-python-rag/`](../rag-python-rag/) - Simple single-file RAG with ChromaDB + Ollama

## 📝 License

MIT
