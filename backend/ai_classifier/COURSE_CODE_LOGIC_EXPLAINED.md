# Course Code Classification Logic Explained

## Overview
The AI document classifier now implements sophisticated course code detection to differentiate between:
1. **Single CSU codes** in regular documents (e.g., syllabi)
2. **Majority codes** in comprehensive course catalogs
3. **Single non-CSU codes** in other documents

## Course Code Categories

### CSU Codes (Computer Science Unit - 20 codes)
```
CSU3200, CSU3301, CSU3302, CSU4300, CSU4301, CSU4302, CSU4303,
CSU5300, CSU5301, CSU5302, CSU5303, CSU5304, CSU5305, CSU5306,
CSU5312, CSU5308, CSU5309, CSU5310, CSU5311, CSU5320
```
**Usage**: Found in Computer Science department syllabi, course outlines, transcripts

### Non-CSU Codes (200 codes across multiple units)
```
BYU (Bachelor of Education), CYU (Communication), PHU (Public Health),
ZYU (Zoology), ADU (Administration), PEU (Physical Education), 
and many more...
```
**Usage**: Found in other faculty syllabi, transcripts, course materials

### All Course Codes (220 total)
Combined list of all CSU + non-CSU codes for majority detection

## Classification Rules

### Rule 1: Single CSU Code → HIGH Booster (+17.5%)
**Trigger**: Document contains ONE OR MORE CSU codes (CSU3200-CSU5320)  
**Confidence**: +17.5% (HIGH tier)

**Example**:
```
The Open University of Sri Lanka
Department of Computer Science
Course: CSU3301 - Data Structures
Semester: 2024/2025
```
**Result**: HIGH booster applied (1 CSU code detected)

**Why HIGH?**  
- CSU codes strongly indicate official Computer Science documents
- Most likely a course syllabus, outline, or transcript
- Directly from the Computer Science department

---

### Rule 2: Majority Codes → HIGH Booster (+17.5%)
**Trigger**: Document contains 50%+ of ALL 220 course codes (110+ codes)  
**Confidence**: +17.5% (HIGH tier)

**Example**:
```
The Open University of Sri Lanka
Complete Course Catalog 2024/2025

CSU3200, CSU3301, CSU3302, BYU3301, BYU3500, CYU3300, CYU3201,
PHU3300, PHU3301, ZYU3500, ADU3300, PEU3300, ... (110+ codes)

This document contains all available courses across all faculties.
```
**Result**: HIGH booster applied (MAJORITY_CODES detected)

**Why HIGH?**  
- Comprehensive course catalogs are official university documents
- Only OUSL publishes complete lists of 100+ course codes
- Strong indicator of official document type (catalog, handbook, etc.)

**Threshold**: 50% of 220 codes = 110 codes minimum

---

### Rule 3: Single Non-CSU Code → MEDIUM Booster (+11.5%)
**Trigger**: Document contains ONE OR MORE non-CSU codes (BYU, CYU, PHU, etc.)  
**Confidence**: +11.5% (MEDIUM tier)

**Example**:
```
The Open University of Sri Lanka
Faculty of Education
Course: BYU3301 - Educational Psychology
Semester 2, 2024/2025
```
**Result**: MEDIUM booster applied (1 non-CSU code detected)

**Why MEDIUM?**  
- Non-CSU codes are still official but from other departments
- Slightly lower confidence than CSU codes
- Still indicates official course materials

---

## Logic Flow

```
1. Extract all course codes from document text (case-sensitive)
   ↓
2. Count total codes found
   ↓
3. Check: Does document have 110+ codes (50% threshold)?
   YES → Apply HIGH booster (MAJORITY_CODES)
   NO  → Continue to next check
   ↓
4. Check: Does document have any CSU codes?
   YES → Apply HIGH booster (single CSU code)
   NO  → Continue to next check
   ↓
5. Check: Does document have any non-CSU codes?
   YES → Apply MEDIUM booster (single non-CSU code)
   NO  → No course code booster applied
```

## Implementation Details

### Config File (`config.py`)
```python
# HIGH CONFIDENCE BOOSTERS
HIGH_CONFIDENCE_BOOSTERS = {
    "course_codes_csu": [
        "CSU3200", "CSU3301", "CSU3302", ...
    ]
}

# MEDIUM CONFIDENCE BOOSTERS
MEDIUM_CONFIDENCE_BOOSTERS = {
    "course_codes_other": [
        "BYU3301", "BYU3500", "CYU3300", ...
    ]
}

# ALL COURSE CODES (for majority detection)
ALL_COURSE_CODES_FOR_MAJORITY = [
    # CSU codes (20 codes)
    "CSU3200", "CSU3301", ...,
    # Non-CSU codes (200 codes)
    "BYU3301", "CYU3300", ...
]

MAJORITY_THRESHOLD = 0.5  # 50%
```

