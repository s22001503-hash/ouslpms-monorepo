# AI Document Classifier - Quick Start Guide

## 🚀 STEP-BY-STEP SETUP

### ✅ Step 1: Packages Installed
All required packages are now installed:
- ✅ LangChain & LangChain Community
- ✅ ChromaDB
- ✅ sentence-transformers
- ✅ langchain-groq
- ✅ python-docx, pdfplumber, tiktoken

### 📝 Step 2: Get Groq API Key

1. Visit https://console.groq.com
2. Sign up or log in
3. Go to "API Keys" section
4. Click "Create API Key"
5. Copy the key

**Add to backend/.env file:**
```env
GROQ_API_KEY=gsk_your_api_key_here
```

### 📚 Step 3: Add Training Documents

You need **50-100 documents** in each category:

#### OFFICIAL Documents
**Location**: `training_documents/official/`

**What to add:**
- OUSL syllabi (PDF)
- Course outlines (PDF/DOCX)
- Transcripts (PDF)
- Official forms (PDF)
- Faculty announcements (PDF/DOCX)
- Degree certificates (PDF)
- Timetables (PDF/DOCX/TXT)

**Key requirement**: Each must contain "The Open University of Sri Lanka"

#### PERSONAL Documents
**Location**: `training_documents/personal/`

**What to add:**
- Novel chapters (PDF/TXT)
- Blog posts (TXT/DOCX)
- Personal letters (DOCX)
- Recipes (TXT)
- Travel logs (PDF/DOCX)
- Diary entries (TXT)
- Creative writing (PDF/DOCX/TXT)

**Key requirement**: Should NOT contain "The Open University of Sri Lanka"

### 🔧 Step 4: Train the Classifier

Once you have added documents (at least 10-20 in each folder to start):

```powershell
cd "C:\Users\user\Desktop\OCT project\ouslpms-monorepo\backend"
.\.venv\Scripts\Activate.ps1
python ai_classifier/train.py
```

**What happens:**
1. Loads all documents from folders
2. Extracts text from PDFs, DOCX, TXT
3. Creates embeddings using sentence-transformers
4. Stores in ChromaDB for similarity search

**Expected output:**
```
Loading OFFICIAL documents...
Loaded 75 OFFICIAL documents

Loading PERSONAL documents...
Loaded 68 PERSONAL documents

Adding documents to ChromaDB...
Total chunks in collection: 2847

TRAINING COMPLETE
```

### 🧪 Step 5: Test the Classifier

```powershell
cd "C:\Users\user\Desktop\OCT project\ouslpms-monorepo\backend"
.\.venv\Scripts\Activate.ps1
python ai_classifier/test_classifier.py
```

**What it tests:**
1. OFFICIAL OUSL document → Should classify as OFFICIAL
2. Personal letter → Should classify as PERSONAL
3. Edge case (mentions OUSL but not official) → Tests mandatory rule

### 🎯 Step 6: Integration Ready

Once testing passes, the classifier is ready to integrate with your print system!

**Basic usage:**
```python
from ai_classifier import DocumentClassifier, DocumentLoader

# Initialize once at startup
classifier = DocumentClassifier()

# When user uploads document
document_text = DocumentLoader.load_document(file_path)
result = classifier.classify_document(document_text)

# Check result
if result['classification'] == 'OFFICIAL':
    # Proceed with OFFICIAL document workflow
    confidence = result['confidence']
    boosters = result['boosters_count']
else:
    # Handle PERSONAL document
    pass
```

## 📊 Current Status

✅ **Completed:**
- Folder structure created
- All Python modules implemented
- Configuration files created
- Training script ready
- Test script ready
- README documentation created
- All packages installed

⏳ **Next Steps:**
1. Get Groq API key
2. Add training documents (50-100 each)
3. Run training script
4. Run test script
5. Integrate with print system API

## 🗂️ Project Structure

```
backend/
├── ai_classifier/
│   ├── __init__.py              ✅ Created
│   ├── config.py                ✅ Created
│   ├── document_loader.py       ✅ Created
│   ├── chroma_manager.py        ✅ Created
│   ├── classifier.py            ✅ Created
│   ├── train.py                 ✅ Created
│   ├── test_classifier.py       ✅ Created
│   ├── README.md                ✅ Created
│   └── chroma_db/               (auto-created during training)
│
training_documents/
├── official/                    ⏳ Add documents here
└── personal/                    ⏳ Add documents here
```

## ⚙️ Configuration

Edit `backend/ai_classifier/config.py` to customize:

**Chunking:**
```python
CHUNK_SIZE = 500              # characters per chunk
CHUNK_OVERLAP = 50            # overlap between chunks
```

**Classification:**
```python
BASE_CONFIDENCE = 0.80        # 80% base
BOOSTER_INCREMENT = 0.05      # +5% per booster
SIMILARITY_THRESHOLD = 0.70   # 70% minimum similarity
```

**Groq LLM:**
```python
GROQ_MODEL = "mixtral-8x7b-32768"
GROQ_TEMPERATURE = 0.1        # consistent classification
```

## 🔍 How It Works

### Two-Stage Classification:

**Stage 1: Semantic Search (ChromaDB)**
- Finds similar documents from training data
- Uses sentence-transformers for embeddings
- Flexible matching (handles variations, typos)

**Stage 2: Rule-Based Decision (Groq LLM)**
- Applies mandatory rule: Must contain "The Open University of Sri Lanka"
- Calculates confidence based on boosters
- Provides reasoning for decision

### Classification Rules:

1. **MANDATORY**: Document MUST have "The Open University of Sri Lanka"
   - If NOT found → **PERSONAL** (100%)
   - If found → **OFFICIAL** (continue to step 2)

2. **CONFIDENCE BOOSTERS** (each adds +5%):
   - Faculty name (+5%)
   - Degree programme (+5%)
   - Department name (+5%)
   - OUSL address (+5%)

3. **BASE CONFIDENCE**: 80%
   - With all 4 boosters: 100%

## 🆘 Troubleshooting

### "GROQ_API_KEY not found"
- Add key to `backend/.env` file
- Format: `GROQ_API_KEY=gsk_...`

### "No training documents found"
- Add at least 10-20 documents to `training_documents/official/` and `training_documents/personal/`
- Supported: PDF, DOCX, TXT

### Import errors
- All packages already installed
- If issues: `pip install -r requirements.txt`

### Low accuracy
- Add more training documents (aim for 50-100 each)
- Ensure OUSL phrase appears in official docs
- Check training data quality

## 📚 Documentation

Full documentation: `backend/ai_classifier/README.md`

**Key files:**
- `config.py` - Configuration settings
- `document_loader.py` - Load PDF/DOCX/TXT
- `chroma_manager.py` - ChromaDB operations
- `classifier.py` - Main classification logic
- `train.py` - Training script
- `test_classifier.py` - Testing script

## ✨ Next Action

**IMMEDIATELY**:
1. Get Groq API key from https://console.groq.com
2. Add to `backend/.env`: `GROQ_API_KEY=your_key_here`

**THEN**:
3. Add training documents to folders (start with 10-20 each, aim for 50-100)
4. Run training: `python ai_classifier/train.py`
5. Run tests: `python ai_classifier/test_classifier.py`

**You're all set to build AI document classification! 🎉**
