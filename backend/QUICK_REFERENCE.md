# 🚀 Quick Reference: AI Document Classification

## One-Command Classification

```python
from app.services.groq_service import get_groq_service

# Initialize once (singleton)
groq_service = get_groq_service()

# Classify any document
result = groq_service.classify_document(
    text="Your document text here...",
    use_rag=True  # Use retrieval context for better accuracy
)

# Get results
print(f"Category: {result.category}")           # official/personal/confidential
print(f"Confidence: {result.confidence:.1%}")   # 87.2%
print(f"Reasoning: {result.reasoning}")         # Why this category?
```

---

## Common Usage Patterns

### 1. Classify + Summarize
```python
service = get_groq_service()

# Classify
classification = service.classify_document(text, use_rag=True)

# Summarize
summary = service.generate_summary(text, max_words=100)

# Use results
print(f"{classification.category} ({classification.confidence:.0%})")
print(f"Summary: {summary.summary}")
for point in summary.key_points:
    print(f"• {point}")
```

### 2. Process PDF File
```python
import PyPDF2

# Extract text from PDF
with open("document.pdf", "rb") as f:
    reader = PyPDF2.PdfReader(f)
    text = " ".join(page.extract_text() for page in reader.pages)

# Classify
result = groq_service.classify_document(text, use_rag=True)
```

### 3. Upload Training Documents
```python
from app.services.embedding_service import get_embedding_service
from app.services.pinecone_service import get_pinecone_service

# Generate embedding
embedding_svc = get_embedding_service()
embedding_result = embedding_svc.generate_embedding(document_text)

# Upload to Pinecone
pinecone_svc = get_pinecone_service()
pinecone_svc.upsert_chunk({
    "id": "unique_doc_id",
    "embedding": embedding_result.embedding,
    "text": document_text,
    "category": "official",  # or "personal" or "confidential"
    "is_training_data": True,
    "file_name": "invoice_001.pdf"
})
```

### 4. Batch Processing
```python
documents = [...]  # List of documents to classify

results = []
for doc in documents:
    result = groq_service.classify_document(doc, use_rag=True)
    results.append({
        "text": doc[:100],
        "category": result.category,
        "confidence": result.confidence
    })

# Analysis
for r in results:
    print(f"{r['category']:15} {r['confidence']:.0%}  {r['text']}...")
```

---

## Configuration

### Environment Variables (.env)
```bash
# Required
PINECONE_API_KEY=pcsk_xxxxx
GROQ_API_KEY=gsk_xxxxx

# Optional (defaults work fine)
PINECONE_INDEX_NAME=ousl-documents
PINECONE_DIMENSION=384
```

### Get API Keys
- **Pinecone**: https://app.pinecone.io/ → API Keys
- **Groq**: https://console.groq.com/ → API Keys

---

## Testing

### Run All Tests
```bash
# Individual steps
python scripts/test_chunking.py
python scripts/test_embeddings.py
python scripts/test_pinecone.py
python scripts/test_retrieval.py
python scripts/test_groq.py

# Verify API keys
python scripts/verify_groq_key.py
```

### Expected Results
```
✓ Chunking:   All tests pass
✓ Embeddings: 5/5 tests pass
✓ Pinecone:   6/6 tests pass (100%)
✓ Retrieval:  6/6 tests pass (100%)
✓ Groq AI:    6/6 tests pass (100%)

Overall: 23/23 tests pass (100% success)
```

---

## API Response Structure

### Classification Result
```python
{
    "category": "official",                    # Category name
    "confidence": 0.9426,                      # 0.0 to 1.0
    "reasoning": "Structured invoice with...", # Why this category
    "suggested_categories": [                  # Alternative suggestions
        {"category": "official", "confidence": 0.94}
    ],
    "retrieval_confidence": 0.8714,            # RAG confidence
    "llm_confidence": 0.99                     # LLM confidence
}
```

### Summary Result
```python
{
    "summary": "John Anderson's performance...",  # Executive summary
    "key_points": [                                # Bullet points
        "Led AI integration project...",
        "Improved system performance by 40%...",
        "Recommended for promotion..."
    ],
    "word_count": 18,                             # Summary length
    "original_length": 153,                       # Original length
    "compression_ratio": 0.118                    # 11.8% of original
}
```

---

## Performance Expectations

### Accuracy
- **With RAG**: 100% on test data (3/3 correct)
- **Without RAG**: ~90% confidence average
- **Confidence range**: 85-100% for correct classifications

### Speed
- **Classification**: 1-2 seconds
- **Summarization**: 2-3 seconds
- **Total pipeline**: < 5 seconds per document

