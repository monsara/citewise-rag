# Deploy to Render - Complete Guide

This guide will help you deploy CiteWise RAG to Render for free.

## 🎯 What You'll Get

- ✅ **Live URL**: `https://citewise-web.onrender.com`
- ✅ **All features working**: Chat, Documents, Traces
- ✅ **Groq API**: Fast, free LLM responses
- ✅ **PostgreSQL**: Free 1GB database
- ✅ **Weaviate**: Vector search
- ✅ **Cost**: $0/month (free tier)

## ⚠️ Free Tier Limitations

- **Sleeps after 15 minutes** of inactivity
- **First request takes 30-60 seconds** to wake up
- **Limited resources**: 512MB RAM per service
- **Good for**: Testing, portfolio, demos
- **Not for**: Production with high traffic

---

## 📋 Prerequisites

1. ✅ GitHub account with repo: https://github.com/monsara/citewise-rag
2. ✅ Render account: https://render.com (sign up with GitHub)
3. ✅ Groq API key: https://console.groq.com/keys

---

## 🚀 Deployment Steps

### Step 1: Sign Up on Render

1. Go to https://render.com
2. Click **"Get Started"**
3. Sign up with **GitHub** (easiest)
4. Authorize Render to access your repositories

### Step 2: Create New Blueprint

1. Click **"New +"** → **"Blueprint"**
2. Connect your GitHub repository: `monsara/citewise-rag`
3. Render will detect `render.yaml` automatically
4. Click **"Apply"**

### Step 3: Configure Environment Variables

Render will create 3 services:
- `citewise-postgres` (database)
- `citewise-weaviate` (vector DB)
- `citewise-api` (backend)
- `citewise-web` (frontend)

**Important:** Add your Groq API key:

1. Go to **citewise-api** service
2. Click **"Environment"**
3. Find `GROQ_API_KEY`
4. Click **"Generate Value"** → Paste your key: `gsk_...`
5. Click **"Save Changes"**

### Step 4: Wait for Deployment

- **PostgreSQL**: ~2 minutes
- **Weaviate**: ~3 minutes
- **Backend API**: ~5 minutes (installs Python packages)
- **Frontend**: ~3 minutes

**Total time**: ~10-15 minutes

### Step 5: Verify Deployment

1. **Check Backend Health:**
   - Go to `citewise-api` service
   - Click on the URL (e.g., `https://citewise-api-xxx.onrender.com`)
   - Add `/health` to URL
   - Should see: `{"status":"healthy","database":"connected"}`

2. **Check Frontend:**
   - Go to `citewise-web` service
   - Click on the URL (e.g., `https://citewise-web-xxx.onrender.com`)
   - Should see the CiteWise RAG interface

### Step 6: Upload Documents & Test

1. Go to **Documents** tab
2. Upload a test document (e.g., `python_basics.md`)
3. Wait for "Completed" status
4. Go to **Chat** tab
5. Ask a question: "What is Python?"
6. Verify you get an answer with citations

---

## 🔧 Troubleshooting

### "Service Unavailable" or 502 Error

**Cause**: Service is sleeping (free tier)

**Solution**: Wait 30-60 seconds and refresh. First request wakes it up.

### "Query processing failed"

**Possible causes:**

1. **Groq API key not set**
   - Go to `citewise-api` → Environment
   - Add `GROQ_API_KEY`
   - Redeploy

2. **Weaviate not ready**
   - Check `citewise-weaviate` service status
   - Wait for it to be "Live"
   - Restart `citewise-api` if needed

3. **PostgreSQL connection failed**
   - Check `citewise-postgres` database status
   - Verify connection string is auto-configured

### Documents Not Uploading

**Check:**
1. Backend API is running (`/health` endpoint works)
2. Weaviate is running
3. Check backend logs for errors

### Slow Performance

**Expected on free tier:**
- First request: 30-60 seconds (waking up)
- Subsequent requests: 2-5 seconds
- After 15 min inactivity: sleeps again

**To improve:**
- Upgrade to paid plan ($7/month per service)
- Services stay awake 24/7
- More RAM and CPU

---

## 📊 Monitoring Your Deployment

### View Logs

1. Go to service (e.g., `citewise-api`)
2. Click **"Logs"** tab
3. See real-time logs
4. Look for errors or warnings

### Check Metrics

1. Go to service
2. Click **"Metrics"** tab
3. See:
   - CPU usage
   - Memory usage
   - Request count
   - Response times

