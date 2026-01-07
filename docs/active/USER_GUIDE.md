# CiteWise RAG - User Guide

Complete guide to using the CiteWise RAG application interface.

## 📱 Application Overview

CiteWise RAG is a learning-focused Retrieval-Augmented Generation system with a simple web interface. The application has **three main tabs**:

1. **Chat** - Ask questions about your documents
2. **Documents** - Upload and manage documents
3. **Traces** - Debug and understand RAG queries

---

## 🏠 Tab 1: Chat (Main Interface)

**URL**: `http://localhost:3000/`

This is the main interface where you interact with your documents through questions.

### Interface Elements

#### Settings Panel (Top)

Located at the top of the page, allows you to configure RAG parameters:

**1. LLM Provider**

- **Groq (Llama 3.3 70B) ⚡** - Recommended, free, fast, high-quality
- **Ollama (Local)** - Runs locally, works offline, requires Ollama installed
- **OpenAI** - Requires paid API key, highest quality

**2. Embeddings Provider**

- **Local (Sentence Transformers)** - Free, runs locally, good quality
- **OpenAI** - Requires API key, slightly better quality

**3. Top-K Slider** (3-10)

- Controls how many document chunks to retrieve
- Higher = more context, but may include less relevant info
- Default: 5
- Recommended: 3-7

**Settings are saved automatically** in your browser's localStorage.

#### Chat Area (Center)

**Empty State:**

```
Ask a question about your documents
Upload documents first in the Documents tab
```

**User Messages:**

- Displayed on the right side
- Blue background
- Your questions appear here

**Assistant Messages:**

- Displayed on the left side
- Gray background
- Contains:
  - **Answer text** with inline citations like [1], [2]
  - **Sources section** with expandable citation cards
  - **Trace ID** and processing time at the bottom

**Citation Cards:**
Each citation shows:

- Document name
- Chunk index (which part of the document)
- Similarity score (how relevant it is)
- Full text of the cited chunk (click "More" to expand)

#### Input Area (Bottom)

- **Text input**: Type your question
- **Ask button**: Submit the question (or press Enter)
- Disabled while processing (shows loading animation)

### How to Use Chat

**Step 1: Upload Documents**
Go to Documents tab first and upload at least one document.

**Step 2: Configure Settings**

- Select **Groq** for best results (if you have API key)
- Keep **Local** embeddings (works great)
- Set **Top-K to 5** (default is good)

**Step 3: Ask Questions**
Type questions like:

- "What is Python?"
- "Explain Transformer architecture"
- "Compare Weaviate and ChromaDB"
- "How does RAG work?"

**Step 4: Review Answers**

- Read the answer with inline citations [1], [2], [3]
- Click on citation cards to see the source text
- Check similarity scores (higher = more relevant)
- Note the processing time

**Step 5: Follow-Up Questions**
Ask follow-up questions to dig deeper. Each question is independent (no conversation memory in v0.1).

### Example Interaction

**Question:**

```
How does self-attention work in Transformers?
```

**Answer:**

```
Self-attention allows the model to weigh the importance of different
words in a sequence when processing each word [1]. It computes three
vectors for each input: Query (Q), Key (K), and Value (V) [1]. The
attention score is calculated as Attention(Q, K, V) = softmax(QK^T /
sqrt(d_k)) * V [2].

Sources:
[1] transformer_architecture.md, Chunk 2, Score: 0.89
[2] transformer_architecture.md, Chunk 3, Score: 0.85
```

---

## 📄 Tab 2: Documents

**URL**: `http://localhost:3000/documents`

Manage your document library and upload new files.

### Interface Elements

#### Upload Section (Top)

**File Input:**

- Click "Choose File" to select a document
- Supported formats: `.txt`, `.md`
- Maximum size: No hard limit (but keep files reasonable)

**Upload Button:**

- Click "Upload" after selecting a file
- Shows progress indicator during upload
- Displays success/error message

**Upload Process:**

1. File is read and validated
2. Text is split into chunks (1000 characters, 200 overlap)
3. Each chunk is converted to embeddings
4. Embeddings are stored in Weaviate
5. Metadata is saved in PostgreSQL
6. Status updates to "completed"

#### Documents List (Center)

Displays all uploaded documents in cards:

**Each card shows:**

- **Filename** (e.g., `python_basics.md`)
- **File type** (e.g., `text/markdown`)
- **File size** (e.g., `15.2 KB`)
- **Upload date** (e.g., `2024-01-08 10:30 AM`)
- **Status badge**:
  - 🟢 **Completed** - Ready to query
  - 🟡 **Processing** - Being indexed
  - 🔴 **Failed** - Upload error
- **Chunk count** (e.g., `12 chunks`)

**Empty State:**

```
No documents uploaded yet
Upload your first document to get started!
```

### How to Use Documents

**Step 1: Prepare Your Documents**

- Save content as `.txt` or `.md` files
- Keep files focused on specific topics
- Use clear headings and structure

**Step 2: Upload**

