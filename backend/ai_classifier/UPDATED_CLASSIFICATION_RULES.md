# AI Document Classifier - Updated Classification Rules

## 📋 MANDATORY CLASSIFICATION RULE (THUMB RULE)

### The Absolute Requirement

A document is classified as **OFFICIAL** if and only if it contains **at least ONE** of these exact phrases:

1. `"The Open University of Sri Lanka"` (any capitalization)
2. `"THE OPEN UNIVERSITY OF SRI LANKA"` (all caps)

**This is ABSOLUTELY REQUIRED and NON-NEGOTIABLE.**

### Decision Logic

```
IF document contains OUSL name:
    → Classify as OFFICIAL
    → Calculate confidence with boosters (70% base + boosters)
    
ELSE (no OUSL name found):
    → Classify as PERSONAL
    → Confidence: 85-95%
    → No further analysis needed
```

---

## 🎯 THREE-TIER CONFIDENCE BOOSTER SYSTEM

When the mandatory OUSL phrase **IS PRESENT**, these additional markers increase classification confidence:

### 🔴 HIGH CONFIDENCE BOOSTERS (+15-20% each)

**Impact**: +17.5% per category matched

**Categories**:

1. **Faculty Names** (specific named faculties):
   - FACULTY OF NATURAL SCIENCE
   - Faculty of Engineering Technology
   - Faculty of Humanities and Social Sciences
   - Faculty of Education
   - Faculty of Health Sciences
   - Faculty of Engineering
   - Faculty of Management and Commerce
   - Faculty of Health Sciences and Allied Health Sciences
   - Faculty of Computing
   - Faculty of Science

2. **Degree Programmes** (specific degree titles):
   - BACHELOR OF SCIENCE DEGREE PROGRAMME
   - Bachelor of Technology Honours
   - Bachelor of Software Engineering Honours
   - Bachelor of Science Honours in Engineering
   - Bachelor of Laws (LLB) Honours
   - Bachelor of Arts in Social Sciences
   - Bachelor of Business Management (BMS) Honours
   - Master of Science
   - And more...

3. **Department Names**:
   - Department of Computer Science
   - Department of Electrical and Computer Engineering
   - Department of Mathematics and Philosophy of Engineering
   - Department of Mechanical Engineering

4. **Course Codes (CSU Series)**: 
   - CSU3200, CSU3301, CSU3302
   - CSU4300, CSU4301, CSU4302, CSU4303
   - CSU5300-CSU5320 (full range)

5. **Official Markers**:
   - University seal
   - Official letterhead
   - University logo

---

### 🟡 MEDIUM CONFIDENCE BOOSTERS (+8-15% each)

**Impact**: +11.5% per category matched

**Categories**:

1. **Full Address**:
   - "PO Box 21, The Open University of Sri Lanka, Nawala, Nugegoda"
   - "P.O. Box 21"
   - "Nawala, Nugegoda"

2. **Course Codes (Other Series)** - 200+ codes:
   - **BYU Series**: BYU3301, BYU3500, BYU4300-BYU4303, BYU5302-BYU5318
   - **CYU Series**: CYU3300, CYU3201, CYU3302, CYU4300-CYU4303, CYU5300-CYU5615
   - **PHU Series**: PHU3300-PHU3202, PHU4300-PHU4303, PHU5300-PHU5318
   - **ZYU Series**: ZYU3500, ZYU3301, ZYU4300-ZYU4303, ZYU5300-ZYU5315
   - **ADU Series**: ADU3300-ADU3218, ADU4300-ADU4303, ADU5300-ADU5321
   - **PEU Series**: PEU3300-PEU3202, PEU4300-PEU4303, PEU5300-PEU5307
   - **Misc**: ADE3200, CYE3200, LTE34GE, FDE3021, CSE3214, LLU3261, OSU3208, DSU3298, FNU3200

3. **Academic Terms** (case-insensitive):
   - Academic years: 2024/2025, 2023/2024
   - Semesters: "Semester 1", "semester 2"
   - Assessments: "CAT 1", "CAT 2", "OBT", "NBT"
   - Terms: "ELIGIBILITY", "MARKS", "PRACTICAL"
   - Activities: "Workshop", "VIVA", "Lab reservation"

