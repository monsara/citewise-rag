# Groq API Setup Guide

## Why Groq?

Groq provides **free, fast inference** for large language models like Llama 3.1 70B and Mixtral 8x7B. Perfect for:

- ✅ Development and learning
- ✅ Production deployments (Vercel, Railway, etc.)
- ✅ No credit card required
- ✅ Faster than OpenAI
- ✅ High-quality responses

## Getting Your Free API Key

### Step 1: Sign Up

1. Visit: https://console.groq.com/keys
2. Click "Sign Up" (or "Sign In" if you have an account)
3. Sign up with:
   - Google account (easiest)
   - GitHub account
   - Or email

**No credit card required!**

### Step 2: Create API Key

1. Once logged in, you'll see the "API Keys" page
2. Click "Create API Key"
3. Give it a name (e.g., "CiteWise RAG")
4. Click "Submit"
5. **Copy the API key immediately** (you won't see it again!)

Example key format: `gsk_...` (starts with `gsk_`)

### Step 3: Configure Your Project

#### For Local Development:

```bash
cd apps/ml

# Create .env file
cat > .env << EOF
LLM_PROVIDER=groq
GROQ_API_KEY=your_actual_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
EOF
```

#### For Production (Vercel/Railway):

Add environment variables in your hosting platform:

```
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_your_actual_key_here
GROQ_MODEL=llama-3.1-70b-versatile
```

## Available Models

Groq offers several free models:

### Recommended for RAG:

**llama-3.3-70b-versatile** ⭐ (Best quality, latest)
- 70 billion parameters
- Excellent reasoning
- Great for complex questions
- ~2-3 seconds response time

**llama-3.1-8b-instant** (Fastest)
- 8 billion parameters
- Very fast responses
- Good for simple queries
- ~0.5-1 second response time

**mixtral-8x7b-32768** (Long context)
- 47 billion parameters (8 experts)
- 32K token context window
- Good balance of speed and quality

### How to Switch Models:

In your `.env` file, change:

```bash
# For best quality (recommended)
GROQ_MODEL=llama-3.3-70b-versatile

# For fastest responses
GROQ_MODEL=llama-3.1-8b-instant

# For long documents
GROQ_MODEL=mixtral-8x7b-32768
```

## Testing Your Setup

### 1. Restart FastAPI Server

```bash
cd apps/ml
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

### 2. Test with curl

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is Python?",
    "llm_provider": "groq"
  }'
```

### 3. Test in UI

1. Open http://localhost:3000
2. Upload a document
3. Ask a question
4. Check the response quality!

## Rate Limits (Free Tier)

Groq's free tier is **very generous**:

- **Requests per minute**: 30
- **Requests per day**: 14,400
- **Tokens per minute**: 6,000

This is more than enough for:
- Learning and development
- Small production apps
- Personal projects

## Troubleshooting

### Error: "Invalid API Key"

- Check that your key starts with `gsk_`
- Make sure there are no extra spaces
- Verify the key is in `.env` file
- Restart the FastAPI server

### Error: "Rate limit exceeded"

- Wait 1 minute and try again
- Free tier: 30 requests/minute
- Consider caching responses

### Error: "Model not found"

- Check model name spelling
- Available models:
  - `llama-3.3-70b-versatile` (latest)
  - `llama-3.1-8b-instant`
  - `mixtral-8x7b-32768`

### Slow responses?

- Try `llama-3.1-8b-instant` for faster inference
- Check your internet connection
- Groq is usually faster than OpenAI

## Comparison: Groq vs Ollama vs OpenAI

| Feature | Groq | Ollama | OpenAI |
|---------|------|--------|--------|
| **Cost** | Free | Free | Paid ($) |
| **Setup** | API key only | Install locally | API key + payment |
| **Speed** | Very fast ⚡ | Depends on hardware | Fast |
| **Quality** | Excellent | Good | Excellent |
| **Offline** | ❌ No | ✅ Yes | ❌ No |
| **Deployment** | ✅ Easy | ❌ Complex | ✅ Easy |
| **Best For** | Production | Learning locally | Enterprise |

## Deployment Checklist

When deploying to Vercel/Railway/etc:

- [ ] Add `GROQ_API_KEY` to environment variables
- [ ] Set `LLM_PROVIDER=groq`
- [ ] Set `GROQ_MODEL=llama-3.3-70b-versatile`
- [ ] Test with a sample query
- [ ] Monitor usage in Groq console

## Getting Help

- **Groq Documentation**: https://console.groq.com/docs
- **Groq Discord**: https://discord.gg/groq
- **Rate limits**: https://console.groq.com/settings/limits

## Next Steps

1. ✅ Get your API key
2. ✅ Configure `.env`
3. ✅ Test locally
4. ✅ Upload documents
5. ✅ Ask questions and see the difference!

---

**Pro Tip**: Groq's Llama 3.1 70B gives **much better answers** than Ollama's Llama 3.2 (3B). You'll immediately notice:
- Longer, more detailed responses
- Better citations
- More accurate information
- Proper formatting

Enjoy your upgraded RAG system! 🚀