1. Click "Choose File"
2. Select your document
3. Click "Upload"
4. Wait for "Processing..." → "Completed"

**Step 3: Verify**

- Check that status is "Completed"
- Note the chunk count (should be > 0)
- If failed, check file format and try again

**Step 4: Start Querying**
Go to Chat tab and ask questions!

### Tips for Better Results

**Document Quality:**

- ✅ Well-structured with headings
- ✅ Clear, concise writing
- ✅ Focused on specific topics
- ❌ Avoid very long paragraphs
- ❌ Avoid tables (not well-supported yet)

**Multiple Documents:**

- Upload related documents on the same topic
- RAG will search across all documents
- Citations will show which document was used

**Document Updates:**

- To update a document, upload a new version
- Old version remains (no deletion in v0.1)
- Consider using versioned filenames (e.g., `guide_v2.md`)

---

## 🔍 Tab 3: Traces

**URL**: `http://localhost:3000/traces`

Debug and understand how RAG queries are processed.

### Interface Elements

#### Traces List (Main View)

Displays all query traces in reverse chronological order (newest first).

**Each trace card shows:**

- **Query text** (the question asked)
- **Answer preview** (first 2 lines)
- **Metadata**:
  - LLM provider used (e.g., `groq`)
  - Embedding provider (e.g., `local`)
  - Top-K value (e.g., `5`)
  - Processing time in milliseconds
  - Timestamp

**Empty State:**

```
No traces found yet. Ask a question in the Chat tab!
```

#### Trace Details (Click on a Trace)

**URL**: `http://localhost:3000/traces/[trace-id]`

Shows complete details of a single query:

**1. Query Information**

- Original question
- Timestamp
- Processing time

**2. Retrieved Chunks**
Table showing all chunks retrieved from vector search:

