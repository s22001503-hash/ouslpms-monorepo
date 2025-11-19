# 🚀 Quick Start: Embedding Service

## Installation (One-Time)

```powershell
cd "c:\Users\user\Desktop\OCT Project\ouslpms-monorepo\backend"
pip install sentence-transformers numpy
```

## Basic Usage

### 1. Generate Single Embedding

```python
from app.services.embedding_service import EmbeddingService

service = EmbeddingService()
result = service.generate_embedding("Invoice for office supplies")

print(f"Success: {result.success}")
print(f"Dimension: {result.dimension}")  # 384
print(f"Vector: {result.embedding[:5]}")  # First 5 values
```

### 2. Generate Batch Embeddings

```python
texts = [
    "Official invoice",
    "Personal letter", 
    "Confidential contract"
]

results = service.generate_embeddings_batch(texts)

for text, result in zip(texts, results):
    if result.success:
        print(f"{text}: {result.dimension}D vector")
```

### 3. Process Chunks with Embeddings

```python
# From TextChunker
chunks = [
    {"text": "Chapter 1...", "chunk_id": 0},
    {"text": "Chapter 2...", "chunk_id": 1}
]

# Add embeddings
processed = service.process_chunks_with_embeddings(chunks)

# Result: chunks with added 'embedding' field
for chunk in processed:
    print(f"Chunk {chunk['chunk_id']}: {len(chunk['embedding'])} dimensions")
```

### 4. Calculate Similarity

```python
result1 = service.generate_embedding("Invoice for equipment")
result2 = service.generate_embedding("Invoice for supplies")
result3 = service.generate_embedding("Birthday invitation")

sim_similar = service.calculate_similarity(result1.embedding, result2.embedding)
sim_different = service.calculate_similarity(result1.embedding, result3.embedding)

print(f"Similar docs: {sim_similar:.2f}")      # ~0.77
print(f"Different docs: {sim_different:.2f}")  # ~0.17
```

## Testing

### Run Validation Test

```powershell
cd "c:\Users\user\Desktop\OCT Project\ouslpms-monorepo\backend"
python scripts/validate_embeddings.py
```

Expected output:
```
STEP 2 VALIDATION: COMPLETE
All tests passed successfully!
```

## Integration with Document Extraction

```python
from app.services.document_extractor import DocumentExtractor
from app.services.embedding_service import get_embedding_service

# Extract text with chunking
extractor = DocumentExtractor()
result = extractor.extract_text("document.pdf", enable_chunking=True)

# Generate embeddings for all chunks
service = get_embedding_service()
chunks_with_embeddings = service.process_chunks_with_embeddings(result["chunks"])

# Ready for Pinecone storage!
print(f"Processed {len(chunks_with_embeddings)} chunks with embeddings")
```

## Singleton Pattern (Recommended)

```python
from app.services.embedding_service import get_embedding_service

# Use this instead of creating new instances
service = get_embedding_service()  # Reuses same model

# Both will use the same instance (faster, less memory)
service1 = get_embedding_service()
service2 = get_embedding_service()
assert service1 is service2  # True
```

## Model Information

```python
service = EmbeddingService()
info = service.get_model_info()

print(info)
# {
#   'model_name': 'all-MiniLM-L6-v2',
#   'dimension': 384,
#   'max_seq_length': 512,
#   'is_loaded': True
# }
```

## Performance Tips

1. **Use batch processing for multiple texts:**
   ```python
   # ❌ Slow
   for text in texts:
       result = service.generate_embedding(text)
   
   # ✅ Fast (3-5x faster)
   results = service.generate_embeddings_batch(texts)
   ```

2. **Use singleton pattern:**
   ```python
   # ❌ Loads model multiple times
   service1 = EmbeddingService()
   service2 = EmbeddingService()
   
   # ✅ Loads model once
   service = get_embedding_service()
   ```

3. **Process chunks in batches:**
   ```python
   # Automatically uses batch processing
   processed = service.process_chunks_with_embeddings(chunks)
   ```

## Error Handling

```python
result = service.generate_embedding(text)

if result.success:
    vector = result.embedding
    # Process vector
else:
    print(f"Error: {result.error}")
    # Handle error
```

## Next Step: Pinecone Integration

Once embeddings are generated, they'll be stored in Pinecone:

```python
# Coming in Step 3
from app.services.pinecone_service import PineconeService

pinecone = PineconeService()
pinecone.store_chunks(chunks_with_embeddings)
```

---

**Status:** ✅ Step 2 Complete  
**Next:** Step 3 - Store in Pinecone
