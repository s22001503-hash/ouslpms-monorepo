"""
AI Document Classifier using RAG approach
- ChromaDB for semantic similarity search
- Groq LLM for final classification decision
"""
from typing import Dict, List
import os
from groq import Groq

from .chroma_manager import ChromaDBManager
from .config import (
    MANDATORY_PHRASE,
    MANDATORY_PHRASE_ALT,
    HIGH_CONFIDENCE_BOOSTERS,
    MEDIUM_CONFIDENCE_BOOSTERS,
    LOW_CONFIDENCE_BOOSTERS,
    BASE_CONFIDENCE,
    HIGH_BOOSTER_INCREMENT,
    MEDIUM_BOOSTER_INCREMENT,
    LOW_BOOSTER_INCREMENT,
    ALL_COURSE_CODES_FOR_MAJORITY,
    MAJORITY_THRESHOLD,
    GROQ_API_KEY,
    GROQ_MODEL,
    GROQ_TEMPERATURE,
    GROQ_MAX_TOKENS
)

class DocumentClassifier:
    """Classify documents as OFFICIAL or PERSONAL using RAG"""
    
    def __init__(self):
        """Initialize classifier with ChromaDB and Groq client"""
        self.chroma = ChromaDBManager()
        
        # Initialize Groq client
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.groq_client = Groq(api_key=GROQ_API_KEY)
        print(f"Groq LLM initialized with model: {GROQ_MODEL}")
    
    def check_mandatory_requirement(self, text: str) -> bool:
        """
        Check if document contains mandatory OUSL phrase
        Returns True if found, False otherwise
        """
        text_lower = text.lower()
        mandatory_lower = MANDATORY_PHRASE.lower()
        mandatory_alt_lower = MANDATORY_PHRASE_ALT.lower()
        
        return mandatory_lower in text_lower or mandatory_alt_lower in text_lower
    
    def calculate_confidence_boosters(self, text: str) -> Dict:
        """
        Calculate confidence score based on three-tier booster system
        Returns dict with booster details and final confidence
        """
        # Initialize found boosters for all three tiers
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
        
        # Check HIGH confidence boosters (excluding course codes, handled separately)
        for category, phrases in HIGH_CONFIDENCE_BOOSTERS.items():
            if category == "course_codes_csu":
                continue  # Handle course codes separately with special logic
            for phrase in phrases:
                # Case-insensitive search
                if phrase.lower() in text_lower:
                    high_boosters[category].append(phrase)
        
        # Check MEDIUM confidence boosters (excluding course codes, handled separately)
        for category, phrases in MEDIUM_CONFIDENCE_BOOSTERS.items():
            if category == "course_codes_other":
                continue  # Handle course codes separately with special logic
            for phrase in phrases:
                # For academic_terms, do case-insensitive comparison
                if category == 'academic_terms':
                    if phrase.lower() in text_lower:
                        medium_boosters[category].append(phrase)
                else:
                    # For others, check if phrase exists (case-insensitive)
                    if phrase.lower() in text_lower or phrase in text:
                        medium_boosters[category].append(phrase)
        
        # Check LOW confidence boosters
        for category, phrases in LOW_CONFIDENCE_BOOSTERS.items():
            for phrase in phrases:
                if phrase.lower() in text_lower:
                    low_boosters[category].append(phrase)
        
        # === COURSE CODE LOGIC ===
        # Find all course codes in document
        found_codes = []
        for code in ALL_COURSE_CODES_FOR_MAJORITY:
            if code in text:  # Case-sensitive for course codes
                found_codes.append(code)
        
        # Determine course code classification
        csu_codes = HIGH_CONFIDENCE_BOOSTERS["course_codes_csu"]
        non_csu_codes = MEDIUM_CONFIDENCE_BOOSTERS["course_codes_other"]
        
        # Check for MAJORITY (50%+ of all 220 codes in single document)
        majority_threshold_count = int(len(ALL_COURSE_CODES_FOR_MAJORITY) * MAJORITY_THRESHOLD)
        if len(found_codes) >= majority_threshold_count:
            # This is a comprehensive course catalog → HIGH booster
            high_boosters["course_codes_csu"] = [f"MAJORITY_CODES ({len(found_codes)}/{len(ALL_COURSE_CODES_FOR_MAJORITY)})"]
        else:
            # Check for single CSU code → HIGH booster
            csu_found = [code for code in found_codes if code in csu_codes]
            if len(csu_found) > 0:
                high_boosters["course_codes_csu"] = csu_found[:1]  # Only count as 1 booster
            
            # Check for single non-CSU code → MEDIUM booster
            non_csu_found = [code for code in found_codes if code in non_csu_codes]
            if len(non_csu_found) > 0:
                medium_boosters["course_codes_other"] = non_csu_found[:1]  # Only count as 1 booster
        
        # Count boosters in each tier (categories with at least one match)
        high_booster_count = sum(1 for boosters in high_boosters.values() if len(boosters) > 0)
        medium_booster_count = sum(1 for boosters in medium_boosters.values() if len(boosters) > 0)
        low_booster_count = sum(1 for boosters in low_boosters.values() if len(boosters) > 0)
        
        # Calculate confidence with three-tier system
        confidence = BASE_CONFIDENCE
        confidence += high_booster_count * HIGH_BOOSTER_INCREMENT
        confidence += medium_booster_count * MEDIUM_BOOSTER_INCREMENT
        confidence += low_booster_count * LOW_BOOSTER_INCREMENT
        confidence = min(confidence, 1.0)  # cap at 100%
        
        return {
            'high_boosters': high_boosters,
            'medium_boosters': medium_boosters,
            'low_boosters': low_boosters,
            'high_booster_count': high_booster_count,
            'medium_booster_count': medium_booster_count,
            'low_booster_count': low_booster_count,
            'total_booster_count': high_booster_count + medium_booster_count + low_booster_count,
            'confidence': confidence,
            'course_codes_found': found_codes  # For debugging
        }
    
    def build_classification_prompt(
        self, 
        document_text: str, 
        similar_docs: List[Dict],
        mandatory_found: bool,
        booster_info: Dict
    ) -> str:
        """
        Build prompt for Groq LLM
        Includes context from similar documents
        """
        # Format similar documents context
        context = "Similar documents from training data:\n\n"
        for i, doc in enumerate(similar_docs[:3], 1):  # use top 3
            label = doc['metadata'].get('label', 'unknown')
            similarity = doc['similarity']
            text_preview = doc['text'][:300] + "..." if len(doc['text']) > 300 else doc['text']
            context += f"{i}. [{label.upper()}] (similarity: {similarity:.2f})\n{text_preview}\n\n"
        
        # Build prompt with three-tier booster system
        prompt = f"""You are a document classifier for The Open University of Sri Lanka (OUSL).

**MANDATORY CLASSIFICATION RULE (THUMB RULE):**
A document is OFFICIAL **IF AND ONLY IF** it contains at least ONE of these:
1. "The Open University of Sri Lanka" (any capitalization)
2. "THE OPEN UNIVERSITY OF SRI LANKA" (all caps)

This is ABSOLUTELY REQUIRED. If neither phrase is found, the document is PERSONAL regardless of any other content.

**OPTIONAL CONFIDENCE BOOSTERS:**

HIGH CONFIDENCE BOOSTERS (+15-20% each):
- Faculty names (e.g., FACULTY OF NATURAL SCIENCE, Faculty of Engineering Technology)
- Degree programmes (e.g., BACHELOR OF SCIENCE DEGREE PROGRAMME)
- Department names (e.g., Department of Computer Science)
- Course codes (CSU series: CSU3200, CSU3301, etc.)
- Official markers (University seal, Official letterhead)

MEDIUM CONFIDENCE BOOSTERS (+8-15% each):
- Full OUSL address (PO Box 21, Nawala, Nugegoda)
- Course codes (other series: BYU, CYU, PHU, ZYU, ADU, PEU, etc.)
- Academic terms (2024/2025, Semester 1, CAT 1, MARKS, PRACTICAL, etc.)
- Document types (Syllabus, Transcript, Certificate, Assignment)
- Staff affiliation (Lecturer, Professor with OUSL)

LOW CONFIDENCE BOOSTERS (+1-7% each):
- General faculty mentions
- General programme mentions

**ANALYSIS FOR THIS DOCUMENT:**
- Mandatory phrase found: {mandatory_found}
- HIGH boosters found: {booster_info['high_booster_count']}
- MEDIUM boosters found: {booster_info['medium_booster_count']}
- LOW boosters found: {booster_info['low_booster_count']}
- Suggested confidence: {booster_info['confidence']:.0%}

{context}

**DOCUMENT TO CLASSIFY:**
{document_text[:1500]}{"..." if len(document_text) > 1500 else ""}

**INSTRUCTIONS:**
Based on the MANDATORY RULE and similar documents above, classify this document as either OFFICIAL or PERSONAL.
Provide your response in this exact format:

CLASSIFICATION: [OFFICIAL or PERSONAL]
CONFIDENCE: [0.0 to 1.0]
REASONING: [Brief explanation of your decision]
"""
        return prompt
    
    def classify_with_llm(self, prompt: str) -> Dict:
        """
        Call Groq LLM to classify document
        Returns classification result
        """
        try:
            response = self.groq_client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a precise document classifier for university documents. Always follow the mandatory classification rules."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=GROQ_TEMPERATURE,
                max_tokens=GROQ_MAX_TOKENS
            )
            
            # Parse response
            response_text = response.choices[0].message.content
            
            # Extract classification
            classification = "PERSONAL"  # default
            confidence = 0.5
            reasoning = ""
            
            for line in response_text.split('\n'):
                if line.startswith('CLASSIFICATION:'):
                    classification = line.split(':', 1)[1].strip().upper()
                elif line.startswith('CONFIDENCE:'):
                    try:
                        confidence = float(line.split(':', 1)[1].strip())
                    except:
                        confidence = 0.5
                elif line.startswith('REASONING:'):
                    reasoning = line.split(':', 1)[1].strip()
            
            return {
                'classification': classification,
                'confidence': confidence,
                'reasoning': reasoning,
                'raw_response': response_text
            }
        
        except Exception as e:
            print(f"Error calling Groq LLM: {e}")
            return {
                'classification': 'PERSONAL',
                'confidence': 0.0,
                'reasoning': f'Error: {str(e)}',
                'raw_response': ''
            }
    
    def classify_document(self, document_text: str) -> Dict:
        """
        Main classification method
        
        Process:
        1. Check mandatory requirement
        2. Search similar documents in ChromaDB
        3. Calculate confidence boosters
        4. Use Groq LLM for final decision
        
        Returns classification result with details
        """
        print("\n" + "="*60)
        print("CLASSIFYING DOCUMENT")
        print("="*60)
        
        # Step 1: Check mandatory requirement
        mandatory_found = self.check_mandatory_requirement(document_text)
        print(f"Mandatory OUSL phrase found: {mandatory_found}")
        
        # Step 2: Find similar documents
        print("Searching for similar documents in ChromaDB...")
        similar_docs = self.chroma.search_similar(document_text[:2000])  # use first 2000 chars
        print(f"Found {len(similar_docs)} similar documents")
        
        # Step 3: Calculate confidence boosters
        booster_info = self.calculate_confidence_boosters(document_text)
        print(f"Confidence boosters found:")
        print(f"  HIGH: {booster_info['high_booster_count']}")
        print(f"  MEDIUM: {booster_info['medium_booster_count']}")
        print(f"  LOW: {booster_info['low_booster_count']}")
        
        # Step 4: Use LLM for final classification
        prompt = self.build_classification_prompt(
            document_text,
            similar_docs,
            mandatory_found,
            booster_info
        )
        
        print("Calling Groq LLM for classification...")
        llm_result = self.classify_with_llm(prompt)
        
        # Combine results
        result = {
            'classification': llm_result['classification'],
            'confidence': llm_result['confidence'],
            'reasoning': llm_result['reasoning'],
            'mandatory_found': mandatory_found,
            'high_boosters': booster_info['high_boosters'],
            'medium_boosters': booster_info['medium_boosters'],
            'low_boosters': booster_info['low_boosters'],
            'high_booster_count': booster_info['high_booster_count'],
            'medium_booster_count': booster_info['medium_booster_count'],
            'low_booster_count': booster_info['low_booster_count'],
            'total_booster_count': booster_info['total_booster_count'],
            'suggested_confidence': booster_info['confidence'],
            'similar_documents_count': len(similar_docs),
            'llm_raw_response': llm_result['raw_response']
        }
        
        print(f"\nRESULT: {result['classification']} ({result['confidence']:.0%})")
        print(f"REASONING: {result['reasoning']}")
        print(f"BOOSTERS: HIGH={result['high_booster_count']}, MEDIUM={result['medium_booster_count']}, LOW={result['low_booster_count']}")
        print("="*60 + "\n")
        
        return result