- Rank (#1, #2, #3...)
- Document name
- Chunk index
- Similarity score (0-1, higher is better)
- Full chunk text

**3. Generated Answer**

- Complete answer text
- Inline citations

**4. Citations Used**

- Which chunks were actually cited in the answer
- May be fewer than retrieved chunks

**5. Configuration**

- LLM provider and model
- Embedding provider and model
- Top-K value

### How to Use Traces

**Use Case 1: Debugging Poor Answers**

If you get a bad answer:

1. Go to Traces tab
2. Find the query
3. Check retrieved chunks:
   - Are they relevant? (check similarity scores)
   - Do they contain the needed information?
4. Adjust Top-K if needed
5. Try different embedding provider

**Use Case 2: Understanding RAG Process**

To learn how RAG works:

1. Ask a simple question in Chat
2. Go to Traces and click on it
3. Observe:
   - How many chunks were retrieved
   - Which had highest similarity
   - Which chunks were cited
   - How long it took

**Use Case 3: Optimizing Performance**

To improve speed/quality:

1. Compare processing times across queries
2. Check if higher Top-K helps or hurts
3. Test different LLM providers
4. Identify slow queries

**Use Case 4: Verifying Citations**

To ensure accuracy:

1. Read the full answer
2. Click on trace
3. Verify each citation [1], [2], [3]
4. Read the actual chunk text
5. Confirm the answer matches the source

### Trace Metrics Explained

**Similarity Score (0-1):**

- 0.9-1.0: Excellent match
- 0.8-0.9: Very good match
- 0.7-0.8: Good match
- 0.6-0.7: Moderate match
- <0.6: Weak match

**Processing Time:**

- <1000ms: Very fast
- 1000-3000ms: Normal
- 3000-5000ms: Acceptable
- > 5000ms: Slow (check network/LLM)

**Top-K vs Retrieved:**

- Top-K: How many you requested
- Retrieved: How many were actually found
- May be less if not enough documents

---

## ⚙️ Settings & Configuration

### Application Settings

**Browser Settings (Saved Automatically):**

- LLM provider choice
- Embedding provider choice
- Top-K value

**Backend Settings (`.env` file):**

```bash
# LLM Configuration
LLM_PROVIDER=groq
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# Embedding Configuration
EMBEDDING_PROVIDER=local
LOCAL_EMBEDDING_MODEL=all-MiniLM-L6-v2

# RAG Parameters
DEFAULT_TOP_K=5
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
MAX_CHUNKS_PER_DOCUMENT=3
```

### Changing LLM Providers

**To use Groq (Recommended):**

1. Get free API key: https://console.groq.com/keys
2. Update `apps/ml/.env`:
   ```
   LLM_PROVIDER=groq
   GROQ_API_KEY=your_key_here
   ```
3. Restart FastAPI server
4. Select "Groq" in UI

**To use Ollama (Local):**

1. Install Ollama: https://ollama.com
2. Pull model: `ollama pull llama3.2`
3. Update `.env`: `LLM_PROVIDER=ollama`
4. Restart FastAPI
5. Select "Ollama" in UI

**To use OpenAI:**

1. Get API key: https://platform.openai.com/api-keys
2. Update `.env`:
   ```
   LLM_PROVIDER=openai
   OPENAI_API_KEY=your_key_here
   ```
3. Restart FastAPI
4. Select "OpenAI" in UI

---

## 🎯 Best Practices

### For Best Answers

1. **Upload Quality Documents**

   - Well-structured content
   - Clear headings
   - Focused topics

2. **Ask Specific Questions**

   - ❌ "Tell me about AI"
   - ✅ "How does self-attention work in Transformers?"

3. **Use Appropriate Top-K**

   - Simple questions: Top-K = 3
   - Complex questions: Top-K = 5-7
   - Very broad questions: Top-K = 10

4. **Choose Right LLM**

   - Learning: Groq (free, fast)
   - Offline work: Ollama
   - Best quality: OpenAI (paid)

5. **Review Citations**
   - Always check sources
   - Verify accuracy
   - Report if answer doesn't match sources

### For Learning RAG

1. **Start Simple**

   - Upload 1-2 documents
   - Ask basic questions
   - Review traces

2. **Experiment**

   - Try different Top-K values
   - Compare LLM providers
   - Test various question styles

3. **Understand the Pipeline**

   - Document → Chunks → Embeddings
   - Question → Embedding → Search
   - Retrieved Chunks → LLM → Answer

4. **Use Traces**
   - See what chunks were retrieved
   - Check similarity scores
   - Understand citation process

---

## 🐛 Troubleshooting

### "No documents uploaded yet"

- Go to Documents tab
- Upload at least one `.txt` or `.md` file
- Wait for "Completed" status

### "Not found in sources"

- Your documents don't contain the answer
- Try rephrasing the question
- Upload more relevant documents
- Increase Top-K value

### "Query processing failed"

- Check FastAPI is running (`http://localhost:8000/health`)
- Verify API keys in `.env` file
- Check terminal logs for errors
- Restart FastAPI server

### Empty or Short Answers

- Using Ollama? Try Groq instead
- Increase Top-K value
- Check if retrieved chunks are relevant (Traces tab)
- Verify documents contain the information

### Slow Responses

- Groq: Should be 2-4 seconds
- Ollama: 5-15 seconds (depends on hardware)
- OpenAI: 3-6 seconds
- Check internet connection
- Reduce Top-K if very slow

### Citations Don't Match Answer

- This is a bug - report it!
- Check trace to see actual chunks
- Verify LLM is following instructions

---

## 📊 Understanding the Interface

### Visual Indicators

**Status Badges:**

- 🟢 Green: Success, completed, healthy
- 🟡 Yellow: Processing, in progress
- 🔴 Red: Error, failed

**Loading States:**

- Animated dots: Processing query
- Spinner: Uploading file
- Disabled buttons: Action in progress

**Similarity Colors (in traces):**

- Dark green: >0.85 (excellent)
- Green: 0.75-0.85 (very good)
- Yellow: 0.65-0.75 (good)
- Orange: 0.55-0.65 (moderate)
- Red: <0.55 (weak)

### Navigation

**Header Links:**

- **CiteWise RAG v0.1** - Click to go home (Chat)
- **Chat** - Main interface
- **Documents** - Upload and manage
- **Traces** - Debug and analyze

**Footer:**

```
Learning > Features | Clarity > Abstraction | Control > Automation
```

Reminds you of the project philosophy.

---

## 🎓 Learning Exercises

### Exercise 1: Basic RAG

1. Upload `python_basics.md`
2. Ask: "What is Python?"
3. Review the answer and citations
4. Check trace to see retrieved chunks

### Exercise 2: Multi-Document Search

1. Upload multiple documents on related topics
2. Ask a question that spans topics
3. Observe which documents were cited
4. Check similarity scores

### Exercise 3: Top-K Experimentation

1. Ask the same question with Top-K=3
2. Ask again with Top-K=7
3. Ask again with Top-K=10
4. Compare answers and processing times

### Exercise 4: LLM Comparison

1. Ask a question with Groq
2. Ask the same question with Ollama
3. Compare answer quality and speed
4. Review traces for both

### Exercise 5: Citation Verification

1. Ask a complex question
2. Read the answer
3. Click on each citation
4. Verify the answer matches the sources

---

## 🚀 Next Steps

After mastering the basics:

1. **Read the Architecture Docs**

   - `docs/active/MVP_SCOPE.md`
   - `docs/active/DECISIONS.md`

2. **Explore the Code**

   - `apps/ml/` - FastAPI RAG service
   - `apps/web/` - Next.js UI

3. **Experiment with Settings**

   - Modify `config.py`
   - Change chunk size/overlap
   - Try different embedding models

4. **Contribute**
   - Report bugs
   - Suggest improvements
   - Add new features

---

## 📞 Getting Help

**Issues?**

- Check this guide first
- Review `README.md`
- Read `GROQ_SETUP.md` for API setup
- Check terminal logs for errors

**Questions?**

- This is a learning project
- Experiment and break things!
- Use Traces tab to understand what's happening

---

**Remember**: This is v0.1 - a learning tool, not a production system. Focus on understanding RAG concepts, not perfection! 🎓

Happy learning! 🚀
