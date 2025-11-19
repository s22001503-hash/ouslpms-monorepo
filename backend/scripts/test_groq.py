"""
Test Groq AI Service for Document Classification and Summarization
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

from app.services.groq_service import GroqService, get_groq_service
from app.services.pinecone_service import get_pinecone_service
from app.services.embedding_service import get_embedding_service


def setup_test_data():
    """Upload test training documents to Pinecone"""
    print("\n" + "=" * 70)
    print("SETUP: Uploading Test Training Documents")
    print("=" * 70)
    
    test_documents = [
        # Official documents
        {
            "text": "Invoice #INV-2025-001 for office supplies. Items: 50 pens ($25), 100 sheets paper ($50), 10 staplers ($30). Subtotal: $105. Tax: $10.50. Total: $115.50. Payment due: 30 days.",
            "category": "official"
        },
        {
            "text": "Annual Financial Report FY 2025. Executive Summary: Revenue increased 18% to $5.2M. Operating profit up 22% to $890K. Key drivers: new product launches, market expansion, cost optimization.",
            "category": "official"
        },
        {
            "text": "Purchase Order PO-2025-456. Requesting approval for IT equipment: 5 Dell monitors ($1,250), 5 wireless keyboards ($200), 5 optical mice ($100). Total: $1,550. Budget code: IT-CAP-2025.",
            "category": "official"
        },
        {
            "text": "Quarterly Sales Report Q4 2025. Sales exceeded target by 15%. Top regions: North (35%), West (28%), East (22%). Product mix: Software (60%), Hardware (40%). Customer retention: 92%.",
            "category": "official"
        },
        
        # Personal documents
        {
            "text": "You're invited to Sarah's Birthday Celebration! Date: Saturday, December 20th, 2025. Time: 7:00 PM. Venue: Grand Ballroom, Hilton Hotel. RSVP by Dec 10th. Dress code: Smart casual.",
            "category": "personal"
        },
        {
            "text": "Dear Mom and Dad, Thank you so much for your support during my studies. Your encouragement means everything. Looking forward to seeing you during the holidays. Love, Alex",
            "category": "personal"
        },
        {
            "text": "Wedding Invitation: Join us as we celebrate the marriage of Emily Johnson and Michael Chen. Saturday, June 15th, 2026 at 4:00 PM. St. Mary's Church followed by reception at Lakeside Resort.",
            "category": "personal"
        },
        
        # Confidential documents
        {
            "text": "CONFIDENTIAL - Employment Contract. Employee: Dr. Jane Smith. Position: Senior Lecturer, Computer Science. Salary: $75,000 per annum. Benefits: health insurance, retirement plan, 20 days annual leave. Start date: January 1, 2026.",
            "category": "confidential"
        },
        {
            "text": "Non-Disclosure Agreement (NDA). This agreement protects proprietary information including trade secrets, technical data, business strategies, and customer information. Violation subject to legal action.",
            "category": "confidential"
        },
        {
            "text": "Salary Statement - Employee ID: EMP-12345. Basic Salary: $5,000. Allowances: $1,200. Gross: $6,200. Deductions: Tax ($850), Insurance ($150). Net Pay: $5,200. Period: November 2025.",
            "category": "confidential"
        }
    ]
    
    embedding_svc = get_embedding_service()
    pinecone_svc = get_pinecone_service()
    
    chunks = []
    for i, doc in enumerate(test_documents):
        result = embedding_svc.generate_embedding(doc["text"])
        
        if result.success:
            chunks.append({
                "id": f"groq_test_doc_{i}",
                "embedding": result.embedding,
                "text": doc["text"],
                "category": doc["category"],
                "is_training_data": True,
                "test_data": True
            })
    
    success, failed = pinecone_svc.upsert_chunks_batch(chunks)
    
    print(f"\nUploaded {success} training documents")
    print(f"Categories: official={sum(1 for d in test_documents if d['category']=='official')}, "
          f"personal={sum(1 for d in test_documents if d['category']=='personal')}, "
          f"confidential={sum(1 for d in test_documents if d['category']=='confidential')}")
    
    return success > 0


def test_classification_with_rag():
    """Test 1: Document classification with RAG context"""
    print("\n" + "=" * 70)
    print("TEST 1: Classification with RAG Context")
    print("=" * 70)
    
    service = get_groq_service(model="llama")
    
    test_docs = [
        {
            "text": "Invoice for laptop computers and accessories. Dell Latitude laptops (3 units) $3,600, laptop bags (3 units) $150, wireless mice (3 units) $75. Total amount: $3,825. Payment terms: Net 30 days.",
            "expected": "official"
        },
        {
            "text": "Dear Friends, You are cordially invited to my graduation party next Saturday evening at 6 PM. We'll have dinner, music, and celebrate this milestone together. Hope to see you there!",
            "expected": "personal"
        },
        {
            "text": "Employee Confidential Record. Performance Review 2025. Employee demonstrates exceptional skills. Recommended for promotion to Senior position with 15% salary increase to $68,000.",
            "expected": "confidential"
        }
    ]
    
    correct = 0
    total = len(test_docs)
    
    for i, test in enumerate(test_docs, 1):
        print(f"\n{i}. Classifying document:")
        print(f"   Text: {test['text'][:80]}...")
        print(f"   Expected: {test['expected']}")
        print("-" * 70)
        
        result = service.classify_document(
            text=test['text'],
            use_rag=True,
            top_k=5
        )
        
        is_correct = result.category == test['expected']
        correct += int(is_correct)
        
        status = "✓" if is_correct else "✗"
        print(f"\n   {status} Predicted: {result.category}")
        print(f"   Confidence: {result.confidence:.2%}")
        print(f"   RAG Confidence: {result.retrieval_confidence:.2%}")
        print(f"   LLM Confidence: {result.llm_confidence:.2%}")
        print(f"   Reasoning: {result.reasoning[:150]}...")
    
    accuracy = correct / total
    print(f"\n{'='*70}")
    print(f"Accuracy: {correct}/{total} = {accuracy:.1%}")
    
    assert accuracy >= 0.6, "Should achieve at least 60% accuracy"
    print("\n✓ Test passed!")


def test_classification_without_rag():
    """Test 2: Document classification without RAG (pure LLM)"""
    print("\n" + "=" * 70)
    print("TEST 2: Classification without RAG (Pure LLM)")
    print("=" * 70)
    
    service = get_groq_service()
    
    test_text = """
    Quarterly Board Meeting Minutes - Q3 2025
    
    Attendees: Board of Directors, CEO, CFO, CTO
    
    Key Decisions:
    1. Approved $2M budget for new product development
    2. Authorized hiring of 10 additional engineers
    3. Discussed market expansion strategy for Asian markets
    4. Reviewed financial performance: Revenue up 12%, Profit up 8%
    
    Action Items:
    - CFO to prepare detailed budget breakdown
    - HR to initiate recruitment process
    - Marketing to conduct market research
    """
    
    print(f"\nDocument: Board Meeting Minutes")
    print(f"Length: {len(test_text)} characters")
    print("-" * 70)
    
    result = service.classify_document(
        text=test_text,
        use_rag=False  # Pure LLM classification
    )
    
    print(f"\nCategory: {result.category}")
    print(f"Confidence: {result.confidence:.2%}")
    print(f"Reasoning: {result.reasoning}")
    
    assert result.category in ["official", "personal", "confidential"]
    print("\n✓ Test passed!")


def test_summary_generation():
    """Test 3: Executive summary generation"""
    print("\n" + "=" * 70)
    print("TEST 3: Executive Summary Generation")
    print("=" * 70)
    
    service = get_groq_service()
    
    long_text = """
    Annual Performance Review and Strategic Planning Document 2025
    
    Executive Summary:
    This year has been transformative for our organization. We achieved record-breaking 
    revenue of $12.5 million, representing 25% growth year-over-year. Customer satisfaction 
    scores improved from 78% to 89%, and employee retention reached an all-time high of 94%.
    
    Key Achievements:
    - Successfully launched three new products, generating $3.2M in additional revenue
    - Expanded operations to five new markets across Southeast Asia
    - Implemented cutting-edge AI technology, improving efficiency by 35%
    - Reduced operational costs by 18% through process optimization
    - Achieved ISO 9001 and ISO 27001 certifications
    
    Financial Performance:
    Revenue grew from $10M to $12.5M (+25%). Operating profit increased from $1.8M to 
    $2.4M (+33%). Gross margin improved from 45% to 48%. The company maintained a 
    healthy cash position of $4.2M with zero long-term debt.
    
    Customer Metrics:
    Customer base grew from 5,000 to 7,200 (+44%). Net Promoter Score improved from 
    42 to 58. Customer churn reduced from 8% to 4.5%. Average customer lifetime value 
    increased by 28%.
    
    Strategic Initiatives for 2026:
    1. Launch AI-powered product suite targeting enterprise customers
    2. Expand into European and Latin American markets
    3. Invest $5M in R&D for next-generation solutions
    4. Build strategic partnerships with industry leaders
    5. Enhance employee development programs with $500K training budget
    
    Challenges and Risks:
    Market competition intensified with new entrants. Talent acquisition remains 
    challenging in competitive tech market. Supply chain disruptions affected delivery 
    timelines. Cybersecurity threats require increased vigilance and investment.
    
    Conclusion:
    2025 was a year of exceptional growth and achievement. With strong fundamentals, 
    innovative products, and a talented team, we are well-positioned for continued 
    success in 2026 and beyond.
    """
    
    print(f"\nDocument length: {len(long_text.split())} words")
    print("-" * 70)
    
    result = service.generate_summary(
        text=long_text,
        max_words=150,
        include_key_points=True
    )
    
    print(f"\nSUMMARY ({result.word_count} words):")
    print(result.summary)
    
    if result.key_points:
        print(f"\nKEY POINTS:")
        for i, point in enumerate(result.key_points, 1):
            print(f"{i}. {point}")
    
    print(f"\nMetrics:")
    print(f"  Original length: {result.original_length} words")
    print(f"  Summary length: {result.word_count} words")
    print(f"  Compression ratio: {result.compression_ratio:.1%}")
    
    assert result.word_count > 0, "Should generate summary"
    assert result.word_count <= 200, f"Summary too long: {result.word_count} words"
    
    print("\n✓ Test passed!")


def test_different_models():
    """Test 4: Compare different Groq models"""
    print("\n" + "=" * 70)
    print("TEST 4: Compare Different Models")
    print("=" * 70)
    
    test_text = "Purchase requisition for conference room equipment: projector, screen, audio system. Total budget: $5,000. Approval required."
    
    models = ["llama", "qwen", "mixtral"]
    
    for model_name in models:
        print(f"\n{model_name.upper()} Model:")
        print("-" * 70)
        
        try:
            service = GroqService(model=model_name)
            result = service.classify_document(
                text=test_text,
                use_rag=True
            )
            
            print(f"Category: {result.category}")
            print(f"Confidence: {result.confidence:.2%}")
            print(f"Reasoning: {result.reasoning[:100]}...")
            
        except Exception as e:
            print(f"Error: {str(e)}")
    
    print("\n✓ Test passed!")


def test_edge_cases():
    """Test 5: Edge cases and error handling"""
    print("\n" + "=" * 70)
    print("TEST 5: Edge Cases")
    print("=" * 70)
    
    service = get_groq_service()
    
    # Test 1: Very short text
    print("\n1. Very short text:")
    result = service.classify_document("Hi there", use_rag=False)
    print(f"   Category: {result.category}, Confidence: {result.confidence:.2%}")
    
    # Test 2: Empty text
    print("\n2. Empty text:")
    try:
        result = service.classify_document("", use_rag=False)
        print(f"   Category: {result.category}, Confidence: {result.confidence:.2%}")
    except Exception as e:
        print(f"   Handled error: {str(e)[:50]}...")
    
    # Test 3: Very long text
    print("\n3. Very long text (5000 words):")
    long_text = " ".join(["word"] * 5000)
    result = service.classify_document(long_text, use_rag=False)
    print(f"   Category: {result.category}, Confidence: {result.confidence:.2%}")
    
    # Test 4: Special characters
    print("\n4. Special characters:")
    special_text = "Invoice #12345 @company.com $1,000.00 50% discount!"
    result = service.classify_document(special_text, use_rag=True)
    print(f"   Category: {result.category}, Confidence: {result.confidence:.2%}")
    
    print("\n✓ Test passed!")


def test_end_to_end_pipeline():
    """Test 6: Complete end-to-end pipeline"""
    print("\n" + "=" * 70)
    print("TEST 6: End-to-End Pipeline (Classification + Summary)")
    print("=" * 70)
    
    service = get_groq_service()
    
    document = """
    CONFIDENTIAL EMPLOYEE PERFORMANCE REVIEW
    
    Employee Name: John Anderson
    Employee ID: EMP-45678
    Department: Software Engineering
    Review Period: January - December 2025
    
    Performance Summary:
    John has demonstrated exceptional technical skills and leadership throughout 2025.
    He successfully led the development of our flagship product's new AI module, 
    delivered 3 weeks ahead of schedule. His code quality metrics rank in the top 5% 
    of the engineering team.
    
    Key Achievements:
    - Led team of 5 engineers on AI integration project ($800K budget)
    - Improved system performance by 40% through optimization
    - Mentored 3 junior developers, all promoted within the year
    - Published 2 technical papers at major conferences
    
    Areas for Development:
    - Could improve delegation and trust in team members
    - Time management for multiple concurrent projects
    
    Recommendation:
    Promote to Senior Engineering Manager with 18% salary increase to $95,000.
    Assign leadership of entire AI division (team of 15).
    
    Approved by: Sarah Chen, VP Engineering
    Date: December 1, 2025
    """
    
    print("\nStep 1: Classify Document")
    print("-" * 70)
    
    classification = service.classify_document(
        text=document,
        use_rag=True
    )
    
    print(f"Category: {classification.category}")
    print(f"Confidence: {classification.confidence:.2%}")
    print(f"Reasoning: {classification.reasoning[:150]}...")
    
    print("\n\nStep 2: Generate Summary")
    print("-" * 70)
    
    summary = service.generate_summary(
        text=document,
        max_words=100,
        include_key_points=True
    )
    
    print(f"\nSummary:\n{summary.summary}")
    
    if summary.key_points:
        print(f"\nKey Points:")
        for i, point in enumerate(summary.key_points, 1):
            print(f"{i}. {point}")
    
    print(f"\n\nResults:")
    print(f"  Classification: {classification.category} ({classification.confidence:.1%})")
    print(f"  Summary: {summary.word_count} words ({summary.compression_ratio:.1%} of original)")
    
    assert classification.category == "confidential", "Should classify as confidential"
    assert summary.word_count > 0, "Should generate summary"
    
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
    print("GROQ AI SERVICE - TEST SUITE")
    print("=" * 70)
    
    # Setup
    if not setup_test_data():
        print("\n✗ Failed to setup test data")
        return
    
    tests = [
        ("Classification with RAG", test_classification_with_rag),
        ("Classification without RAG", test_classification_without_rag),
        ("Summary Generation", test_summary_generation),
        ("Different Models", test_different_models),
        ("Edge Cases", test_edge_cases),
        ("End-to-End Pipeline", test_end_to_end_pipeline)
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