4. **Document Types**:
   - Syllabus, Transcript, Certificate
   - Assignment, Research Paper
   - MTT, Tentative, Course Outline
   - Examination, Assessment

5. **Staff Affiliation**:
   - Lecturer, Senior Lecturer, Professor
   - "Dr." with OUSL context
   - "OUSL affiliation"
   - "Department of" (when with names)

---

### 🟢 LOW CONFIDENCE BOOSTERS (+1-7% each)

**Impact**: +4% per category matched

**Categories**:

1. **General Faculty References**:
   - Faculty of Engineering
   - Faculty of Humanities and Social Sciences
   - Faculty of Management and Commerce
   - Faculty of Health Sciences and Allied Health Sciences
   - Faculty of Education
   - Faculty of Computing
   - Faculty of Science

2. **General Programme References**:
   - Civil Engineering, Mechanical Engineering
   - Computer Engineering, Electrical & Electronic Engineering
   - Fashion Design, Textile Manufacture
   - Marketing Management, Special Needs Education
   - Laboratory Technology, Food Science
   - Physics, Chemistry, Zoology, Botany, Mathematics

---

## 📊 CONFIDENCE CALCULATION

### Formula

```
Base Confidence (when OUSL name found): 70%

Final Confidence = Base + (HIGH × 17.5%) + (MEDIUM × 11.5%) + (LOW × 4%)

Maximum: 100% (capped)
```

### Examples

**Example 1: Maximum Confidence**
```
Document contains:
✅ "The Open University of Sri Lanka" (mandatory)
✅ "FACULTY OF NATURAL SCIENCE" (HIGH: +17.5%)
✅ "BACHELOR OF SCIENCE DEGREE PROGRAMME" (HIGH: +17.5%)
✅ "Department of Computer Science" (HIGH: +17.5%)
✅ "CSU3200" (HIGH: +17.5%)
✅ "2024/2025" (MEDIUM: +11.5%)
✅ "Syllabus" (MEDIUM: +11.5%)

Calculation:
70% + (4 × 17.5%) + (2 × 11.5%) = 70% + 70% + 23% = 163% → Capped at 100%
```

**Example 2: High Confidence**
```
Document contains:
✅ "The Open University of Sri Lanka" (mandatory)
✅ "Faculty of Engineering" (LOW: +4%)
✅ "Bachelor of Technology Honours" (HIGH: +17.5%)
✅ "BYU3301" (MEDIUM: +11.5%)
✅ "Semester 1" (MEDIUM: +11.5%)

Calculation:
70% + (1 × 17.5%) + (2 × 11.5%) + (1 × 4%) = 70% + 17.5% + 23% + 4% = 114.5% → Capped at 100%
```

**Example 3: Base Confidence Only**
```
Document contains:
✅ "THE OPEN UNIVERSITY OF SRI LANKA" (mandatory only)
❌ No boosters found

Calculation:
70% + 0% = 70%
```

**Example 4: Personal Document**
```
Document contains:
❌ No OUSL name
(Doesn't matter what else is in the document)

Result:
PERSONAL (85-95% confidence)
```

---

## 🔍 Special Considerations

### Case Sensitivity

- **Mandatory phrase**: Case-insensitive search
- **HIGH boosters**: Case-insensitive search
- **MEDIUM boosters**: 
  - Academic terms: **Case-insensitive** (as specified)
  - Others: Case-sensitive or case-insensitive depending on context
- **LOW boosters**: Case-insensitive search

### Course Code Matching

All course codes are matched **exactly** as listed:
- CSU series (20 codes)
- Other series (200+ codes including BYU, CYU, PHU, ZYU, ADU, PEU)

**Example matches**:
```
✅ "Course Code: CSU3200" → Matches HIGH booster
✅ "BYU3301 - Biology" → Matches MEDIUM booster
✅ "PHU5318 assignment" → Matches MEDIUM booster
❌ "CSU9999" → No match (not in list)
```

### Academic Terms

**All case variations accepted** for academic terms:
```
✅ "Semester 1" → Matches
✅ "semester 2" → Matches
✅ "SEMESTER 1" → Matches
✅ "CAT 1" → Matches
✅ "cat 2" → Matches
✅ "PRACTICAL" → Matches
✅ "practical" → Matches
```

---

## 🎓 Classification Examples

### Example 1: Syllabus (HIGH confidence)

