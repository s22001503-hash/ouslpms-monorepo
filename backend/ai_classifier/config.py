"""
Configuration for AI Document Classifier
"""
import os
from pathlib import Path

# ===================================================================
# Paths
# ===================================================================
# Path structure: ai_classifier/config.py -> backend -> ouslpms-monorepo -> OCT project
BASE_DIR = Path(__file__).parent.parent.parent.parent  # Go up to "OCT project" directory
TRAINING_DATA_DIR = BASE_DIR / "training_documents"
OFFICIAL_DIR = TRAINING_DATA_DIR / "official"
PERSONAL_DIR = TRAINING_DATA_DIR / "personal"
CHROMA_DB_DIR = Path(__file__).parent / "chroma_db"

# ===================================================================
# ChromaDB Settings
# ===================================================================
COLLECTION_NAME = "ousl_document_classifier"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ===================================================================
# Document Processing Settings
# ===================================================================
CHUNK_SIZE = 500  # characters per chunk
CHUNK_OVERLAP = 50  # overlap between chunks
MAX_CHUNKS_PER_DOC = 20  # limit chunks to prevent overwhelming

# ===================================================================
# Classification Settings
# ===================================================================
# === MANDATORY CLASSIFICATION RULE (THUMB RULE) ===
# A document is OFFICIAL IF AND ONLY IF it contains at least ONE of these
MANDATORY_PHRASE = "The Open University of Sri Lanka"
MANDATORY_PHRASE_ALT = "THE OPEN UNIVERSITY OF SRI LANKA"

# === OPTIONAL CONFIDENCE BOOSTERS ===
# If the mandatory OUSL name IS present, these markers increase confidence

# HIGH CONFIDENCE BOOSTERS (+15-20% each)
HIGH_CONFIDENCE_BOOSTERS = {
    "faculty": [
        "FACULTY OF NATURAL SCIENCE",
        "Faculty of Natural Science",
        "Faculty of Engineering Technology",
        "Faculty of Humanities and Social Sciences",
        "Faculty of Education",
        "Faculty of Health Sciences",
        "Faculty of Engineering",
        "Faculty of Management and Commerce",
        "Faculty of Health Sciences and Allied Health Sciences",
        "Faculty of Computing",
        "Faculty of Science"
    ],
    "degree_programme": [
        "BACHELOR OF SCIENCE DEGREE PROGRAMME",
        "Bachelor of Science Degree Programme",
        "Bachelor of Technology Honours",
        "Bachelor of Software Engineering Honours",
        "Bachelor of Science Honours in Engineering",
        "Bachelor of Laws (LLB) Honours",
        "Bachelor of Arts in Social Sciences",
        "Bachelor of Arts in English and English Language Teaching",
        "Bachelor of Science Honours in Psychology",
        "Bachelor of Business Management (BMS) Honours",
        "Bachelor of Industrial Studies Honours",
        "Bachelor of Science Honours in Nursing",
        "Bachelor of Medical Laboratory Sciences Honours",
        "Master of Science in Nursing",
        "Bachelor of Education Honours",
        "Advanced Certificate In Pre-school Education",
        "Bachelor of Science (General)",
        "Master of Science",
        "Postgraduate Diploma"
    ],
    "department": [
        "Department of Computer Science",
        "Department of Electrical and Computer Engineering",
        "Department of Mathematics and Philosophy of Engineering",
        "Department of Mechanical Engineering"
    ],
    # Single CSU code in document → HIGH booster
    "course_codes_csu": [
        "CSU3200", "CSU3301", "CSU3302", "CSU4300", "CSU4301", "CSU4302", 
        "CSU4303", "CSU5300", "CSU5301", "CSU5302", "CSU5303", "CSU5304", 
        "CSU5305", "CSU5306", "CSU5312", "CSU5308", "CSU5309", "CSU5310", 
        "CSU5311", "CSU5320"
    ],
    "official_markers": [
        "University seal",
        "Official letterhead",
        "university logo"
    ]
}

