# 🔑 Getting Your Pinecone API Key

## Step-by-Step Guide

### 1. **Sign Up for Pinecone**

Go to: **https://app.pinecone.io/**

Click "Sign Up" (it's free!)

### 2. **Create Account**

You can sign up with:
- Google account (recommended - fastest)
- Email + password

### 3. **Get Your API Key**

After logging in:

1. Click on **"API Keys"** in the left sidebar
2. You'll see your API key displayed
3. Click **"Copy"** to copy it

### 4. **Add to Environment Variables**

#### **Option A: Add to `.env` file (Recommended)**

Create or edit `backend/.env` file:

```env
# Pinecone Configuration
PINECONE_API_KEY=your_api_key_here
PINECONE_INDEX_NAME=ousl-documents
PINECONE_DIMENSION=384
PINECONE_METRIC=cosine
PINECONE_CLOUD=aws
PINECONE_REGION=us-east-1
```

#### **Option B: Set in PowerShell (Temporary)**

```powershell
$env:PINECONE_API_KEY="your_api_key_here"
```

---

## 📊 Pinecone Free Tier

**What you get:**
- ✅ 1 serverless index
- ✅ Up to 100,000 vectors
- ✅ 2GB storage
- ✅ Unlimited queries
- ✅ No credit card required

**Perfect for:**
- Development and testing
- Small to medium document collections (500-1000 documents)
- OUSL's initial deployment

---

## 🔍 Verifying Your Setup

### Step 1: Check API Key

```powershell
cd "c:\Users\user\Desktop\OCT Project\ouslpms-monorepo\backend"
python -c "import os; print('API Key:', os.getenv('PINECONE_API_KEY', 'NOT SET'))"
```

Expected output:
```
API Key: pcsk_XXXXXX_XXXXXXXXXXXXXX
```

### Step 2: Run Setup Script

```powershell
python scripts/setup_pinecone.py
```

Expected output:
```
PINECONE INDEX SETUP
============================================
✓ API key found
✓ Index created/verified successfully
Total vectors: 0
SETUP COMPLETE!
```

### Step 3: Run Tests

```powershell
python scripts/test_pinecone.py
```

This will:
- Test connection
- Upload sample documents
- Test similarity search
- Verify everything works

---

## ⚠️ Common Issues

### Issue 1: "API key not found"

**Solution:**
```powershell
# Check if .env file exists
ls backend\.env

# If not, create it:
New-Item -Path "backend\.env" -ItemType File

# Add your API key:
Add-Content -Path "backend\.env" -Value "PINECONE_API_KEY=your_key_here"
```

### Issue 2: "Connection timeout"

**Solution:**
- Check internet connection
- Verify API key is correct
- Try a different region (us-west-2, eu-west-1)

### Issue 3: "Index already exists"

**Solution:**
- This is normal! Script will use existing index
- To recreate: Set `delete_if_exists=True` in setup script

---

## 📝 Sample `.env` File

```env
# FastAPI Backend
VITE_API_BASE=http://localhost:8000

# Firebase (existing)
FIREBASE_ADMIN_SDK_PATH=path/to/serviceAccountKey.json

# Pinecone Vector Database
PINECONE_API_KEY=pcsk_XXXXXX_XXXXXXXXXXXXXX
PINECONE_INDEX_NAME=ousl-documents
PINECONE_DIMENSION=384
PINECONE_METRIC=cosine
PINECONE_CLOUD=aws
PINECONE_REGION=us-east-1

# Groq AI (for Step 5)
GROQ_API_KEY=gsk_XXXXXXXXXXXXXX
```

---

## 🎯 Next Steps After Setup

1. ✅ API key obtained
2. ✅ Added to `.env` file
3. ✅ Run `setup_pinecone.py`
4. ✅ Run `test_pinecone.py`
5. ⏭️ Upload training documents
6. ⏭️ Test classification

---

## 💡 Tips

- **Keep API key secret**: Never commit `.env` to git
- **Use descriptive index names**: e.g., `ousl-documents-prod`, `ousl-documents-dev`
- **Monitor usage**: Check Pinecone dashboard for usage stats
- **Free tier limits**: 100K vectors is plenty for most use cases

---

## 📞 Need Help?

If you have issues:

1. **Check Pinecone status**: https://status.pinecone.io/
2. **Pinecone docs**: https://docs.pinecone.io/
3. **Contact support**: support@pinecone.io

---

**Ready to proceed?** Run the setup script!

```powershell
cd "c:\Users\user\Desktop\OCT Project\ouslpms-monorepo\backend"
python scripts/setup_pinecone.py
```