```text
The Open University of Sri Lanka
FACULTY OF NATURAL SCIENCE
Department of Computer Science

Course Code: CSU3200
BACHELOR OF SCIENCE DEGREE PROGRAMME

Academic Year: 2024/2025
Semester: 1
Assessment: CAT 1, CAT 2, PRACTICAL
```

**Classification**:
- ✅ Mandatory: Yes
- HIGH: 3 (Faculty, Department, Course Code)
- MEDIUM: 3 (Academic year, Semester, CAT)
- LOW: 0
- **Result**: OFFICIAL (100%)

---

### Example 2: Transcript (MEDIUM-HIGH confidence)

```text
THE OPEN UNIVERSITY OF SRI LANKA
Student Transcript

Name: John Doe
Programme: Bachelor of Arts in Social Sciences
Course: BYU3301 - Biology
Semester: 2023/2024 Semester 2
MARKS: 75/100
ELIGIBILITY: Passed
```

**Classification**:
- ✅ Mandatory: Yes
- HIGH: 1 (Degree programme)
- MEDIUM: 4 (Course code, Academic year, MARKS, ELIGIBILITY)
- LOW: 0
- **Result**: OFFICIAL (93.5%)

---

### Example 3: Personal Blog Post

```text
My Experience at Universities

I've been researching distance education in Sri Lanka.
The Open University of Sri Lanka offers flexible programs.

In my opinion, online learning is the future. Many students
appreciate the convenience of studying from home.

This is just my personal blog about education trends.
```

**Classification**:
- ✅ Mandatory: Yes (mentions OUSL)
- HIGH: 0
- MEDIUM: 0
- LOW: 0
- **Result**: OFFICIAL (70% - base only)

**Note**: This would be classified as OFFICIAL because it contains the mandatory phrase, even though it's clearly a personal blog. This is by design - the thumb rule is absolute.

---

### Example 4: Personal Letter

```text
Dear Sarah,

I hope this finds you well. I wanted to share my thoughts
about the novel I've been reading. It's quite fascinating!

I'm also planning a trip next month. Would you like to join?

Best regards,
Emily
```

**Classification**:
- ❌ Mandatory: No
- **Result**: PERSONAL (90%)

---

## 🛠️ Implementation Details

### Updated Files

1. **config.py**:
   - Added three-tier booster dictionaries
   - Updated confidence calculation parameters
   - Added 200+ course codes

2. **classifier.py**:
   - Updated `calculate_confidence_boosters()` method
   - Three-tier scoring system
   - Enhanced prompt with detailed rules
   - Updated result format

3. **test_classifier.py**:
   - New test cases for three-tier system
   - Enhanced result display

### Configuration Parameters

```python
# Base confidence when mandatory phrase found
BASE_CONFIDENCE = 0.70  # 70%

# Booster increments
HIGH_BOOSTER_INCREMENT = 0.175   # +17.5% (avg of 15-20%)
MEDIUM_BOOSTER_INCREMENT = 0.115 # +11.5% (avg of 8-15%)
LOW_BOOSTER_INCREMENT = 0.04     # +4% (avg of 1-7%)
```

---

## 📈 Expected Accuracy

With the three-tier system:

- **High-quality OUSL documents**: 95-100% confidence
- **Standard OUSL documents**: 85-95% confidence
- **Basic OUSL documents**: 70-85% confidence
- **Personal documents**: 85-95% confidence (PERSONAL)

---

## 🔧 Testing

Run the updated test script:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python ai_classifier/test_classifier.py
```

Expected output shows three-tier booster breakdown for each test case.

---

## 📚 Summary

### Key Changes

✅ Mandatory rule unchanged (OUSL name required)
✅ Base confidence lowered to 70% (from 80%)
✅ Three-tier booster system implemented
✅ 200+ course codes added (CSU, BYU, CYU, PHU, ZYU, ADU, PEU series)
✅ Academic terms case-insensitive
✅ More granular confidence calculation
✅ Better distinction between document types

### Benefits

🎯 More accurate confidence scoring
🎯 Better handling of different document types
🎯 Comprehensive course code coverage
🎯 Flexible academic term matching
🎯 Clear booster hierarchy

---

**Last Updated**: November 23, 2025
**Version**: 2.0 (Three-Tier Booster System)