# ALL COURSE CODES for majority detection (50%+ in document → HIGH booster)
ALL_COURSE_CODES_FOR_MAJORITY = [
    # CSU codes (20 codes)
    "CSU3200", "CSU3301", "CSU3302", "CSU4300", "CSU4301", "CSU4302", 
    "CSU4303", "CSU5300", "CSU5301", "CSU5302", "CSU5303", "CSU5304", 
    "CSU5305", "CSU5306", "CSU5312", "CSU5308", "CSU5309", "CSU5310", 
    "CSU5311", "CSU5320",
    # Non-CSU codes (200 codes)
    "BYU3301", "BYU3500", "CYU3300", "CYU3201", "CYU3302", "PHU3300", 
    "PHU3301", "PHU3202", "ZYU3500", "ZYU3301", "ADU3300", "ADU3201", 
    "ADU3302", "PEU3300", "PEU3301", "PEU3202", "ADE3200", "CYE3200", 
    "LTE34GE", "FDE3021", "CSE3214", "LLU3261", "OSU3208", "DSU3298", 
    "FNU3200", "ADU3218", "BYU4300", "BYU4301", "BYU4302", "BYU4303", 
    "CYU4300", "CYU4301", "CYU4303", "CYU4302", "PHU4300", "PHU4301", 
    "PHU4302", "PHU4303", "ZYU4300", "ZYU4301", "ZYU4302", "ZYU4303", 
    "ADU4300", "ADU4301", "ADU4302", "ADU4303", "PEU4300", "PEU4301", 
    "PEU4302", "PEU4303", "BYU3500", "BYU3501", "BYU5302", "BYU5303", 
    "BYU5304", "BYU5305", "BYU5306", "BYU5307", "BYU5308", "BYU5610", 
    "CYU5300", "CYU5301", "CYU5302", "CYU5303", "CYU5304", "CYU5305", 
    "CYU5306", "CYU5307", "CYU5308", "CYU5309", "CYU5310", "CYU5611", 
    "CYU5312", "CYU5313", "CYU5614", "CYU5615", "PHU5300", "PHU5301", 
    "PHU5302", "PHU5303", "PHU5304", "PHU5305", "PHU5306", "PHU5307", 
    "PHU5308", "PHU5309", "PHU5610", "PHU5311", "PHU5312", "PHU5313", 
    "PHU5314", "PHU5315", "ZYU5300", "ZYU5301", "ZYU5302", "ZYU5303", 
    "ZYU5304", "ZYU5305", "ZYU5306", "ZYU5307", "ZYU5608", "ZYU5309", 
    "ZYU5310", "ZYU5311", "ZYU5312", "ZYU5313", "ZYU5314", "ZYU5315", 
    "ADU5300", "ADU5301", "ADU5302", "ADU5303", "ADU5304", "ADU5305", 
    "ADU5307", "ADU5308", "ADU5309", "ADU5310", "ADU5312", "ADU5313", 
    "ADU5314", "ADU5615", "PEU5300", "PEU5301", "PEU5302", "PEU5303", 
    "PEU5304", "PEU5305", "PEU5306", "PEU5307", "ADU5318", "ADU5319", 
    "ADU5320", "ADU5321", "BYU5318", "PHU5318"
]

# Majority threshold: 50% of codes must be present
MAJORITY_THRESHOLD = 0.5

