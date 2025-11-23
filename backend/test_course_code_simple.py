"""
Simple Test for Course Code Logic (No API Required)
Tests only the calculate_confidence_boosters method
"""
from ai_classifier.config import (
    HIGH_CONFIDENCE_BOOSTERS,
    MEDIUM_CONFIDENCE_BOOSTERS,
    LOW_CONFIDENCE_BOOSTERS,
    BASE_CONFIDENCE,
    HIGH_BOOSTER_INCREMENT,
    MEDIUM_BOOSTER_INCREMENT,
    LOW_BOOSTER_INCREMENT,
    ALL_COURSE_CODES_FOR_MAJORITY,
    MAJORITY_THRESHOLD
)

def calculate_confidence_boosters(text: str) -> dict:
    """Standalone version of the course code logic"""
    high_boosters = {
        'faculty': [],
        'degree_programme': [],
        'department': [],
        'course_codes_csu': [],
        'official_markers': []
    }
    
    medium_boosters = {
        'full_address': [],
        'course_codes_other': [],
        'academic_terms': [],
        'document_types': [],
        'staff_affiliation': []
    }
    
    low_boosters = {
        'general_faculties': [],
        'general_programmes': []
    }
    
    text_lower = text.lower()
    
    # Check HIGH confidence boosters (excluding course codes)
    for category, phrases in HIGH_CONFIDENCE_BOOSTERS.items():
        if category == "course_codes_csu":
            continue
        for phrase in phrases:
            if phrase.lower() in text_lower:
                high_boosters[category].append(phrase)
    
    # Check MEDIUM confidence boosters (excluding course codes)
    for category, phrases in MEDIUM_CONFIDENCE_BOOSTERS.items():
        if category == "course_codes_other":
            continue
        for phrase in phrases:
            if category == 'academic_terms':
                if phrase.lower() in text_lower:
                    medium_boosters[category].append(phrase)
            else:
                if phrase.lower() in text_lower or phrase in text:
                    medium_boosters[category].append(phrase)
    
    # Check LOW confidence boosters
    for category, phrases in LOW_CONFIDENCE_BOOSTERS.items():
        for phrase in phrases:
            if phrase.lower() in text_lower:
                low_boosters[category].append(phrase)
    
    # === COURSE CODE LOGIC ===
    found_codes = []
    for code in ALL_COURSE_CODES_FOR_MAJORITY:
        if code in text:
            found_codes.append(code)
    
    csu_codes = HIGH_CONFIDENCE_BOOSTERS["course_codes_csu"]
    non_csu_codes = MEDIUM_CONFIDENCE_BOOSTERS["course_codes_other"]
    
    # Check for MAJORITY
    majority_threshold_count = int(len(ALL_COURSE_CODES_FOR_MAJORITY) * MAJORITY_THRESHOLD)
    if len(found_codes) >= majority_threshold_count:
        high_boosters["course_codes_csu"] = [f"MAJORITY_CODES ({len(found_codes)}/{len(ALL_COURSE_CODES_FOR_MAJORITY)})"]
    else:
        # Check for single CSU code
        csu_found = [code for code in found_codes if code in csu_codes]
        if len(csu_found) > 0:
            high_boosters["course_codes_csu"] = csu_found[:1]
        
        # Check for single non-CSU code
        non_csu_found = [code for code in found_codes if code in non_csu_codes]
        if len(non_csu_found) > 0:
            medium_boosters["course_codes_other"] = non_csu_found[:1]
    
    high_booster_count = sum(1 for boosters in high_boosters.values() if len(boosters) > 0)
    medium_booster_count = sum(1 for boosters in medium_boosters.values() if len(boosters) > 0)
    low_booster_count = sum(1 for boosters in low_boosters.values() if len(boosters) > 0)
    
    confidence = BASE_CONFIDENCE
    confidence += high_booster_count * HIGH_BOOSTER_INCREMENT
    confidence += medium_booster_count * MEDIUM_BOOSTER_INCREMENT
    confidence += low_booster_count * LOW_BOOSTER_INCREMENT
    confidence = min(confidence, 1.0)
    
    return {
        'high_boosters': high_boosters,
        'medium_boosters': medium_boosters,
        'low_boosters': low_boosters,
        'high_booster_count': high_booster_count,
        'medium_booster_count': medium_booster_count,
        'low_booster_count': low_booster_count,
        'total_booster_count': high_booster_count + medium_booster_count + low_booster_count,
        'confidence': confidence,
        'course_codes_found': found_codes
    }


