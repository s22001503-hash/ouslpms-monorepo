# 🚀 Modal.com Deployment Guide

## Why Use Modal?

**Current Setup:**
- FastAPI runs on local machine (localhost:8000)
- Requires keeping your PC on 24/7
- No auto-scaling
- Manual restarts needed

**With Modal:**
- ✅ **Serverless** - No server management
- ✅ **Auto-scaling** - Handle 1 to 10,000+ requests/sec
- ✅ **Cold start** - Under 1 second
- ✅ **GPU support** - Optional GPU for faster inference
- ✅ **Free tier** - $30/month free credits
- ✅ **Built-in monitoring** - Logs, metrics, alerts

---

## 📋 Step-by-Step Deployment

### 1. Install Modal

```powershell
pip install modal
```

### 2. Setup Modal Account

```powershell
modal setup
```

This will:
- Open browser to create account
- Authenticate your CLI
- Create API token

### 3. Create Secrets in Modal Dashboard

Go to https://modal.com/secrets and create:

**Secret 1: `groq-api-key`**
```
GROQ_API_KEY=your_groq_api_key_here
```

**Secret 2: `pinecone-api-key`**
```
PINECONE_API_KEY=pcsk_2QcU2n_SrNgQBo6SGKjcGPBnSjyxDyLd1pN9MbGB1LYVp4hvhmWruYzeBAZrVVn619Wuco
PINECONE_INDEX_NAME=ousl-documents
```

### 4. Deploy to Modal

```powershell
cd "C:\Users\user\Desktop\OCT Project\ouslpms-monorepo\backend"
modal deploy modal_classifier.py
```

Output will show your endpoint URL:
```
✓ Created web function classify_document => https://yourorg--ousl-ai-classifier-classify-document.modal.run
```

### 5. Update File Watcher

Edit `services/print_job_watcher.py`:

**Line 53 - Change from:**
```python
GROQ_API_URL = "http://localhost:8000/ai/classify"
```

**To:**
```python
GROQ_API_URL = "https://yourorg--ousl-ai-classifier-classify-document.modal.run"
```

### 6. Test the Deployment

```powershell
# Test Modal endpoint
$body = @{text="This is an official university document"} | ConvertTo-Json
Invoke-WebRequest -Uri "https://yourorg--ousl-ai-classifier-classify-document.modal.run" -Method POST -Body $body -ContentType "application/json"
```

### 7. Restart File Watcher

```powershell
# Stop existing watcher
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force

# Start with new Modal endpoint
cd "C:\Users\user\Desktop\OCT Project\ouslpms-monorepo\backend"
Start-Process python -ArgumentList "services\print_job_watcher.py" -WindowStyle Hidden
```

---

## 💰 Cost Estimation

**Modal Pricing:**
- **CPU**: $0.000025/second ($0.0015/minute)
- **Memory**: $0.000003/GB/second
- **Free Tier**: $30/month credits

**Example Usage:**
- 1000 classifications/day
- 2 seconds per classification
- 2GB memory usage

**Cost = $0.09/day = $2.70/month** (well within free tier!)

---

## 🔧 Advanced Configuration

### Enable GPU (Optional)

For faster embedding generation:

```python
@app.function(
    gpu="T4",  # NVIDIA T4 GPU
    # ...
)
```

**GPU Pricing:** $0.0006/second (~$0.036/minute)

### Add Caching

Modal automatically caches:
- Docker image builds
- Model downloads
- Function code

Warm containers respond in <100ms!

### Monitor Performance

View in Modal dashboard:
- Request count
- Average latency
- Error rate
- Cost breakdown

---

## 🏗️ Architecture Comparison

### Before (Local FastAPI):
```
┌─────────────┐
│ PC (Always  │
│ Running)    │
│             │
│ ┌─────────┐ │
│ │ FastAPI │ │
│ │ :8000   │ │
│ └─────────┘ │
│             │
│ ┌─────────┐ │
│ │ File    │ │
│ │ Watcher │ │
│ └─────────┘ │
└─────────────┘
```

### After (Modal):
```
┌─────────────┐         ┌─────────────────┐
│ PC          │         │ Modal Cloud     │
│             │  HTTPS  │                 │
│ ┌─────────┐ │ ──────► │ ┌─────────────┐ │
│ │ File    │ │         │ │ Auto-scaling│ │
│ │ Watcher │ │         │ │ Classifier  │ │
│ └─────────┘ │         │ │             │ │
│             │         │ │ • Groq API  │ │
└─────────────┘         │ │ • Pinecone  │ │
                        │ │ • GPU (opt) │ │
                        │ └─────────────┘ │
                        └─────────────────┘
```

**Benefits:**
- ✅ PC can sleep/restart anytime
- ✅ Zero infrastructure management
- ✅ Scales automatically
- ✅ Better performance (cloud GPUs)
- ✅ Global CDN for low latency

---

## 🧪 Testing

### Test Endpoint Directly

```powershell
# Simple test
Invoke-WebRequest -Uri "https://your-modal-url.modal.run" `
  -Method POST `
  -Body '{"text":"Test document"}' `
  -ContentType "application/json"

# Full test with metadata
$body = @{
  text = "This is an official university document about course schedules"
  filename = "test.pdf"
  metadata = @{
    user = "testuser"
  }
} | ConvertTo-Json

Invoke-WebRequest -Uri "https://your-modal-url.modal.run" `
  -Method POST `
  -Body $body `
  -ContentType "application/json"
```

### Check Logs

```powershell
modal logs ousl-ai-classifier
```

---

## 🔒 Security Best Practices

1. **Never commit API keys** - Use Modal secrets only
2. **Enable HTTPS** - Modal provides this automatically
3. **Rate limiting** - Add in Modal config if needed
4. **Monitor costs** - Set alerts in Modal dashboard

---

## 🚨 Troubleshooting

### Cold Start Too Slow?
```python
container_idle_timeout=300  # Keep warm for 5 minutes
```

### Out of Memory?
```python
memory=2048  # Increase to 2GB
```

### Timeout Errors?
```python
timeout=600  # Increase to 10 minutes
```

### Check Deployment Status
```powershell
modal app list
modal app logs ousl-ai-classifier
```

---

## 📊 Next Steps

1. ✅ Deploy to Modal
2. ✅ Update file watcher URL
3. ✅ Test end-to-end
4. ⏭️ Monitor usage in dashboard
5. ⏭️ Add GPU if needed for performance
6. ⏭️ Set up alerts for errors

**You can now turn off your local FastAPI server!** The file watcher will use Modal's cloud endpoint instead.