# MEDIUM CONFIDENCE BOOSTERS (+8-15% each)
MEDIUM_CONFIDENCE_BOOSTERS = {
    "full_address": [
        "PO Box 21, The Open University of Sri Lanka, Nawala, Nugegoda",
        "P.O. Box 21",
        "Nawala, Nugegoda"
    ],
    # Single non-CSU code in document → MEDIUM booster
    "course_codes_other": [
        "BYU3301", "BYU3500", "CYU3300", "CYU3201", "CYU3302", "PHU3300", 
        "PHU3301", "PHU3202", "ZYU3500", "ZYU3301", "ADU3300", "ADU3201", 
        "ADU3302", "PEU3300", "PEU3301", "PEU3202", "ADE3200", "CYE3200", 
        "LTE34GE", "FDE3021", "CSE3214", "LLU3261", "OSU3208", "DSU3298", 
        "FNU3200", "ADU3218", "BYU4300", "BYU4301", "BYU4302", "BYU4303", 
        "CYU4300", "CYU4301", "CYU4303", "CYU4302", "PHU4300", "PHU4301", 
        "PHU4302", "PHU4303", "ZYU4300", "ZYU4301", "ZYU4302", "ZYU4303", 
        "ADU4300", "ADU4301", "ADU4302", "ADU4303", "PEU4300", "PEU4301", 
        "PEU4302", "PEU4303", "BYU3500", "BYU3501", "BYU5302", "BYU5303", 
        "BYU5304", "BYU5305", "BYU5306", "BYU5307", "BYU5308", "BYU5610", 
        "CYU5300", "CYU5301", "CYU5302", "CYU5303", "CYU5304", "CYU5305", 
        "CYU5306", "CYU5307", "CYU5308", "CYU5309", "CYU5310", "CYU5611", 
        "CYU5312", "CYU5313", "CYU5614", "CYU5615", "PHU5300", "PHU5301", 
        "PHU5302", "PHU5303", "PHU5304", "PHU5305", "PHU5306", "PHU5307", 
        "PHU5308", "PHU5309", "PHU5610", "PHU5311", "PHU5312", "PHU5313", 
        "PHU5314", "PHU5315", "ZYU5300", "ZYU5301", "ZYU5302", "ZYU5303", 
        "ZYU5304", "ZYU5305", "ZYU5306", "ZYU5307", "ZYU5608", "ZYU5309", 
        "ZYU5310", "ZYU5311", "ZYU5312", "ZYU5313", "ZYU5314", "ZYU5315", 
        "ADU5300", "ADU5301", "ADU5302", "ADU5303", "ADU5304", "ADU5305", 
        "ADU5307", "ADU5308", "ADU5309", "ADU5310", "ADU5312", "ADU5313", 
        "ADU5314", "ADU5615", "PEU5300", "PEU5301", "PEU5302", "PEU5303", 
        "PEU5304", "PEU5305", "PEU5306", "PEU5307", "ADU5318", "ADU5319", 
        "ADU5320", "ADU5321", "BYU5318", "PHU5318"
    ],
    "academic_terms": [
        "2024/2025", "2023/2024", "Semester 1", "semester 2", "CAT 1", 
        "CAT 2", "OBT", "NBT", "ELIGIBILITY", "MARKS", "PRACTICAL", 
        "Workshop", "VIVA", "Lab reservation", "Semester", "Academic year"
    ],
    "document_types": [
        "Syllabus", "Transcript", "Certificate", "Assignment", 
        "Research Paper", "MTT", "Tentative", "Course Outline",
        "Examination", "Assessment"
    ],
    "staff_affiliation": [
        "Lecturer", "Senior Lecturer", "Professor", "Dr.", 
        "OUSL affiliation", "Department of"
    ]
}

# LOW CONFIDENCE BOOSTERS (+1-7% each)
LOW_CONFIDENCE_BOOSTERS = {
    "general_faculties": [
        "Faculty of Engineering",
        "Faculty of Humanities and Social Sciences",
        "Faculty of Management and Commerce",
        "Faculty of Health Sciences and Allied Health Sciences",
        "Faculty of Education",
        "Faculty of Computing",
        "Faculty of Science"
    ],
    "general_programmes": [
        "Civil Engineering", "Mechanical Engineering", "Mechatronics Engineering",
        "Computer Engineering", "Electrical & Electronic Engineering",
        "Agricultural Engineering", "Textile & Apparel Engineering",
        "Fashion Design and Apparel Production", "Textile Manufacture",
        "Apparel Production and Management", "Marketing Management",
        "Special Needs Education", "Pre-school Education",
        "Laboratory Technology", "Food Science",
        "Physics", "Chemistry", "Zoology", "Botany", "Mathematics"
    ]
}

# Confidence calculation settings
BASE_CONFIDENCE = 0.70  # 70% base when mandatory phrase found
HIGH_BOOSTER_INCREMENT = 0.175  # +17.5% per high confidence booster (average of 15-20%)
MEDIUM_BOOSTER_INCREMENT = 0.115  # +11.5% per medium confidence booster (average of 8-15%)
LOW_BOOSTER_INCREMENT = 0.04  # +4% per low confidence booster (average of 1-7%)

# For backward compatibility
CONFIDENCE_BOOSTERS = HIGH_CONFIDENCE_BOOSTERS
BOOSTER_INCREMENT = HIGH_BOOSTER_INCREMENT

# Semantic similarity thresholds
SIMILARITY_THRESHOLD = 0.70  # minimum similarity to retrieve from ChromaDB
TOP_K_RESULTS = 5  # number of similar documents to retrieve

# ===================================================================
# Groq LLM Settings
# ===================================================================
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = "mixtral-8x7b-32768"  # or "llama-3.1-70b-versatile"
GROQ_TEMPERATURE = 0.1  # low temperature for consistent classification
GROQ_MAX_TOKENS = 500

# ===================================================================
# Supported File Types
# ===================================================================
SUPPORTED_EXTENSIONS = [".pdf", ".docx", ".txt"]