### Database Usage

1. Go to `citewise-postgres`
2. Click **"Info"** tab
3. See:
   - Storage used (max 1GB free)
   - Connection count
   - Queries per second

---

## 🔄 Updating Your Deployment

### Automatic Updates (Recommended)

Render auto-deploys when you push to GitHub:

```bash
# Make changes locally
git add .
git commit -m "Update feature X"
git push origin main

# Render automatically redeploys (2-5 minutes)
```

### Manual Redeploy

1. Go to service
2. Click **"Manual Deploy"**
3. Select branch: `main`
4. Click **"Deploy"**

---

## 💰 Cost Breakdown

### Free Tier (Current Setup)

| Service | Plan | Cost | Limits |
|---------|------|------|--------|
| PostgreSQL | Free | $0 | 1GB storage, sleeps |
| Weaviate | Free Web Service | $0 | 512MB RAM, sleeps |
| Backend API | Free Web Service | $0 | 512MB RAM, sleeps |
| Frontend | Free Web Service | $0 | 512MB RAM, sleeps |
| **Total** | | **$0/month** | |

### Paid Tier (If You Upgrade)

| Service | Plan | Cost | Benefits |
|---------|------|------|----------|
| PostgreSQL | Starter | $7/mo | 10GB, no sleep |
| Weaviate | Starter | $7/mo | 2GB RAM, no sleep |
| Backend API | Starter | $7/mo | 2GB RAM, no sleep |
| Frontend | Starter | $7/mo | 2GB RAM, no sleep |
| **Total** | | **$28/month** | Always on, faster |

---

## 🌐 Custom Domain (Optional)

### Add Your Domain

1. Go to `citewise-web` service
2. Click **"Settings"** → **"Custom Domain"**
3. Add your domain (e.g., `citewise-rag.com`)
4. Follow DNS instructions
5. Wait for SSL certificate (automatic)

**Cost**: Free (just domain registration ~$10/year)

---

## 🔒 Security Best Practices

### 1. Protect Your API Keys

- ✅ Never commit `.env` files
- ✅ Use Render's environment variables
- ✅ Rotate keys periodically

### 2. Database Security

- ✅ Render auto-generates secure passwords
- ✅ Connections are encrypted (SSL)
- ✅ Database is not publicly accessible

### 3. CORS Configuration

Current setup allows all origins (`*`). For production:

1. Edit `apps/ml/config.py`
2. Change `CORS_ORIGINS` to your frontend URL
3. Redeploy

---

## 📈 Scaling Tips

### When to Upgrade

Upgrade if you experience:
- ❌ Frequent timeouts
- ❌ Slow responses (>10 seconds)
- ❌ "Out of memory" errors
- ❌ Database storage full

### What to Upgrade First

1. **Backend API** - Most resource-intensive (embeddings, LLM calls)
2. **Weaviate** - If you have many documents
3. **PostgreSQL** - If you have lots of traces
4. **Frontend** - Usually fine on free tier

---

## 🆘 Getting Help

### Render Support

- **Docs**: https://render.com/docs
- **Community**: https://community.render.com
- **Status**: https://status.render.com

### Project Issues

- **GitHub Issues**: https://github.com/monsara/citewise-rag/issues
- **Documentation**: See `docs/active/USER_GUIDE.md`

---

## ✅ Deployment Checklist

Before going live:

- [ ] GitHub repo is public and up-to-date
- [ ] `render.yaml` is in root directory
- [ ] Groq API key is added to environment
- [ ] All services are "Live" (green status)
- [ ] Backend `/health` endpoint returns 200
- [ ] Frontend loads correctly
- [ ] Can upload a document
- [ ] Can query and get answers with citations
- [ ] Traces are being recorded

---

## 🎉 Success!

Your CiteWise RAG is now live! 🚀

**Share your deployment:**
- Add URL to GitHub README
- Share with friends/portfolio
- Tweet about it!

**Next steps:**
- Upload your AI/ML documents
- Test with different questions
- Explore the Traces tab
- Consider upgrading for better performance

---

## 📝 Example URLs

After deployment, you'll have:

- **Frontend**: `https://citewise-web-xxx.onrender.com`
- **Backend API**: `https://citewise-api-xxx.onrender.com`
- **Health Check**: `https://citewise-api-xxx.onrender.com/health`
- **API Docs**: `https://citewise-api-xxx.onrender.com/docs`

Replace `xxx` with your actual service hash.

---

**Happy deploying!** 🎊
