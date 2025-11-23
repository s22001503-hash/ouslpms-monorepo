"""
Test Suite for Course Code Classification Logic
Tests the differentiation between single CSU codes, majority codes, and single non-CSU codes
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

def test_single_csu_code():
    """Test: Single CSU code in document → HIGH booster"""
    print("\n=== Test 1: Single CSU Code (HIGH Booster) ===")
    
    test_text = """
    The Open University of Sri Lanka
    FACULTY OF NATURAL SCIENCE
    Department of Computer Science
    
    Course: CSU3301 - Data Structures and Algorithms
    Semester: 2024/2025
    """
    
    from classifier import DocumentClassifier
    classifier = DocumentClassifier()
    
    # Check mandatory phrase
    mandatory = classifier.check_mandatory_requirement(test_text)
    print(f"✓ Mandatory phrase found: {mandatory}")
    assert mandatory, "OUSL phrase must be present"
    
    # Calculate boosters
    booster_info = classifier.calculate_confidence_boosters(test_text)
    
    print(f"✓ Course codes found: {booster_info['course_codes_found']}")
    print(f"✓ HIGH boosters count: {booster_info['high_booster_count']}")
    print(f"✓ Course codes in HIGH: {booster_info['high_boosters']['course_codes_csu']}")
    
    # Assertions
    assert "CSU3301" in booster_info['course_codes_found'], "Should find CSU3301"
    assert len(booster_info['high_boosters']['course_codes_csu']) > 0, "Should have HIGH booster for CSU code"
    assert "CSU3301" in booster_info['high_boosters']['course_codes_csu'][0], "Should contain CSU3301"
    
    print("✅ Test 1 PASSED: Single CSU code detected as HIGH booster")


def test_majority_codes():
    """Test: Majority (50%+) of all 220 codes in document → HIGH booster"""
    print("\n=== Test 2: Majority Codes (HIGH Booster) ===")
    
    from config import ALL_COURSE_CODES_FOR_MAJORITY
    
    # Create document with 110+ course codes (50%+)
    majority_codes = ALL_COURSE_CODES_FOR_MAJORITY[:115]  # Take first 115 codes
    codes_text = ", ".join(majority_codes)
    
    test_text = f"""
    The Open University of Sri Lanka
    Complete Course Catalog - All Programmes
    
    {codes_text}
    
    This document contains all available courses across all faculties.
    """
    
    from classifier import DocumentClassifier
    classifier = DocumentClassifier()
    
    # Check mandatory phrase
    mandatory = classifier.check_mandatory_requirement(test_text)
    print(f"✓ Mandatory phrase found: {mandatory}")
    assert mandatory, "OUSL phrase must be present"
    
    # Calculate boosters
    booster_info = classifier.calculate_confidence_boosters(test_text)
    
    print(f"✓ Course codes found: {len(booster_info['course_codes_found'])}/{len(ALL_COURSE_CODES_FOR_MAJORITY)}")
    print(f"✓ HIGH boosters count: {booster_info['high_booster_count']}")
    print(f"✓ Course codes in HIGH: {booster_info['high_boosters']['course_codes_csu']}")
    
    # Assertions
    assert len(booster_info['course_codes_found']) >= 110, "Should find 110+ codes"
    assert "MAJORITY_CODES" in booster_info['high_boosters']['course_codes_csu'][0], "Should detect MAJORITY_CODES"
    
    print("✅ Test 2 PASSED: Majority codes detected as HIGH booster")


def test_single_non_csu_code():
    """Test: Single non-CSU code in document → MEDIUM booster"""
    print("\n=== Test 3: Single Non-CSU Code (MEDIUM Booster) ===")
    
    test_text = """
    The Open University of Sri Lanka
    Faculty of Education
    
    Course: BYU3301 - Educational Psychology
    Semester 2, 2024/2025
    """
    
    from classifier import DocumentClassifier
    classifier = DocumentClassifier()
    
    # Check mandatory phrase
    mandatory = classifier.check_mandatory_requirement(test_text)
    print(f"✓ Mandatory phrase found: {mandatory}")
    assert mandatory, "OUSL phrase must be present"
    
    # Calculate boosters
    booster_info = classifier.calculate_confidence_boosters(test_text)
    
    print(f"✓ Course codes found: {booster_info['course_codes_found']}")
    print(f"✓ MEDIUM boosters count: {booster_info['medium_booster_count']}")
    print(f"✓ Course codes in MEDIUM: {booster_info['medium_boosters']['course_codes_other']}")
    
    # Assertions
    assert "BYU3301" in booster_info['course_codes_found'], "Should find BYU3301"
    assert len(booster_info['medium_boosters']['course_codes_other']) > 0, "Should have MEDIUM booster for non-CSU code"
    assert "BYU3301" in booster_info['medium_boosters']['course_codes_other'][0], "Should contain BYU3301"
    
    print("✅ Test 3 PASSED: Single non-CSU code detected as MEDIUM booster")


def test_mixed_codes():
    """Test: Mixed CSU and non-CSU codes (both HIGH and MEDIUM boosters)"""
    print("\n=== Test 4: Mixed Codes (HIGH + MEDIUM Boosters) ===")
    
    test_text = """
    The Open University of Sri Lanka
    BACHELOR OF SCIENCE DEGREE PROGRAMME
    Department of Computer Science
    
    Available Courses:
    - CSU3301: Data Structures
    - BYU3301: Educational Psychology
    - CSU4300: Software Engineering
    - PHU3300: Health Sciences
    """
    
    from classifier import DocumentClassifier
    classifier = DocumentClassifier()
    
    # Check mandatory phrase
    mandatory = classifier.check_mandatory_requirement(test_text)
    print(f"✓ Mandatory phrase found: {mandatory}")
    assert mandatory, "OUSL phrase must be present"
    
    # Calculate boosters
    booster_info = classifier.calculate_confidence_boosters(test_text)
    
    print(f"✓ Course codes found: {booster_info['course_codes_found']}")
    print(f"✓ HIGH boosters (CSU): {booster_info['high_boosters']['course_codes_csu']}")
    print(f"✓ MEDIUM boosters (non-CSU): {booster_info['medium_boosters']['course_codes_other']}")
    
    # Assertions
    assert len(booster_info['course_codes_found']) == 4, "Should find 4 codes"
    assert len(booster_info['high_boosters']['course_codes_csu']) > 0, "Should have HIGH booster for CSU"
    assert len(booster_info['medium_boosters']['course_codes_other']) > 0, "Should have MEDIUM booster for non-CSU"
    
    print("✅ Test 4 PASSED: Mixed codes properly categorized")


def test_no_course_codes():
    """Test: No course codes in document → No course code boosters"""
    print("\n=== Test 5: No Course Codes (No Code Boosters) ===")
    
    test_text = """
    The Open University of Sri Lanka
    Faculty of Humanities and Social Sciences
    
    This is a general information document about the university.
    No specific courses are mentioned.
    """
    
    from classifier import DocumentClassifier
    classifier = DocumentClassifier()
    
    # Check mandatory phrase
    mandatory = classifier.check_mandatory_requirement(test_text)
    print(f"✓ Mandatory phrase found: {mandatory}")
    assert mandatory, "OUSL phrase must be present"
    
    # Calculate boosters
    booster_info = classifier.calculate_confidence_boosters(test_text)
    
    print(f"✓ Course codes found: {booster_info['course_codes_found']}")
    print(f"✓ HIGH course code boosters: {booster_info['high_boosters']['course_codes_csu']}")
    print(f"✓ MEDIUM course code boosters: {booster_info['medium_boosters']['course_codes_other']}")
    
    # Assertions
    assert len(booster_info['course_codes_found']) == 0, "Should find no codes"
    assert len(booster_info['high_boosters']['course_codes_csu']) == 0, "Should have no HIGH course code booster"
    assert len(booster_info['medium_boosters']['course_codes_other']) == 0, "Should have no MEDIUM course code booster"
    
    print("✅ Test 5 PASSED: No course codes detected correctly")


if __name__ == "__main__":
    print("=" * 70)
    print("COURSE CODE CLASSIFICATION LOGIC TEST SUITE")
    print("=" * 70)
    print("\nTesting the differentiation between:")
    print("1. Single CSU code (CSU3200-CSU5320) → HIGH booster (+17.5%)")
    print("2. Majority codes (50%+ of 220 codes) → HIGH booster (+17.5%)")
    print("3. Single non-CSU code (BYU, CYU, PHU, etc.) → MEDIUM booster (+11.5%)")
    print("=" * 70)
    
    try:
        test_single_csu_code()
        test_majority_codes()
        test_single_non_csu_code()
        test_mixed_codes()
        test_no_course_codes()
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS PASSED!")
        print("=" * 70)
        print("\nCourse code classification logic is working correctly.")
        print("The system can now differentiate between:")
        print("  • Single CSU codes (HIGH)")
        print("  • Comprehensive course catalogs with 50%+ codes (HIGH)")
        print("  • Single non-CSU codes (MEDIUM)")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
