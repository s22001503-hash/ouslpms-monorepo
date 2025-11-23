"""
Test the AI classifier with a sample document
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from ai_classifier.classifier import DocumentClassifier

def test_classifier():
    """Test classification with sample documents"""
    
    print("\n" + "="*60)
    print("TESTING AI DOCUMENT CLASSIFIER")
    print("="*60 + "\n")
    
    # Initialize classifier
    print("Initializing classifier...")
    classifier = DocumentClassifier()
    
    # Test document 1: OFFICIAL OUSL document with HIGH boosters
    print("\n--- TEST 1: OFFICIAL OUSL DOCUMENT (HIGH BOOSTERS) ---")
    official_sample = """
    The Open University of Sri Lanka
    FACULTY OF NATURAL SCIENCE
    Department of Computer Science
    
    BACHELOR OF SCIENCE DEGREE PROGRAMME
    
    Course Code: CSU3200
    Course Title: Software Project Management
    
    This course covers project planning, risk management, and team coordination
    for software development projects. Students will learn industry-standard
    methodologies including Agile and Waterfall approaches.
    
    Academic Year: 2024/2025
    Semester: 1
    Assessment: CAT 1 (30%), CAT 2 (30%), Final (40%)
    
    Address: PO Box 21, The Open University of Sri Lanka, Nawala, Nugegoda
    """
    
    result1 = classifier.classify_document(official_sample)
    print(f"\nExpected: OFFICIAL (HIGH confidence ~95%+)")
    print(f"Got: {result1['classification']} ({result1['confidence']:.0%})")
    print(f"HIGH Boosters: {result1['high_booster_count']}")
    print(f"MEDIUM Boosters: {result1['medium_booster_count']}")
    print(f"LOW Boosters: {result1['low_booster_count']}")
    
    # Test document 2: PERSONAL document
    print("\n--- TEST 2: PERSONAL DOCUMENT ---")
    personal_sample = """
    Dear John,
    
    Thank you for your letter. I hope this finds you well.
    I wanted to share some thoughts about the novel I've been reading.
    
    The story takes place in a small village where the protagonist
    discovers an ancient mystery. It's quite captivating!
    
    I'm also planning a trip to the mountains next month.
    Would you like to join?
    
    Best regards,
    Sarah
    """
    
    result2 = classifier.classify_document(personal_sample)
    print(f"\nExpected: PERSONAL")
    print(f"Got: {result2['classification']} ({result2['confidence']:.0%})")
    
    # Test document 3: Edge case - mentions OUSL with MEDIUM boosters
    print("\n--- TEST 3: EDGE CASE (MEDIUM BOOSTERS) ---")
    edge_sample = """
    Course Syllabus
    The Open University of Sri Lanka
    
    This is a syllabus for the 2024/2025 academic year, Semester 1.
    
    Course Code: BYU3301
    
    Assessment Structure:
    - CAT 1: 20%
    - CAT 2: 20%
    - Practical: 20%
    - Final Examination (OBT): 40%
    
    Students must complete all PRACTICAL sessions and Workshop activities.
    MARKS will be calculated based on ELIGIBILITY criteria.
    
    Lab reservation is required for VIVA sessions.
    """
    
    result3 = classifier.classify_document(edge_sample)
    print(f"\nNote: Should be OFFICIAL (has mandatory phrase + MEDIUM boosters)")
    print(f"Got: {result3['classification']} ({result3['confidence']:.0%})")
    print(f"HIGH Boosters: {result3['high_booster_count']}")
    print(f"MEDIUM Boosters: {result3['medium_booster_count']}")
    print(f"LOW Boosters: {result3['low_booster_count']}")
    
    print("\n" + "="*60)
    print("TESTING COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    test_classifier()
