"""
Upload Training Documents to Pinecone
======================================
This script processes PDF documents from the training_documents folder and uploads them to Pinecone.

Categories:
- official: University work documents
- personal: Personal documents
- confidential: Sensitive documents
"""

import os
import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.utils.text_chunker import TextChunker
from app.services.embedding_service import EmbeddingService
from app.services.pinecone_service import PineconeService
from dotenv import load_dotenv
import PyPDF2
from pdfminer.high_level import extract_text as pdfminer_extract_text
from datetime import datetime

# Load environment variables
load_dotenv()

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file using pdfminer (most robust)."""
    text = ""
    
    # Use pdfminer (most robust for complex PDFs)
    try:
        text = pdfminer_extract_text(pdf_path)
    except Exception as e:
        print(f"  ⚠️  pdfminer failed: {e}")
        return None
    
    # Return cleaned text
    text = text.strip()
    
    if not text or len(text) < 50:
        return None
    
    return text

def process_document(file_path, category, chunker, embedding_service, pinecone_service):
    """Process a single document: extract text, chunk, embed, and upload."""
    file_name = os.path.basename(file_path)
    print(f"\n📄 Processing: {file_name}")
    
    # Extract text from PDF
    print(f"  📖 Extracting text...")
    text = extract_text_from_pdf(file_path)
    if not text:
        print(f"  ❌ Failed to extract text")
        return False
    
    print(f"  ✅ Extracted {len(text)} characters")
    
    # Chunk the text
    print(f"  ✂️  Chunking text...")
    chunks = chunker.chunk_text(text, strategy="auto")
    print(f"  ✅ Created {len(chunks)} chunks")
    
    # Generate embeddings
    print(f"  🧮 Generating embeddings...")
    texts = [chunk.text for chunk in chunks]
    embeddings_results = embedding_service.generate_embeddings_batch(texts)
    embeddings = [result.embedding for result in embeddings_results]
    print(f"  ✅ Generated {len(embeddings)} embeddings")
    
    # Prepare vectors for Pinecone
    print(f"  📤 Uploading to Pinecone...")
    vectors = []
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        # Clean filename for vector ID (remove special characters)
        clean_filename = file_name.replace('.pdf', '').encode('ascii', 'ignore').decode('ascii')
        clean_filename = ''.join(c if c.isalnum() or c in [' ', '_', '-'] else '_' for c in clean_filename)
        
        chunk_dict = {
            'id': f"{category}_{clean_filename}_{i}_{int(datetime.now().timestamp())}",
            'embedding': embedding,  # Use 'embedding' key, not 'values'
            'text': chunk.text,
            'category': category,
            'source': file_name,
            'chunk_index': chunk.chunk_id,
            'total_chunks': chunk.total_chunks,
            'word_count': chunk.word_count,
            'section_title': chunk.section_title or 'General',
            'upload_timestamp': datetime.now().isoformat()
        }
        vectors.append(chunk_dict)
    
    # Upload to Pinecone
    successful, failed_count = pinecone_service.upsert_chunks_batch(vectors)
    if successful > 0:
        print(f"  ✅ Uploaded {successful} vectors to Pinecone")
        return True
    else:
        print(f"  ❌ Failed to upload to Pinecone ({failed_count} failed)")
        return False

def main():
    """Main function to process all training documents."""
    print("=" * 60)
    print("🚀 TRAINING DOCUMENT UPLOAD TO PINECONE")
    print("=" * 60)
    
    # Define training documents directory
    training_dir = Path(r"C:\Users\user\Desktop\OCT Project\training_documents")
    
    if not training_dir.exists():
        print(f"❌ Training directory not found: {training_dir}")
        return
    
    # Initialize services
    print("\n🔧 Initializing services...")
    chunker = TextChunker()
    embedding_service = EmbeddingService()
    pinecone_service = PineconeService()
    print("✅ Services initialized")
    
    # Categories to process
    categories = ['official', 'personal', 'confidential']
    
    total_processed = 0
    total_failed = 0
    
    for category in categories:
        category_dir = training_dir / category
        
        if not category_dir.exists():
            print(f"\n⚠️  Category directory not found: {category}")
            continue
        
        # Get all PDF files in the category
        pdf_files = list(category_dir.glob("*.pdf"))
        
        if not pdf_files:
            print(f"\n📂 Category: {category.upper()}")
            print(f"  ℹ️  No PDF files found")
            continue
        
        print(f"\n" + "=" * 60)
        print(f"📂 CATEGORY: {category.upper()}")
        print(f"📊 Found {len(pdf_files)} PDF files")
        print("=" * 60)
        
        for pdf_file in pdf_files:
            try:
                success = process_document(
                    str(pdf_file), 
                    category, 
                    chunker, 
                    embedding_service, 
                    pinecone_service
                )
                if success:
                    total_processed += 1
                else:
                    total_failed += 1
            except Exception as e:
                print(f"\n❌ Error processing {pdf_file.name}: {e}")
                total_failed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 UPLOAD SUMMARY")
    print("=" * 60)
    print(f"✅ Successfully processed: {total_processed} documents")
    print(f"❌ Failed: {total_failed} documents")
    print(f"📈 Total: {total_processed + total_failed} documents")
    print("=" * 60)
    
    if total_processed > 0:
        print("\n🎉 Training documents uploaded successfully!")
        print("\n💡 Next steps:")
        print("   1. Test retrieval with: python scripts/test_retrieval.py")
        print("   2. Test AI classification with: python scripts/test_groq.py")
        print("   3. Run print agent with: python virtual_printer_agent.py")
    else:
        print("\n⚠️  No documents were processed. Please check:")
        print("   - PDF files exist in training_documents folders")
        print("   - PDFs have extractable text (not scanned images)")
        print("   - Pinecone credentials are correct in .env")

if __name__ == "__main__":
    main()
