"""
Test Document Retrieval Service
Tests retrieval, context building, and category suggestions
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

from app.services.retrieval_service import DocumentRetrievalService, get_retrieval_service
from app.services.pinecone_service import get_pinecone_service
from app.services.embedding_service import get_embedding_service


def setup_test_data():
    """Upload test documents to Pinecone"""
    print("\n" + "=" * 70)
    print("SETUP: Uploading Test Training Documents")
    print("=" * 70)
    
    # Test documents with different categories
    test_documents = [
        # Official documents (invoices, reports)
        {
            "text": "Invoice #12345 for office supplies including pens, paper, and staplers. Total amount: $150.00",
            "category": "official",
            "file_name": "invoice_12345.pdf"
        },
        {
            "text": "Invoice #12346 for IT equipment including monitors, keyboards, and mouse. Total: $500.00",
            "category": "official",
            "file_name": "invoice_12346.pdf"
        },
        {
            "text": "Annual Financial Report 2025. Revenue increased by 15% compared to previous year. Profit margins improved.",
            "category": "official",
            "file_name": "annual_report_2025.pdf"
        },
        {
            "text": "Quarterly sales report Q3 2025. Sales targets exceeded by 20%. Top performing regions: North and West.",
            "category": "official",
            "file_name": "sales_report_q3.pdf"
        },
        
        # Personal documents
        {
            "text": "You are cordially invited to my birthday party on Saturday, December 15th at 6 PM. Venue: Grand Hotel",
            "category": "personal",
            "file_name": "birthday_invitation.docx"
        },
        {
            "text": "Thank you letter for your generous donation to our charity. Your contribution makes a difference.",
            "category": "personal",
            "file_name": "thank_you_letter.docx"
        },
        {
            "text": "Personal letter to family members regarding upcoming holiday plans and travel arrangements.",
            "category": "personal",
            "file_name": "family_letter.docx"
        },
        
        # Confidential documents
        {
            "text": "Employment Contract between OUSL and John Doe. Position: Senior Lecturer. Salary: $60,000 per annum.",
            "category": "confidential",
            "file_name": "employment_contract_jdoe.pdf"
        },
        {
            "text": "Confidential Non-Disclosure Agreement (NDA) regarding proprietary technology and trade secrets.",
            "category": "confidential",
            "file_name": "nda_agreement.pdf"
        },
        {
            "text": "Salary slip for employee ID 12345. Basic salary, allowances, and deductions detailed.",
            "category": "confidential",
            "file_name": "salary_slip_12345.pdf"
        }
    ]
    
    # Generate embeddings and upload
    embedding_svc = get_embedding_service()
    pinecone_svc = get_pinecone_service()
    
    chunks = []
    for i, doc in enumerate(test_documents):
        result = embedding_svc.generate_embedding(doc["text"])
        
        if result.success:
            chunks.append({
                "id": f"test_train_doc_{i}",
                "embedding": result.embedding,
                "text": doc["text"],
                "category": doc["category"],
                "is_training_data": True,
                "file_name": doc["file_name"],
                "test_data": True
            })
    
    success, failed = pinecone_svc.upsert_chunks_batch(chunks)
    
    print(f"\nUploaded {success} training documents")
    print(f"Categories: official={sum(1 for d in test_documents if d['category']=='official')}, "
          f"personal={sum(1 for d in test_documents if d['category']=='personal')}, "
          f"confidential={sum(1 for d in test_documents if d['category']=='confidential')}")
    
    return success > 0


def test_basic_retrieval():
    """Test 1: Basic document retrieval"""
    print("\n" + "=" * 70)
    print("TEST 1: Basic Document Retrieval")
    print("=" * 70)
    
    service = get_retrieval_service()
    
    # Query for invoice
    query = "Invoice for office equipment purchase"
    print(f"\nQuery: '{query}'")
    print("-" * 70)
    
    result = service.retrieve_similar_documents(
        query_text=query,
        top_k=5
    )
    
    print(f"\nResults found: {result.total_results}")
    print(f"Top category: {result.top_category}")
    print(f"Confidence: {result.confidence:.2%}")
    
    print("\nTop matches:")
    for i, chunk in enumerate(result.chunks[:3], 1):
        print(f"\n{i}. [{chunk['similarity_score']*100:5.1f}%] {chunk['category']}")
        print(f"   {chunk['text'][:80]}...")
    
    assert result.total_results > 0, "Should find results"
    assert result.top_category == "official", "Should suggest 'official' category"
    
    print("\n✓ Test passed!")


def test_category_filtering():
    """Test 2: Retrieval with category filter"""
    print("\n" + "=" * 70)
    print("TEST 2: Category Filtering")
    print("=" * 70)
    
    service = get_retrieval_service()
    
    query = "document about contracts"
    print(f"\nQuery: '{query}'")
    print(f"Filter: category = 'confidential'")
    print("-" * 70)
    
    result = service.retrieve_similar_documents(
        query_text=query,
        top_k=5,
        filter={
            "is_training_data": True,
            "category": "confidential"
        }
    )
    
    print(f"\nResults found: {result.total_results}")
    print(f"All results are confidential: {all(c['category'] == 'confidential' for c in result.chunks)}")
    
    for i, chunk in enumerate(result.chunks, 1):
        print(f"{i}. [{chunk['similarity_score']*100:5.1f}%] {chunk['text'][:60]}...")
    
    assert all(c['category'] == 'confidential' for c in result.chunks), "All should be confidential"
    
    print("\n✓ Test passed!")


def test_context_building():
    """Test 3: Build context for AI classification"""
    print("\n" + "=" * 70)
    print("TEST 3: Context Building for AI")
    print("=" * 70)
    
    service = get_retrieval_service()
    
    query = "Quarterly financial performance report for Q4 2025"
    print(f"\nQuery: '{query}'")
    print("-" * 70)
    
    context = service.build_context_for_classification(
        query_text=query,
        top_k=5,
        include_examples=2
    )
    
    print(f"\nContext structure:")
    print(f"  Total similar documents: {context['total_similar_documents']}")
    print(f"  Suggested category: {context['suggested_category']}")
    print(f"  Confidence: {context['confidence']:.2%}")
    
    print(f"\n  Category distribution:")
    for category, percentage in context['category_distribution'].items():
        print(f"    {category}: {percentage:.1%}")
    
    print(f"\n  Examples by category:")
    for category, examples in context['examples_by_category'].items():
        print(f"    {category}: {len(examples)} examples")
    
    print(f"\n  Top matches:")
    for i, match in enumerate(context['top_matches'], 1):
        print(f"    {i}. [{match['similarity']*100:5.1f}%] {match['category']}")
        print(f"       {match['text'][:60]}...")
    
    assert context['total_similar_documents'] > 0, "Should have context"
    assert context['suggested_category'] is not None, "Should suggest category"
    
    print("\n✓ Test passed!")


def test_category_suggestions():
    """Test 4: Get category suggestions"""
    print("\n" + "=" * 70)
    print("TEST 4: Category Suggestions")
    print("=" * 70)
    
    service = get_retrieval_service()
    
    test_queries = [
        "Invoice for printer and computer accessories",
        "Birthday party invitation for colleagues",
        "Employee salary information and benefits"
    ]
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        print("-" * 70)
        
        suggestions = service.get_category_suggestions(
            query_text=query,
            top_k=10
        )
        
        print("Category suggestions:")
        for category, confidence in suggestions:
            bar_length = int(confidence * 50)
            bar = "█" * bar_length
            print(f"  {category:15} [{confidence:5.1%}] {bar}")
    
    print("\n✓ Test passed!")


def test_multiple_queries():
    """Test 5: Multiple query types"""
    print("\n" + "=" * 70)
    print("TEST 5: Multiple Query Types")
    print("=" * 70)
    
    service = get_retrieval_service()
    
    test_cases = [
        {
            "query": "Purchase order for office stationery",
            "expected_category": "official"
        },
        {
            "query": "Thank you note for helping with project",
            "expected_category": "personal"
        },
        {
            "query": "Confidential employment terms and conditions",
            "expected_category": "confidential"
        }
    ]
    
    correct = 0
    total = len(test_cases)
    
    for i, test in enumerate(test_cases, 1):
        query = test["query"]
        expected = test["expected_category"]
        
        result = service.retrieve_similar_documents(
            query_text=query,
            top_k=5
        )
        
        predicted = result.top_category
        is_correct = predicted == expected
        correct += int(is_correct)
        
        status = "✓" if is_correct else "✗"
        print(f"\n{i}. {status} Query: '{query}'")
        print(f"   Expected: {expected}, Got: {predicted} ({result.confidence:.2%})")
    
    accuracy = correct / total
    print(f"\n{'='*70}")
    print(f"Accuracy: {correct}/{total} = {accuracy:.1%}")
    
    assert accuracy >= 0.6, "Should achieve at least 60% accuracy"
    
    print("\n✓ Test passed!")


def test_edge_cases():
    """Test 6: Edge cases"""
    print("\n" + "=" * 70)
    print("TEST 6: Edge Cases")
    print("=" * 70)
    
    service = get_retrieval_service()
    
    # Test 1: Empty query
    print("\n1. Empty query:")
    result = service.retrieve_similar_documents("", top_k=5)
    print(f"   Results: {result.total_results}")
    
    # Test 2: Very short query
    print("\n2. Very short query:")
    result = service.retrieve_similar_documents("Hi", top_k=5)
    print(f"   Results: {result.total_results}")
    
    # Test 3: No matches (very specific query)
    print("\n3. Unrelated query:")
    result = service.retrieve_similar_documents(
        "Quantum physics molecular structure analysis",
        top_k=5,
        min_similarity=0.8  # High threshold
    )
    print(f"   Results: {result.total_results}")
    
    # Test 4: Large top_k
    print("\n4. Large top_k:")
    result = service.retrieve_similar_documents(
        "financial document",
        top_k=100
    )
    print(f"   Results: {result.total_results}")
    
    print("\n✓ Test passed!")


def cleanup_test_data():
    """Remove test data from Pinecone"""
    print("\n" + "=" * 70)
    print("CLEANUP: Removing Test Data")
    print("=" * 70)
    
    pinecone_svc = get_pinecone_service()
    success = pinecone_svc.delete_by_filter({"test_data": True})
    
    if success:
        print("✓ Test data removed")
    else:
        print("✗ Cleanup failed")
    
    return success


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("DOCUMENT RETRIEVAL SERVICE - TEST SUITE")
    print("=" * 70)
    
    # Setup
    if not setup_test_data():
        print("\n✗ Failed to setup test data")
        return
    
    tests = [
        ("Basic Retrieval", test_basic_retrieval),
        ("Category Filtering", test_category_filtering),
        ("Context Building", test_context_building),
        ("Category Suggestions", test_category_suggestions),
        ("Multiple Queries", test_multiple_queries),
        ("Edge Cases", test_edge_cases)
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"\n✗ {name} FAILED: {str(e)}")
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
        print("\n🎉 All tests passed!")
        
        # Cleanup
        response = input("\nRemove test data? (y/n): ")
        if response.lower() == 'y':
            cleanup_test_data()
    else:
        print(f"\n⚠️ {failed} test(s) failed")
    
    print("=" * 70)


if __name__ == "__main__":
    run_all_tests()
