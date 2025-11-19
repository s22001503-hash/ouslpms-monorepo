"""
Test Script for Embedding Service
Tests embedding generation with real document chunks
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.embedding_service import EmbeddingService, get_embedding_service
from app.services.document_extractor import DocumentExtractor
from app.utils.text_chunker import TextChunker
import json


def test_basic_embedding():
    """Test 1: Basic embedding generation"""
    print("\n" + "=" * 70)
    print("TEST 1: Basic Embedding Generation")
    print("=" * 70)
    
    service = EmbeddingService()
    
    # Test single text
    text = "Invoice #12345 for office supplies totaling $1,500"
    result = service.generate_embedding(text)
    
    print(f"\nInput text: {text}")
    print(f"Success: {result.success}")
    print(f"Dimension: {result.dimension}")
    print(f"Model: {result.model_name}")
    print(f"Text length: {result.text_length} characters")
    print(f"\nFirst 10 embedding values:")
    print(f"  {result.embedding[:10]}")
    
    assert result.success, "Embedding generation failed"
    assert result.dimension == 384, f"Expected 384 dimensions, got {result.dimension}"
    assert len(result.embedding) == 384, "Embedding length mismatch"
    
    print("\n✅ Test 1 passed!")


def test_batch_embeddings():
    """Test 2: Batch embedding generation"""
    print("\n" + "=" * 70)
    print("TEST 2: Batch Embedding Generation")
    print("=" * 70)
    
    service = EmbeddingService()
    
    # Multiple texts
    texts = [
        "Official invoice for office equipment",
        "Personal birthday party invitation",
        "Confidential employment contract",
        "Annual financial report 2025",
        "Thank you letter for donation"
    ]
    
    print(f"\nGenerating embeddings for {len(texts)} texts...")
    results = service.generate_embeddings_batch(texts, show_progress=True)
    
    print(f"\n{'Text':<50} {'Success':<10} {'Dimension'}")
    print("-" * 70)
    for text, result in zip(texts, results):
        status = "✓" if result.success else "✗"
        print(f"{text[:47]:50} {status:<10} {result.dimension}")
    
    success_count = sum(1 for r in results if r.success)
    assert success_count == len(texts), f"Expected {len(texts)} successful embeddings, got {success_count}"
    
    print(f"\n✅ Test 2 passed! ({success_count}/{len(texts)} successful)")


def test_similarity_calculation():
    """Test 3: Similarity between documents"""
    print("\n" + "=" * 70)
    print("TEST 3: Similarity Calculation")
    print("=" * 70)
    
    service = EmbeddingService()
    
    # Create similar and dissimilar texts
    invoice1 = "Invoice #001 for office supplies - stapler, paper, pens - total $50"
    invoice2 = "Invoice #002 for office equipment - printer, scanner - total $500"
    birthday = "You are invited to my birthday party on Saturday at 3 PM"
    contract = "Employment contract between company and employee, effective January 2025"
    
    texts = [invoice1, invoice2, birthday, contract]
    results = service.generate_embeddings_batch(texts)
    
    print("\nDocuments:")
    for i, text in enumerate(texts, 1):
        print(f"  {i}. {text[:60]}...")
    
    print("\nSimilarity Matrix:")
    print(f"{'':20} {'Invoice 1':<12} {'Invoice 2':<12} {'Birthday':<12} {'Contract':<12}")
    print("-" * 70)
    
    for i, (name, result1) in enumerate(zip(['Invoice 1', 'Invoice 2', 'Birthday', 'Contract'], results)):
        row = f"{name:20}"
        for result2 in results:
            sim = service.calculate_similarity(result1.embedding, result2.embedding)
            row += f" {sim:>10.4f} "
        print(row)
    
    # Test expectations
    sim_invoices = service.calculate_similarity(results[0].embedding, results[1].embedding)
    sim_invoice_birthday = service.calculate_similarity(results[0].embedding, results[2].embedding)
    
    print(f"\nKey comparisons:")
    print(f"  Invoice 1 ↔ Invoice 2:  {sim_invoices:.4f} (should be high)")
    print(f"  Invoice 1 ↔ Birthday:   {sim_invoice_birthday:.4f} (should be low)")
    
    assert sim_invoices > 0.5, "Similar documents should have high similarity"
    assert sim_invoice_birthday < sim_invoices, "Dissimilar docs should have lower similarity"
    
    print("\n✅ Test 3 passed!")


def test_chunk_processing():
    """Test 4: Processing chunks with embeddings"""
    print("\n" + "=" * 70)
    print("TEST 4: Chunk Processing with Embeddings")
    print("=" * 70)
    
    service = EmbeddingService()
    chunker = TextChunker()
    
    # Create sample document with sections
    document = """
    Chapter 1: Introduction
    This is a comprehensive guide to document management systems.
    It covers various aspects including classification and storage.
    
    Chapter 2: Document Classification
    Document classification is the process of categorizing documents
    into predefined categories based on their content and purpose.
    
    Chapter 3: Storage Solutions
    Proper storage is essential for document management. We discuss
    various cloud and on-premise storage solutions.
    
    Chapter 4: Security Considerations
    Security is paramount when dealing with confidential documents.
    This chapter covers encryption, access control, and audit trails.
    """
    
    # Chunk the document
    print("\nChunking document...")
    chunks = chunker.chunk_text(document, strategy="semantic")
    print(f"Created {len(chunks)} chunks")
    
    # Convert chunks to dicts
    chunk_dicts = []
    for chunk in chunks:
        chunk_dicts.append({
            "text": chunk.text,
            "chunk_id": chunk.chunk_id,
            "section_title": chunk.section_title,
            "word_count": chunk.word_count
        })
    
    # Add embeddings
    print("\nGenerating embeddings for chunks...")
    processed_chunks = service.process_chunks_with_embeddings(chunk_dicts)
    
    print(f"\nProcessed Chunks:")
    print(f"{'Chunk':<8} {'Section':<30} {'Words':<8} {'Embedding'}")
    print("-" * 70)
    
    for chunk in processed_chunks:
        has_embedding = "✓" if chunk.get("embedding") else "✗"
        section = chunk.get("section_title", "N/A")[:28]
        print(f"{chunk['chunk_id']:<8} {section:<30} {chunk['word_count']:<8} {has_embedding}")
    
    # Verify all chunks have embeddings
    success_count = sum(1 for c in processed_chunks if c.get("embedding") is not None)
    assert success_count == len(chunks), f"Expected {len(chunks)} embeddings, got {success_count}"
    
    # Verify embedding dimensions
    for chunk in processed_chunks:
        assert chunk.get("embedding_dimension") == 384, "Embedding dimension mismatch"
    
    print(f"\n✅ Test 4 passed! ({success_count}/{len(chunks)} chunks with embeddings)")


def test_document_extraction_with_embeddings():
    """Test 5: Full pipeline - Extract + Chunk + Embed"""
    print("\n" + "=" * 70)
    print("TEST 5: Full Pipeline (Extract → Chunk → Embed)")
    print("=" * 70)
    
    # Create a sample text file
    sample_file = Path(__file__).parent.parent / "test_sample_document.txt"
    sample_content = """
    INVOICE
    
    Invoice Number: INV-2025-001
    Date: November 2, 2025
    
    Bill To:
    Open University of Sri Lanka
    Department of Computer Science
    Nawala, Nugegoda
    
    Items:
    1. Office Supplies - Pens, Papers, Staplers: $150
    2. Printer Cartridges - HP Black & Color: $200
    3. USB Flash Drives - 32GB x 10: $100
    
    Subtotal: $450
    Tax (15%): $67.50
    Total: $517.50
    
    Payment Terms: Net 30 Days
    Thank you for your business!
    """
    
    # Write sample file
    with open(sample_file, 'w', encoding='utf-8') as f:
        f.write(sample_content)
    
    print(f"\nCreated sample document: {sample_file.name}")
    
    # Extract text
    extractor = DocumentExtractor()
    extraction_result = extractor.extract_text(str(sample_file), enable_chunking=False)
    
    print(f"\n1. Text Extraction:")
    print(f"   Method: {extraction_result['extraction_method']}")
    print(f"   Characters: {len(extraction_result['text'])}")
    
    # Generate embedding
    service = EmbeddingService()
    embedding_result = service.generate_embedding(extraction_result['text'])
    
    print(f"\n2. Embedding Generation:")
    print(f"   Success: {embedding_result.success}")
    print(f"   Dimension: {embedding_result.dimension}")
    print(f"   Model: {embedding_result.model_name}")
    
    # Compare with similar and dissimilar texts
    similar_text = "Invoice for office equipment and supplies"
    dissimilar_text = "Employee birthday party invitation"
    
    similar_emb = service.generate_embedding(similar_text)
    dissimilar_emb = service.generate_embedding(dissimilar_text)
    
    sim_similar = service.calculate_similarity(embedding_result.embedding, similar_emb.embedding)
    sim_dissimilar = service.calculate_similarity(embedding_result.embedding, dissimilar_emb.embedding)
    
    print(f"\n3. Similarity Test:")
    print(f"   vs 'Invoice for office equipment': {sim_similar:.4f}")
    print(f"   vs 'Birthday party invitation':   {sim_dissimilar:.4f}")
    
    # Clean up
    sample_file.unlink()
    print(f"\n✅ Test 5 passed!")


def test_model_info():
    """Test 6: Model information"""
    print("\n" + "=" * 70)
    print("TEST 6: Model Information")
    print("=" * 70)
    
    service = EmbeddingService()
    info = service.get_model_info()
    
    print(f"\nModel Information:")
    print(json.dumps(info, indent=2))
    
    assert info['is_loaded'], "Model should be loaded"
    assert info['dimension'] == 384, "Expected 384 dimensions"
    
    print("\n✅ Test 6 passed!")


def test_singleton_pattern():
    """Test 7: Singleton service instance"""
    print("\n" + "=" * 70)
    print("TEST 7: Singleton Pattern")
    print("=" * 70)
    
    # Get service multiple times
    service1 = get_embedding_service()
    service2 = get_embedding_service()
    service3 = get_embedding_service()
    
    print(f"\nInstance 1 ID: {id(service1)}")
    print(f"Instance 2 ID: {id(service2)}")
    print(f"Instance 3 ID: {id(service3)}")
    
    assert service1 is service2, "Should return same instance"
    assert service2 is service3, "Should return same instance"
    
    print("\n✅ Test 7 passed! (All instances are the same)")


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("EMBEDDING SERVICE - COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    
    tests = [
        ("Basic Embedding", test_basic_embedding),
        ("Batch Embeddings", test_batch_embeddings),
        ("Similarity Calculation", test_similarity_calculation),
        ("Chunk Processing", test_chunk_processing),
        ("Full Pipeline", test_document_extraction_with_embeddings),
        ("Model Information", test_model_info),
        ("Singleton Pattern", test_singleton_pattern)
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
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Total tests: {len(tests)}")
    print(f"Passed: {passed} ✅")
    print(f"Failed: {failed} ❌")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print(f"\n⚠️  {failed} test(s) failed")
    
    print("=" * 70)


if __name__ == "__main__":
    run_all_tests()
