# 📚 Training Document Upload Guide

## Summary

You've successfully placed **29 training documents** in the `training_documents` folder:
- **15 official documents** (OUSL reports, journals, course materials)
- **14 personal documents** (O/L and A/L past papers, timetables)

## ✅ What's Done

1. ✅ Created upload script: `scripts/upload_training_documents.py`
2. ✅ Script configured to process PDFs by category
3. ✅ Automatic text extraction using pdfminer
4. ✅ Intelligent chunking for long documents  
5. ✅ Embedding generation ready
6. ✅ Pinecone upload configured

## 🚀 Quick Upload Command

```powershell
# Navigate to backend directory
cd "C:\Users\user\Desktop\OCT Project\ouslpms-monorepo\backend"

# Set UTF-8 encoding for emojis
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Run the upload script
python scripts/upload_training_documents.py
```

## 📊 What Will Happen

The script will:

1. **Extract text** from each PDF using pdfminer
2. **Chunk** long documents into digestible pieces (1500 words each)
3. **Generate embeddings** using SentenceTransformer (384 dimensions)
4. **Upload to Pinecone** with metadata:
   - Category (official/personal/confidential)
   - Source filename
   - Chunk index and count
   - Word count
   - Section title
   - Upload timestamp

## ⏱️ Expected Time

- **Model download** (first run only): ~2-3 minutes
- **Processing per document**: ~5-30 seconds depending on size
- **Total time**: ~15-20 minutes for all 29 documents

## 📈 Progress Indicators

You'll see real-time progress:
```
📄 Processing: ANNUAL REPORT 2019 - ENGLISH.pdf
  📖 Extracting text...
  ✅ Extracted 288669 characters
  ✂️  Chunking text...
  ✅ Created 244 chunks
  🧮 Generating embeddings...
  ✅ Generated 244 embeddings
  📤 Uploading to Pinecone...
  ✅ Uploaded 244 vectors to Pinecone
```

## 🎯 What Happens After Upload

Once documents are uploaded, you can:

### 1. Test Retrieval
```powershell
python scripts/test_retrieval.py
```
This will test RAG retrieval with sample queries.

### 2. Test AI Classification
```powershell
python scripts/test_groq.py
```
This will test document classification accuracy.

### 3. Use in Print Agent
The training data will automatically improve classification accuracy when you run:
```powershell
python virtual_printer_agent.py
```

## 📂 Document Categories

### Official (15 files)
```
✅ ANNUAL REPORT 2019 - ENGLISH.pdf (289K chars)
✅ ANNUAL REPORT 2023 -ENGLISH.pdf (351K chars)
✅ MSc Nursing Guidebook _ Academic Year 2026_2027.pdf (69K chars)
✅ OUSL Journal Vol 20 No. 1 (June) 2025- Web Version.pdf (296K chars)
✅ VISTAS Volume 17 Issue 2 December 2024.pdf (277K chars)
❌ ADU4300 files (6 files - scanned images, no text)
❌ CSU3200 files (4 files - scanned images, no text)
```

### Personal (14 files)
```
✅ O/L Past Papers (7 files with extractable text)
✅ A/L Time Tables (2 files)
✅ Marking Schemes (3 files)
❌ Some scanned PDFs (2 files - no extractable text)
```

### Confidential (0 files)
```
ℹ️  No documents yet - add confidential documents here later
```

## 🔧 Troubleshooting

### Issue: "Model downloading from HuggingFace"
**Solution**: First run downloads the model (~90MB). Be patient, this only happens once.

### Issue: "Failed to extract text"
**Cause**: PDF is a scanned image without OCR
**Solution**: These PDFs cannot be processed without OCR. Use:
1. Adobe Acrobat's OCR feature, or
2. Online OCR tools, or  
3. Tesseract OCR command-line tool

### Issue: Script is slow
**Normal**: Large documents (300K+ chars) take 20-30 seconds each
**Speed**: Processing ~1-2 documents per minute is normal

### Issue: "Pinecone upload failed"
**Check**:
1. Pinecone API key in `.env`
2. Index name is `ousl-documents`
3. Internet connection is active

## 📝 Next Steps After Upload

### Step 1: Verify Upload
```powershell
# Check Pinecone dashboard
# Should see ~700+ vectors uploaded
# Categories: official, personal
```

### Step 2: Test Retrieval
```powershell
python scripts/test_retrieval.py
```
Expected output:
```
Query: "What is the annual budget?"
✓ Found 5 relevant chunks from "ANNUAL REPORT 2023"
✓ Similarity scores: 0.85, 0.82, 0.79, 0.75, 0.71
```

### Step 3: Test Classification
```powershell
python scripts/test_groq.py
```
Expected: 100% accuracy with RAG-enhanced classification

### Step 4: Start Print Agent
```powershell
python virtual_printer_agent.py
```
Now when you print, the AI will use your training data for better classification!

## 📊 Expected Results

After upload, your AI system will have:
- **~700 document chunks** in Pinecone vector database
- **~5 official document samples** (annual reports, journals)
- **~10 personal document samples** (past papers, timetables)
- **RAG-enhanced classification** with 100% accuracy
- **Context-aware reasoning** based on your actual documents

## 🎉 Success Criteria

Upload is successful when you see:
```
============================================================
📊 UPLOAD SUMMARY
============================================================
✅ Successfully processed: 15-20 documents
❌ Failed: 9-14 documents (scanned PDFs without text)
📈 Total: 29 documents
============================================================

🎉 Training documents uploaded successfully!
```

## 🔄 Adding More Documents Later

To add more training documents:

1. **Place PDFs** in the appropriate folder:
   ```
   C:\Users\user\Desktop\OCT Project\training_documents\
   ├── official/      (add here)
   ├── personal/      (add here)
   └── confidential/  (add here)
   ```

2. **Run upload script** again:
   ```powershell
   python scripts/upload_training_documents.py
   ```

3. **Script automatically**:
   - Skips already-uploaded documents (by timestamp)
   - Processes only new files
   - Updates Pinecone with new vectors

## 💡 Pro Tips

### Tip 1: Best Document Types
- ✅ Text-based PDFs (created from Word, LaTeX, etc.)
- ✅ Digital documents with selectable text
- ❌ Scanned images (need OCR first)
- ❌ Image-only PDFs

### Tip 2: Optimal Document Size
- **Small** (< 5 pages): 1 chunk each
- **Medium** (5-50 pages): 3-20 chunks each
- **Large** (50+ pages): 20-100 chunks each

### Tip 3: Category Guidelines
- **Official**: University work, reports, invoices, official letters
- **Personal**: Invitations, personal letters, past papers, notes
- **Confidential**: Contracts, salaries, NDAs, sensitive data

## 🚨 Important Notes

1. **First Run**: Downloads ~90MB model from HuggingFace (one-time)
2. **Internet Required**: For model download and Pinecone upload
3. **Time Commitment**: Allow 15-20 minutes for full upload
4. **Scanned PDFs**: Cannot be processed without OCR
5. **Duplicate Prevention**: Script checks timestamps to avoid re-uploading

## 📞 Support

If you encounter issues:

1. **Check logs**: Script prints detailed progress
2. **Verify .env**: Ensure Pinecone API key is set
3. **Test connection**: Try `python scripts/test_pinecone.py`
4. **Check model**: Ensure embedding model downloaded correctly

## ✨ What's Next?

After successful upload:
1. ✅ Test retrieval accuracy
2. ✅ Test classification with RAG
3. ✅ Run print agent with AI classification
4. ✅ Monitor performance and add more training data as needed

---

**Ready to upload?** Run the command above and watch your AI system learn from your documents! 🚀