### Classifier Logic (`classifier.py`)
```python
def calculate_confidence_boosters(self, text: str) -> Dict:
    # Find all course codes in document
    found_codes = []
    for code in ALL_COURSE_CODES_FOR_MAJORITY:
        if code in text:  # Case-sensitive
            found_codes.append(code)
    
    # Check for MAJORITY (50%+)
    majority_count = int(len(ALL_COURSE_CODES_FOR_MAJORITY) * MAJORITY_THRESHOLD)
    if len(found_codes) >= majority_count:
        high_boosters["course_codes_csu"] = [f"MAJORITY_CODES ({len(found_codes)}/220)"]
    else:
        # Check for single CSU code
        csu_found = [code for code in found_codes if code in csu_codes]
        if len(csu_found) > 0:
            high_boosters["course_codes_csu"] = csu_found[:1]
        
        # Check for single non-CSU code
        non_csu_found = [code for code in found_codes if code in non_csu_codes]
        if len(non_csu_found) > 0:
            medium_boosters["course_codes_other"] = non_csu_found[:1]
```

## Test Cases

### Test 1: Single CSU Code (HIGH)
**Input**: Document with "CSU3301"  
**Expected**: HIGH booster (+17.5%)  
**Actual**: ✅ PASSED

### Test 2: Majority Codes (HIGH)
**Input**: Document with 115+ course codes  
**Expected**: HIGH booster (+17.5%, MAJORITY_CODES)  
**Actual**: ✅ PASSED

### Test 3: Single Non-CSU Code (MEDIUM)
**Input**: Document with "BYU3301"  
**Expected**: MEDIUM booster (+11.5%)  
**Actual**: ✅ PASSED

### Test 4: Mixed Codes (HIGH + MEDIUM)
**Input**: Document with CSU3301, BYU3301, CSU4300, PHU3300  
**Expected**: HIGH booster for CSU + MEDIUM booster for non-CSU  
**Actual**: ✅ PASSED

### Test 5: No Course Codes
**Input**: Document with no course codes  
**Expected**: No course code boosters  
**Actual**: ✅ PASSED

## Edge Cases

### Case 1: Document with OUSL name + Single CSU code
```
Confidence Calculation:
Base: 70%
+ HIGH (Faculty): +17.5%
+ HIGH (CSU code): +17.5%
= 105% → Capped at 100%
```

### Case 2: Document with OUSL name + Majority codes
```
Confidence Calculation:
Base: 70%
+ HIGH (MAJORITY_CODES): +17.5%
+ HIGH (Faculty): +17.5%
= 105% → Capped at 100%
```

### Case 3: Document with OUSL name + Single non-CSU code
```
Confidence Calculation:
Base: 70%
+ MEDIUM (non-CSU code): +11.5%
+ MEDIUM (Semester info): +11.5%
= 93%
```

### Case 4: Document with OUSL name only (no codes)
```
Confidence Calculation:
Base: 70%
+ HIGH (Faculty): +17.5%
= 87.5%
```

## Benefits of This Approach

1. **Precise Differentiation**
   - Distinguishes between regular syllabi (1 code) and course catalogs (100+ codes)
   - Both receive HIGH confidence, but for different reasons

2. **Flexible Handling**
   - Single CSU code → Strong indicator of CS department official doc
   - Comprehensive catalog → Strong indicator of official university-wide doc
   - Single non-CSU code → Moderate indicator of other department doc

3. **Prevents False Positives**
   - Student notes mentioning multiple course codes won't trigger MAJORITY (need 50%+)
   - Personal documents with 1-2 codes get appropriate MEDIUM confidence

4. **Scalable**
   - Easy to add new course codes to the lists
   - Threshold can be adjusted (currently 50%)
   - Logic works for any number of codes

## Future Enhancements

1. **Dynamic Threshold**: Adjust majority threshold based on document type
2. **Code Frequency**: Weight codes by frequency in document
3. **Code Context**: Check if codes appear in official context (syllabus headers, etc.)
4. **Faculty-Specific Codes**: Different confidence levels for different faculty codes

## Summary

The course code classification logic now provides:
- ✅ **Single CSU code detection** → HIGH booster
- ✅ **Majority code detection** (50%+) → HIGH booster
- ✅ **Single non-CSU code detection** → MEDIUM booster
- ✅ **Proper differentiation** between regular syllabi and comprehensive catalogs
- ✅ **Comprehensive test suite** to validate all scenarios

This sophisticated logic ensures accurate classification of diverse document types while maintaining high precision and preventing false positives.
