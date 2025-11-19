"""
Test Pinecone Integration
Tests uploading and searching document embeddings
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

from app.services.pinecone_service import PineconeService
from app.services.embedding_service import get_embedding_service


def test_pinecone_connection():
    """Test 1: Connection and index access"""
    print("\n" + "=" * 70)
    print("TEST 1: Pinecone Connection")
    print("=" * 70)
    
    service = PineconeService()
    stats = service.get_index_stats()
    
    print(f"\nIndex: {service.config.index_name}")
    print(f"Total vectors: {stats.get('total_vector_count', 0)}")
    print(f"Dimension: {stats.get('dimension', 'N/A')}")
    print(f"Status: SUCCESS")


def test_upsert_single():
    """Test 2: Upload single chunk"""
    print("\n" + "=" * 70)
    print("TEST 2: Upload Single Chunk")
    print("=" * 70)
    
    # Generate embedding
    embedding_svc = get_embedding_service()
    text = "This is a test invoice for office supplies"
    result = embedding_svc.generate_embedding(text)
    
    print(f"\nText: {text}")
    print(f"Embedding dimension: {len(result.embedding)}")
    
    # Upload to Pinecone
    pinecone_svc = PineconeService()
    success = pinecone_svc.upsert_chunk(
        chunk_id="test_chunk_001",
        embedding=result.embedding,
        metadata={
            "text": text,
            "category": "official",
            "is_training_data": True,
            "test": True
        }
    )
    
    print(f"Upload status: {'SUCCESS' if success else 'FAILED'}")


def test_upsert_batch():
    """Test 3: Upload multiple chunks"""
    print("\n" + "=" * 70)
    print("TEST 3: Upload Batch of Chunks")
    print("=" * 70)
    
    # Prepare test documents
    documents = [
        {"text": "Invoice #001 for office supplies", "category": "official"},
        {"text": "Invoice #002 for IT equipment", "category": "official"},
        {"text": "Personal birthday party invitation", "category": "personal"},
        {"text": "Confidential employment contract", "category": "confidential"},
        {"text": "Annual financial report 2025", "category": "official"}
    ]
    
    # Generate embeddings
    embedding_svc = get_embedding_service()
    chunks = []
    
    for i, doc in enumerate(documents):
        result = embedding_svc.generate_embedding(doc["text"])
        
        if result.success:
            chunks.append({
                "id": f"test_doc_{i}",
                "embedding": result.embedding,
                "text": doc["text"],
                "category": doc["category"],
                "is_training_data": True,
                "test": True
            })
    
    print(f"\nPrepared {len(chunks)} chunks with embeddings")
    
    # Upload to Pinecone
    pinecone_svc = PineconeService()
    success, failed = pinecone_svc.upsert_chunks_batch(chunks)
    
    print(f"\nUpload results:")
    print(f"  Successful: {success}")
    print(f"  Failed: {failed}")
    print(f"  Status: {'SUCCESS' if failed == 0 else 'PARTIAL'}")


def test_similarity_search():
    """Test 4: Search for similar documents"""
    print("\n" + "=" * 70)
    print("TEST 4: Similarity Search")
    print("=" * 70)
    
    embedding_svc = get_embedding_service()
    pinecone_svc = PineconeService()
    
    # Test queries
    queries = [
        "Show me invoices for office equipment",
        "Find birthday invitations",
        "Search for employment contracts"
    ]
    
    for query in queries:
        print(f"\nQuery: '{query}'")
        print("-" * 70)
        
        results = pinecone_svc.search_by_text(
            text=query,
            embedding_service=embedding_svc,
            top_k=3,
            filter={"is_training_data": True}
        )
        
        for i, result in enumerate(results, 1):
            score_pct = result.score * 100
            text = result.metadata.get('text', 'N/A')[:50]
            category = result.metadata.get('category', 'N/A')
            
            print(f"  {i}. [{score_pct:5.1f}%] {category:15} | {text}...")


def test_filter_search():
    """Test 5: Search with metadata filters"""
    print("\n" + "=" * 70)
    print("TEST 5: Filtered Search")
    print("=" * 70)
    
    embedding_svc = get_embedding_service()
    pinecone_svc = PineconeService()
    
    query = "financial documents"
    
    # Search with filter
    print(f"\nQuery: '{query}'")
    print(f"Filter: category = 'official'")
    print("-" * 70)
    
    results = pinecone_svc.search_by_text(
        text=query,
        embedding_service=embedding_svc,
        top_k=5,
        filter={"category": "official"}
    )
    
    print(f"\nFound {len(results)} results:")
    for i, result in enumerate(results, 1):
        text = result.metadata.get('text', 'N/A')[:50]
        print(f"  {i}. [{result.score*100:5.1f}%] {text}...")


def test_index_stats():
    """Test 6: Get index statistics"""
    print("\n" + "=" * 70)
    print("TEST 6: Index Statistics")
    print("=" * 70)
    
    pinecone_svc = PineconeService()
    stats = pinecone_svc.get_index_stats()
    
    print(f"\nIndex: {pinecone_svc.config.index_name}")
    print(f"Total vectors: {stats.get('total_vector_count', 0)}")
    print(f"Dimension: {stats.get('dimension', 'N/A')}")
    print(f"Index fullness: {stats.get('index_fullness', 0):.2%}")
    print(f"Status: SUCCESS")


def cleanup_test_data():
    """Cleanup: Remove test data"""
    print("\n" + "=" * 70)
    print("CLEANUP: Removing Test Data")
    print("=" * 70)
    
    pinecone_svc = PineconeService()
    
    print("\nRemoving test documents...")
    success = pinecone_svc.delete_by_filter({"test": True})
    
    if success:
        print("Status: Test data removed")
    else:
        print("Status: Cleanup failed (may need manual cleanup)")


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("PINECONE INTEGRATION - TEST SUITE")
    print("=" * 70)
    
    # Check API key
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        print("\n❌ ERROR: PINECONE_API_KEY not set")
        print("\nPlease run setup_pinecone.py first")
        return
    
    tests = [
        ("Connection Test", test_pinecone_connection),
        ("Single Upload", test_upsert_single),
        ("Batch Upload", test_upsert_batch),
        ("Similarity Search", test_similarity_search),
        ("Filtered Search", test_filter_search),
        ("Index Statistics", test_index_stats)
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"\n❌ {name} FAILED: {str(e)}")
            import traceback
            traceback.print_exc()
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Total tests: {len(tests)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\nAll tests passed!")
        
        # Offer cleanup
        print("\n" + "=" * 70)
        response = input("Remove test data? (y/n): ")
        if response.lower() == 'y':
            cleanup_test_data()
    else:
        print(f"\n{failed} test(s) failed")
    
    print("=" * 70)


if __name__ == "__main__":
    run_all_tests()
