# AI Document Classifier for OUSL Print Management System

## Overview

This AI document classifier uses a **RAG (Retrieval-Augmented Generation)** approach to classify documents as either **OFFICIAL** (OUSL-related) or **PERSONAL** based on content analysis.

### Architecture

```
┌─────────────────┐
│  New Document   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  1. CHECK MANDATORY REQUIREMENT     │
│  "The Open University of Sri Lanka" │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  2. SEMANTIC SEARCH (ChromaDB)      │
│  Find similar training documents    │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  3. CONFIDENCE BOOSTERS             │
│  Faculty, Programme, Department...  │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  4. GROQ LLM DECISION               │
│  Final classification with context  │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  OFFICIAL or    │
│  PERSONAL       │
│  + Confidence   │
└─────────────────┘
```

## Technology Stack

- **ChromaDB**: Vector database for document embeddings
- **sentence-transformers**: Local embedding model (all-MiniLM-L6-v2)
- **LangChain**: RAG pipeline orchestration
- **Groq**: Fast LLM inference (Mixtral-8x7b or Llama-3)
- **Document Loaders**: pypdf2, python-docx, pdfplumber

## Classification Rules

### Mandatory Rule

✅ **MUST contain**: "The Open University of Sri Lanka" or "THE OPEN UNIVERSITY OF SRI LANKA"

- If **NOT found** → **PERSONAL** (regardless of other content)
- If **found** → **OFFICIAL** (proceed to confidence calculation)

### Confidence Boosters (Optional)

Each major booster found adds **+5%** to base confidence of **80%**:

1. **Faculty** (e.g., Faculty of Engineering Technology)
2. **Degree Programme** (e.g., Bachelor of Technology Honours)
3. **Department** (e.g., Department of Electrical and Computer Engineering)
4. **OUSL Address** (Nawala, Nugegoda, Sri Lanka)

**Examples**:
- Mandatory phrase only: **80%** confidence
- + Faculty: **85%**
- + Programme: **90%**
- + Department: **95%**
- + Address: **100%**

## Project Structure

```
backend/
├── ai_classifier/
│   ├── __init__.py              # Module initialization
│   ├── config.py                # Configuration settings
│   ├── document_loader.py       # Load PDF/DOCX/TXT files
│   ├── chroma_manager.py        # ChromaDB operations
│   ├── classifier.py            # Main classification logic
│   ├── train.py                 # Training script
│   ├── test_classifier.py       # Test script
│   └── chroma_db/               # ChromaDB storage (auto-created)
│
training_documents/
├── official/                    # OUSL official documents (50-100)
│   ├── syllabus_1.pdf
│   ├── transcript_sample.pdf
│   └── course_outline.docx
│
└── personal/                    # Personal documents (50-100)
    ├── novel_chapter.pdf
    ├── personal_letter.docx
    └── blog_post.txt
```

## Setup Instructions

### Step 1: Install Dependencies

All required packages are in `requirements.txt`:

```bash
cd backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables

Create/update `backend/.env`:

```env
# Groq API Key (required for classification)
GROQ_API_KEY=your_groq_api_key_here
```

**Get Groq API Key**:
1. Visit https://console.groq.com
2. Sign up / Log in
3. Go to API Keys section
4. Create new API key
5. Copy and paste into `.env`

### Step 3: Prepare Training Documents

Add training documents to folders:

#### Official Documents (50-100 recommended)
- Syllabi
- Course outlines
- Transcripts
- Official forms
- Faculty announcements
- Degree certificates
- Timetables

**Location**: `training_documents/official/`

#### Personal Documents (50-100 recommended)
- Novel chapters
- Blog posts
- Personal letters
- Recipes
- Travel logs
- Diary entries
- Creative writing

**Location**: `training_documents/personal/`

**Supported formats**: `.pdf`, `.docx`, `.txt`

### Step 4: Train the Classifier

Run the training script to ingest documents into ChromaDB:

```bash
cd backend
.\.venv\Scripts\Activate.ps1
python ai_classifier/train.py
```

**What happens**:
1. Loads all documents from `official/` and `personal/` folders
2. Extracts text from PDFs, DOCX, TXT files
3. Chunks text into 500-character segments (50 char overlap)
4. Generates embeddings using sentence-transformers
5. Stores in ChromaDB for similarity search

**Expected output**:
```
Loading OFFICIAL documents...
Loaded 75 OFFICIAL documents

Loading PERSONAL documents...
Loaded 68 PERSONAL documents

Adding documents to ChromaDB...
Total chunks in collection: 2847
Label distribution: {'OFFICIAL': 1523, 'PERSONAL': 1324}

TRAINING COMPLETE
```

### Step 5: Test the Classifier

Run the test script to verify classification:

```bash
cd backend
.\.venv\Scripts\Activate.ps1
python ai_classifier/test_classifier.py
```

**Expected output**:
```
TEST 1: OFFICIAL OUSL DOCUMENT
RESULT: OFFICIAL (95%)
REASONING: Document contains mandatory OUSL phrase and multiple boosters

TEST 2: PERSONAL DOCUMENT
RESULT: PERSONAL (85%)
REASONING: No mandatory OUSL phrase found