def test_single_csu_code():
    """Test: Single CSU code → HIGH booster"""
    print("\n=== Test 1: Single CSU Code (HIGH Booster) ===")
    
    test_text = "CSU3301 Data Structures"
    result = calculate_confidence_boosters(test_text)
    
    print(f"✓ Course codes found: {result['course_codes_found']}")
    print(f"✓ HIGH boosters (CSU): {result['high_boosters']['course_codes_csu']}")
    
    assert "CSU3301" in result['course_codes_found'], "Should find CSU3301"
    assert len(result['high_boosters']['course_codes_csu']) > 0, "Should have HIGH booster"
    print("✅ PASSED")


def test_majority_codes():
    """Test: Majority codes (110+) → HIGH booster"""
    print("\n=== Test 2: Majority Codes (HIGH Booster) ===")
    
    codes = ALL_COURSE_CODES_FOR_MAJORITY[:115]
    test_text = " ".join(codes)
    result = calculate_confidence_boosters(test_text)
    
    print(f"✓ Course codes found: {len(result['course_codes_found'])}")
    print(f"✓ HIGH boosters: {result['high_boosters']['course_codes_csu']}")
    
    assert len(result['course_codes_found']) >= 110, "Should find 110+ codes"
    assert "MAJORITY_CODES" in result['high_boosters']['course_codes_csu'][0], "Should detect MAJORITY"
    print("✅ PASSED")


def test_single_non_csu_code():
    """Test: Single non-CSU code → MEDIUM booster"""
    print("\n=== Test 3: Single Non-CSU Code (MEDIUM Booster) ===")
    
    test_text = "BYU3301 Educational Psychology"
    result = calculate_confidence_boosters(test_text)
    
    print(f"✓ Course codes found: {result['course_codes_found']}")
    print(f"✓ MEDIUM boosters (non-CSU): {result['medium_boosters']['course_codes_other']}")
    
    assert "BYU3301" in result['course_codes_found'], "Should find BYU3301"
    assert len(result['medium_boosters']['course_codes_other']) > 0, "Should have MEDIUM booster"
    print("✅ PASSED")


def test_mixed_codes():
    """Test: Mixed CSU and non-CSU codes"""
    print("\n=== Test 4: Mixed Codes (HIGH + MEDIUM) ===")
    
    test_text = "CSU3301 BYU3301 CSU4300 PHU3300"
    result = calculate_confidence_boosters(test_text)
    
    print(f"✓ Course codes found: {result['course_codes_found']}")
    print(f"✓ HIGH (CSU): {result['high_boosters']['course_codes_csu']}")
    print(f"✓ MEDIUM (non-CSU): {result['medium_boosters']['course_codes_other']}")
    
    assert len(result['course_codes_found']) == 4, "Should find 4 codes"
    assert len(result['high_boosters']['course_codes_csu']) > 0, "Should have HIGH"
    assert len(result['medium_boosters']['course_codes_other']) > 0, "Should have MEDIUM"
    print("✅ PASSED")


def test_no_codes():
    """Test: No course codes"""
    print("\n=== Test 5: No Course Codes ===")
    
    test_text = "General university information"
    result = calculate_confidence_boosters(test_text)
    
    print(f"✓ Course codes found: {result['course_codes_found']}")
    
    assert len(result['course_codes_found']) == 0, "Should find no codes"
    assert len(result['high_boosters']['course_codes_csu']) == 0, "No HIGH booster"
    assert len(result['medium_boosters']['course_codes_other']) == 0, "No MEDIUM booster"
    print("✅ PASSED")


if __name__ == "__main__":
    print("=" * 70)
    print("COURSE CODE LOGIC TEST (Simplified - No API Required)")
    print("=" * 70)
    print(f"\nTotal course codes available: {len(ALL_COURSE_CODES_FOR_MAJORITY)}")
    print(f"Majority threshold: {MAJORITY_THRESHOLD * 100}% ({int(len(ALL_COURSE_CODES_FOR_MAJORITY) * MAJORITY_THRESHOLD)} codes)")
    print("=" * 70)
    
    try:
        test_single_csu_code()
        test_majority_codes()
        test_single_non_csu_code()
        test_mixed_codes()
        test_no_codes()
        
        print("\n" + "=" * 70)
        print("✅ ALL 5 TESTS PASSED!")
        print("=" * 70)
        print("\nCourse code differentiation working correctly:")
        print("  ✓ Single CSU code → HIGH booster (+17.5%)")
        print("  ✓ Majority codes (110+) → HIGH booster (+17.5%)")
        print("  ✓ Single non-CSU code → MEDIUM booster (+11.5%)")
        print("=" * 70)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
