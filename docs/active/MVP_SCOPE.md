# MVP Scope — CiteWise RAG (Learning-first)

## Goal

Build a minimal RAG system to understand the full pipeline end-to-end:
ingestion → chunking → retrieval → answer generation → citations.

This MVP is intentionally simple and optimized for learning, not for production.

---

## Must Have (v0.1)

### 1. Document Ingestion

- Upload `.txt` and `.md` files
- Parse raw text
- Split documents into chunks
- Generate embeddings for each chunk
- Store chunks + embeddings in a vector database

### 2. Retrieval-Augmented Generation

- Accept a user query
- Retrieve top-K relevant chunks from the vector database
- Assemble retrieved chunks into a context
- Generate an answer using an LLM
- Answer must be grounded ONLY in retrieved context

### 3. Source Citations

- Return a list of cited chunks for each answer
- Each citation must reference:
  - document title or source
  - chunk identifier
- Inline citation markers like [1], [2] are required

### 4. Basic Tracing

- Store for each query:
  - original question
  - retrieved chunk IDs and similarity scores
  - final answer text
  - citations
- Traces must be inspectable for debugging

---

## Out of Scope (NOT in v0.1)

- GraphRAG / Neo4j
- Authentication or users
- Multi-tenancy
- Redis or caching
- Re-ranking models
- PDF parsing
- Streaming responses
- Advanced UX or UI polish
- Production scaling or performance optimizations

---

## Success Criteria

The MVP is successful if:

- A document can be uploaded and indexed
- A user can ask questions about the document
- Answers include correct citations
- If information is not present in sources, the system responds with:
  “Not found in sources”
- Traces clearly show how the answer was produced