TEST 3: EDGE CASE
RESULT: OFFICIAL (80%)
REASONING: Mandatory phrase found but no additional boosters
```

## Usage Examples

### Basic Classification

```python
from ai_classifier import DocumentClassifier

# Initialize classifier
classifier = DocumentClassifier()

# Classify a document
result = classifier.classify_document(document_text)

print(f"Classification: {result['classification']}")
print(f"Confidence: {result['confidence']:.0%}")
print(f"Reasoning: {result['reasoning']}")
```

### Classification Result Format

```python
{
    'classification': 'OFFICIAL',  # or 'PERSONAL'
    'confidence': 0.95,            # 0.0 to 1.0
    'reasoning': 'Document contains mandatory OUSL phrase...',
    'mandatory_found': True,
    'boosters': {
        'faculty': ['Faculty of Engineering Technology'],
        'programme': ['Bachelor of Technology Honours'],
        'department': [],
        'address': ['Nawala, Nugegoda']
    },
    'boosters_count': 3,
    'suggested_confidence': 0.95,
    'similar_documents_count': 5
}
```

### Integration with Print System

```python
from ai_classifier import DocumentClassifier, DocumentLoader

# Initialize classifier (once at startup)
classifier = DocumentClassifier()

# When user uploads document for printing
def handle_print_request(file_path):
    # Load document
    document_text = DocumentLoader.load_document(file_path)
    
    # Classify
    result = classifier.classify_document(document_text)
    
    if result['classification'] == 'OFFICIAL':
        # Check policy limits
        if user.official_pages_used >= user.official_pages_limit:
            show_policy_violation_dialog()
        else:
            show_print_confirmation_dialog(result)
    else:
        # PERSONAL document
        show_personal_document_alert()
```

## Configuration

Edit `ai_classifier/config.py` to customize:

### Document Processing
```python
CHUNK_SIZE = 500              # characters per chunk
CHUNK_OVERLAP = 50            # overlap between chunks
MAX_CHUNKS_PER_DOC = 20       # limit chunks per document
```

### Classification Rules
```python
MANDATORY_PHRASE = "The Open University of Sri Lanka"
BASE_CONFIDENCE = 0.80        # 80% base confidence
BOOSTER_INCREMENT = 0.05      # +5% per booster
```

### Similarity Search
```python
SIMILARITY_THRESHOLD = 0.70   # minimum similarity (0-1)
TOP_K_RESULTS = 5             # number of similar docs to retrieve
```

### Groq LLM
```python
GROQ_MODEL = "mixtral-8x7b-32768"  # or "llama-3.1-70b-versatile"
GROQ_TEMPERATURE = 0.1        # low for consistent classification
GROQ_MAX_TOKENS = 500
```

## How It Works

### 1. Semantic Search (ChromaDB)

- Finds similar documents **without strict rules**
- Uses **sentence-transformers** for embeddings
- Handles variations, typos, context
- More flexible than keyword matching

**Example**: Query "university transcript" might find:
- "academic record from OUSL" (semantic similarity)
- "degree certificate issued by..." (context similarity)

### 2. Rule-Based Decision (Groq LLM)

- Applies **strict mandatory rule** (OUSL name required)
- Uses similar documents as **context**
- Provides **reasoning** for classification
- Ensures consistency

### 3. Two-Stage Benefit

**Stage 1 (ChromaDB)**: "Which documents are similar?" (flexible)  
**Stage 2 (LLM)**: "Does this meet OFFICIAL criteria?" (strict)

This approach combines **flexibility** (semantic search) with **precision** (rule enforcement).

## Troubleshooting

### No training documents found
**Solution**: Add at least 10-20 documents to each folder (`official/`, `personal/`)

### GROQ_API_KEY not found
**Solution**: Add API key to `backend/.env` file

### Import errors
**Solution**: Ensure all packages installed: `pip install -r requirements.txt`

### Low accuracy
**Solutions**:
- Add more training documents (aim for 50-100 each)
- Ensure training documents are representative
- Check if OUSL phrase appears consistently in official docs
- Adjust `SIMILARITY_THRESHOLD` in config

### Slow classification
**Solutions**:
- Reduce `TOP_K_RESULTS` (fewer similar docs retrieved)
- Reduce `MAX_CHUNKS_PER_DOC` (fewer chunks per document)
- Use smaller embedding model (edit `EMBEDDING_MODEL`)

## Performance

### Training
- **Time**: ~2-5 minutes for 100 documents
- **Storage**: ~50-100 MB for ChromaDB

### Classification
- **Time**: ~2-5 seconds per document
- **Accuracy**: 90-95% with good training data

## Next Steps

1. ✅ Install dependencies
2. ✅ Get Groq API key
3. ✅ Add training documents (50-100 each)
4. ✅ Run training script
5. ✅ Test classifier
6. ⏳ Integrate with print system API
7. ⏳ Connect frontend to classification endpoint
8. ⏳ Test with real user documents

## Support

**Documentation**:
- ChromaDB: https://docs.trychroma.com
- LangChain: https://python.langchain.com
- Groq: https://console.groq.com/docs
- sentence-transformers: https://www.sbert.net

**Issues**: Contact development team or check logs in terminal.
