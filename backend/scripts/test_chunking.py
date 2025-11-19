"""
Test the Document Extractor with Chunking
==========================================

Run this script to test the chunking functionality
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.document_extractor import DocumentExtractor

def create_sample_long_text():
    """Create a sample long document for testing"""
    text = """
Chapter 1: Introduction to OUSL

The Open University of Sri Lanka (OUSL) is a national university in Sri Lanka.
It was established in 1980 and is the premier open and distance learning 
institution in the country.

""" + " ".join(["Sample text about OUSL history and mission."] * 500) + """

Chapter 2: Academic Programs

OUSL offers a wide range of undergraduate and postgraduate programs across
multiple faculties including Engineering, Natural Sciences, and Social Sciences.

""" + " ".join(["Details about academic programs and courses offered."] * 500) + """

Chapter 3: Student Services

The university provides comprehensive support services to students including
library facilities, counseling, and online learning platforms.

""" + " ".join(["Information about student support services."] * 500) + """

Chapter 4: Research and Innovation

OUSL is committed to research excellence and innovation in various fields.

""" + " ".join(["Research activities and achievements."] * 500)
    
    return text

def test_chunking():
    """Test the chunking functionality"""
    print("\n" + "="*70)
    print("DOCUMENT EXTRACTOR CHUNKING TEST")
    print("="*70)
    
    extractor = DocumentExtractor()
    
    # Test 1: Short text (no chunking needed)
    print("\n📄 Test 1: Short Document (No Chunking Expected)")
    print("-" * 70)
    short_text = "This is a short invoice with only 50 words. " * 10
    
    # Save to temp file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(short_text)
        short_file = f.name
    
    # Note: For actual testing, use PDF files
    # For now, we'll test the chunker directly
    from app.utils.text_chunker import TextChunker
    
    chunker = TextChunker()
    
    print(f"Text length: {len(short_text.split())} words")
    print(f"Should chunk: {chunker.should_chunk(short_text)}")
    
    chunks = chunker.chunk_text(short_text)
    print(f"Number of chunks: {len(chunks)}")
    print(f"Chunk strategy: {'No chunking' if len(chunks) == 1 else 'Chunked'}")
    
    # Test 2: Long text (chunking expected)
    print("\n\n📚 Test 2: Long Document (Chunking Expected)")
    print("-" * 70)
    long_text = create_sample_long_text()
    
    print(f"Text length: {len(long_text.split())} words")
    print(f"Should chunk: {chunker.should_chunk(long_text)}")
    
    # Test fixed-size chunking
    print("\n  Strategy: Fixed-size chunking")
    chunks_fixed = chunker.chunk_text(long_text, strategy="fixed")
    print(f"  Number of chunks: {len(chunks_fixed)}")
    
    for i, chunk in enumerate(chunks_fixed[:3]):  # Show first 3
        print(f"\n  Chunk {i+1}:")
        print(f"    Chunk ID: {chunk.chunk_id}")
        print(f"    Total chunks: {chunk.total_chunks}")
        print(f"    Section: {chunk.section_title}")
        print(f"    Words: {chunk.word_count}")
        print(f"    Pages: {chunk.page_range[0]}-{chunk.page_range[1]}")
        print(f"    Preview: {chunk.text[:100]}...")
    
    # Test semantic chunking
    print("\n\n  Strategy: Semantic (section-based) chunking")
    chunks_semantic = chunker.chunk_text(long_text, strategy="semantic")
    print(f"  Number of chunks: {len(chunks_semantic)}")
    
    for i, chunk in enumerate(chunks_semantic):
        print(f"\n  Chunk {i+1}:")
        print(f"    Section: {chunk.section_title}")
        print(f"    Words: {chunk.word_count}")
        print(f"    Pages: {chunk.page_range[0]}-{chunk.page_range[1]}")
        print(f"    Preview: {chunk.text[:100]}...")
    
    # Test 3: Compare strategies
    print("\n\n📊 Test 3: Strategy Comparison")
    print("-" * 70)
    print(f"Fixed-size chunks: {len(chunks_fixed)}")
    print(f"Semantic chunks: {len(chunks_semantic)}")
    print(f"\nSemantic chunking preserved {len(chunks_semantic)} distinct sections")
    print(f"Fixed-size chunking created {len(chunks_fixed)} uniform chunks")
    
    # Cleanup
    try:
        os.unlink(short_file)
    except:
        pass
    
    print("\n" + "="*70)
    print("✅ CHUNKING TEST COMPLETE")
    print("="*70)
    
    return {
        "short_chunks": len(chunks),
        "long_chunks_fixed": len(chunks_fixed),
        "long_chunks_semantic": len(chunks_semantic)
    }

if __name__ == "__main__":
    results = test_chunking()
    
    print("\n\n📋 Summary:")
    print(f"  Short document chunks: {results['short_chunks']} (expected: 1)")
    print(f"  Long document (fixed): {results['long_chunks_fixed']} chunks")
    print(f"  Long document (semantic): {results['long_chunks_semantic']} chunks")
    
    print("\n✨ Next steps:")
    print("  1. ✅ Chunking utility created")
    print("  2. ✅ Document extractor enhanced")
    print("  3. ⏭️  Next: Generate embeddings for chunks")
    print("  4. ⏭️  Next: Store chunks in Pinecone")