### Compression
- **Summary length**: 10-15% of original (6-10x reduction)
- **Key points**: 3-5 bullets extracted
- **Quality**: High - preserves critical information

---

## Common Issues & Solutions

### Issue: "Invalid API Key" (401)
**Solution**: Get new API key from https://console.groq.com/keys
```bash
# Verify key
python scripts/verify_groq_key.py
```

### Issue: "Model not found" (404)
**Solution**: Use `llama` model (others deprecated)
```python
service = get_groq_service(model="llama")
```

### Issue: Low confidence scores
**Solution**: Add more training documents to Pinecone
```python
# Need 20-50 examples per category for best results
```

### Issue: Empty embeddings
**Solution**: Text might be too short
```python
# Minimum ~10 words recommended for good embeddings
```

---

## Best Practices

### 1. Training Data Quality
- **Quantity**: 20-50 examples per category minimum
- **Diversity**: Include various document types
- **Quality**: Clear, well-written examples
- **Balance**: Similar number per category

### 2. Classification
- **Use RAG**: Always set `use_rag=True` for better accuracy
- **Check confidence**: < 70% may need review
- **Monitor reasoning**: Understand why category was chosen
- **Provide feedback**: Update training data based on errors

### 3. Summarization
- **Adjust length**: Shorter for quick reference, longer for detail
- **Use key points**: Easier to scan than paragraph
- **Combine with classification**: Better context understanding

### 4. Production Deployment
- **Cache results**: Don't re-classify same document
- **Batch processing**: Process multiple docs in parallel
- **Monitor usage**: Track API calls and costs
- **Log classifications**: Track accuracy over time

---

## Integration Examples

### Print Job Classification
```python
def classify_print_job(print_job):
    # Extract text
    text = extract_text_from_print_job(print_job)
    
    # Classify
    result = groq_service.classify_document(text, use_rag=True)
    
    # Store in Firestore
    firestore_db.collection('print_jobs').document(print_job.id).set({
        'category': result.category,
        'confidence': result.confidence,
        'reasoning': result.reasoning,
        'timestamp': datetime.now()
    })
    
    return result
```

### FastAPI Endpoint
```python
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ClassifyRequest(BaseModel):
    text: str

@router.post("/api/classify")
async def classify(request: ClassifyRequest):
    result = groq_service.classify_document(
        text=request.text,
        use_rag=True
    )
    
    return {
        "category": result.category,
        "confidence": result.confidence,
        "reasoning": result.reasoning
    }
```

### Automated Folder Monitoring
```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class DocumentHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith('.pdf'):
            # Extract text
            text = extract_pdf_text(event.src_path)
            
            # Classify
            result = groq_service.classify_document(text, use_rag=True)
            
            # Move to category folder
            category_folder = f"sorted/{result.category}"
            move_file(event.src_path, category_folder)

# Start monitoring
observer = Observer()
observer.schedule(DocumentHandler(), "incoming/", recursive=False)
observer.start()
```

---

## Troubleshooting Checklist

- [ ] API keys configured in `.env`
- [ ] `.env` file saved (not just in editor)
- [ ] Pinecone index created (`setup_pinecone.py`)
- [ ] Training data uploaded (at least 5-10 docs per category)
- [ ] Python packages installed (`pip install -r requirements.txt`)
- [ ] Virtual environment activated
- [ ] Internet connection working
- [ ] Test scripts passing

---

## Quick Commands

```bash
# Setup
pip install -r requirements.txt
python scripts/setup_pinecone.py

# Test
python scripts/verify_groq_key.py
python scripts/test_groq.py

# Classify (interactive)
python -c "
from app.services.groq_service import get_groq_service
svc = get_groq_service()
text = input('Enter document text: ')
result = svc.classify_document(text, use_rag=True)
print(f'{result.category} ({result.confidence:.0%}): {result.reasoning}')
"
```

---

## Documentation Links

- **Full Documentation**: `AI_CLASSIFICATION_COMPLETE.md`
- **Step-by-step guides**:
  - `STEP1_CHUNKING_COMPLETE.md`
  - `STEP2_EMBEDDING_COMPLETE.md`
  - `STEP3_PINECONE_COMPLETE.md`
  - `STEP4_RETRIEVAL_COMPLETE.md`
  - `STEP5_GROQ_COMPLETE.md`

---

## Support

Need help? Check these resources:
1. Test scripts output (detailed error messages)
2. API key verification (`verify_groq_key.py`)
3. Documentation files in `backend/`
4. Groq docs: https://console.groq.com/docs
5. Pinecone docs: https://docs.pinecone.io/

---

**🎉 Happy Classifying!**

*System tested and ready for production use.*
*100% test success rate on all 5 implementation steps.*
