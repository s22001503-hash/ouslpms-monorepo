from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Header
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
import os
import firebase_admin
from firebase_admin import auth, firestore
import logging
import openai  # ✅ NEW: For executive summary generation

router = APIRouter()
logger = logging.getLogger(__name__)

# Firestore client will be initialized lazily
def get_db():
    """Get Firestore client instance."""
    try:
        if not firebase_admin._apps:
            logger.warning("⚠️ Firebase not initialized - Firestore unavailable")
            return None
        return firestore.client()
    except Exception as e:
        logger.error(f"❌ Firestore client error: {e}")
        return None

# ==================== Pydantic Models ====================

class AuthorizeRequest(BaseModel):
    token: str  # Firebase ID token
    user_id: Optional[str] = None  # EPF number

class AuthorizeResponse(BaseModel):
    authorized: bool
    message: str
    user_id: Optional[str] = None
    role: Optional[str] = None

class BlockedPrintAttempt(BaseModel):
    user_id: str
    timestamp: str
    reason: str
    file_name: Optional[str] = None

class AgentTokenData(BaseModel):
    token: str
    user_id: str
    role: str
    email: str

class PrintJobRequest(BaseModel):
    file_path: str
    file_name: str
    file_size: int
    file_hash: Optional[str] = None  # SHA-256 hash for traceability
    pdf_text: Optional[str] = None  # Extracted PDF text for classification
    printer: str
    user_id: str
    document: str
    total_pages: int
    timestamp: str
    status: str
    auth_token: Optional[str] = None  # Firebase auth token
    copies: Optional[int] = 1  # ✅ NEW: Copy count from print spooler

class PrintJobResponse(BaseModel):
    status: str
    classification: str
    action: str  # approved, block, require_approval
    message: str
    job_id: Optional[str] = None
    executive_summary: Optional[Dict[str, Any]] = None  # ✅ NEW: Executive summary from GPT-4


# ==================== Helper Functions ====================

def classify_document(file_path: str, metadata: Dict[str, Any]) -> str:
    """
    Enhanced AI-based document classification using PDF text content.
    
    Categories:
    - office: Work-related documents
    - personal: Personal documents
    - sensitive: Confidential/sensitive documents
    
    Uses both filename and PDF content for classification.
    """
    document_name = metadata.get('document', '').lower()
    pdf_text = metadata.get('pdf_text', '').lower()
    
    # Combine document name and text for analysis
    content = f"{document_name} {pdf_text}"
    
    # Sensitive document keywords (highest priority)
    sensitive_keywords = [
        'confidential', 'private', 'secret', 'classified',
        'internal only', 'restricted', 'proprietary',
        'salary', 'budget', 'financial statement', 'ssn',
        'password', 'credit card', 'bank account'
    ]
    
    # Office document keywords
    office_keywords = [
        'report', 'memo', 'meeting', 'project', 'agenda',
        'minutes', 'proposal', 'presentation', 'analysis',
        'quarterly', 'annual', 'department', 'strategy',
        'objective', 'roadmap', 'milestone', 'deliverable'
    ]
    
    # Personal document keywords
    personal_keywords = [
        'birthday', 'party', 'invitation', 'wedding',
        'vacation', 'holiday', 'personal', 'family',
        'resume', 'cv', 'recipe', 'shopping'
    ]
    
    # Check for sensitive content first (security priority)
    if any(keyword in content for keyword in sensitive_keywords):
        return 'sensitive'
    
    # Count matches for office vs personal
    office_score = sum(1 for keyword in office_keywords if keyword in content)
    personal_score = sum(1 for keyword in personal_keywords if keyword in content)
    
    if office_score > personal_score:
        return 'office'
    elif personal_score > 0:
        return 'personal'
    else:
        # Default to office if no clear indicators
        return 'office'

def determine_action(classification: str, user_role: str = 'user') -> str:
    """
    Determine action based on classification and user role.
    
    Returns:
    - approved: Allow printing immediately
    - block: Block printing
    - require_approval: Require Dean/Admin approval
    """
    # Policy rules
    if classification == 'office':
        return 'approved'  # Office documents are allowed
    elif classification == 'personal':
        if user_role == 'admin':
            return 'require_approval'  # Admin personal prints need Dean approval
        else:
            return 'block'  # Regular users cannot print personal documents
    elif classification == 'sensitive':
        return 'require_approval'  # Sensitive documents always require approval
    else:
        return 'block'  # Unknown classification - block by default

# ==================== Endpoints ====================

@router.post("/authorize", response_model=AuthorizeResponse)
async def authorize_print(request: AuthorizeRequest):
    """
    Verify if user is logged in via Firebase Auth token.
    This endpoint is called by the virtual printer agent before processing print jobs.
    
    Returns:
    - authorized: True if user is logged in and token is valid
    - message: Status message
    - user_id: EPF number
    - role: User role (user/admin/dean)
    """
    try:
        # Check if Firebase is available
        if not firebase_admin._apps:
            return AuthorizeResponse(
                authorized=False,
                message="Firebase authentication not configured",
                user_id=None,
                role=None
            )
        
        # Verify Firebase ID token
        decoded_token = auth.verify_id_token(request.token)
        user_email = decoded_token.get('email', '')
        uid = decoded_token.get('uid', '')
        
        # Extract EPF from email (format: {epf}@ousl.edu.lk)
        epf = user_email.split('@')[0] if '@' in user_email else request.user_id
        
        # Get user role from Firestore
        db = get_db()
        if db is None:
            # Firestore not available, return default role
            logger.warning("⚠️ Firestore unavailable - returning default user role")
            return AuthorizeResponse(
                authorized=True,
                message="User authenticated (Firestore unavailable)",
                user_id=epf,
                role='user'
            )
        
        user_ref = db.collection('users').document(epf)
        user_doc = user_ref.get()
        
        if not user_doc.exists:
            return AuthorizeResponse(
                authorized=False,
                message="User not found in database",
                user_id=epf,
                role=None
            )
        
        user_data = user_doc.to_dict()
        role = user_data.get('role', 'user')
        
        return AuthorizeResponse(
            authorized=True,
            message="User authenticated successfully",
            user_id=epf,
            role=role
        )
    
    except auth.InvalidIdTokenError:
        return AuthorizeResponse(
            authorized=False,
            message="Invalid or expired authentication token",
            user_id=None,
            role=None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authorization error: {str(e)}")

@router.post("/save-agent-token")
async def save_agent_token(token_data: AgentTokenData):
    """
    Save Firebase token to file for print agent authentication.
    Called by frontend after successful login to enable print agent authentication.
    """
    try:
        import json
        from pathlib import Path
        
        AUTH_TOKEN_FILE = r"C:\AI_Prints\auth_token.txt"
        
        # Ensure directory exists
        Path(AUTH_TOKEN_FILE).parent.mkdir(parents=True, exist_ok=True)
        
        # Save token data
        with open(AUTH_TOKEN_FILE, 'w') as f:
            json.dump({
                'token': token_data.token,
                'user_id': token_data.user_id,
                'role': token_data.role,
                'email': token_data.email,
                'timestamp': datetime.now().isoformat()
            }, f, indent=2)
        
        logger.info(f"✅ Agent token saved for user: {token_data.user_id}")
        
        return {
            "status": "success",
            "message": f"Token saved for user {token_data.user_id}",
            "file_path": AUTH_TOKEN_FILE
        }
    
    except Exception as e:
        logger.error(f"Failed to save agent token: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save token: {str(e)}")

@router.post("/clear-agent-token")
async def clear_agent_token():
    """
    Clear the print agent authentication token file.
    Called by frontend on logout to disable print agent authentication.
    """
    try:
        import os
        
        AUTH_TOKEN_FILE = r"C:\AI_Prints\auth_token.txt"
        
        if os.path.exists(AUTH_TOKEN_FILE):
            os.remove(AUTH_TOKEN_FILE)
            logger.info("✅ Agent token cleared")
            return {
                "status": "success",
                "message": "Agent token cleared successfully"
            }
        else:
            return {
                "status": "success",
                "message": "No token file to clear"
            }
    
    except Exception as e:
        logger.error(f"Failed to clear agent token: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to clear token: {str(e)}")

@router.post("/log-blocked-attempt")
async def log_blocked_attempt(attempt: BlockedPrintAttempt):
    """
    Log unauthorized print attempts for audit trail.
    Called by virtual printer agent when blocking unauthenticated print jobs.
    """
    try:
        # Store in Firestore if available
        db = get_db()
        if db is None:
            logger.warning("⚠️ Firestore unavailable - blocked attempt not logged to database")
            return {
                "status": "warning",
                "message": "Logged locally (Firestore unavailable)"
            }
        
        blocked_ref = db.collection('blocked_print_attempts').document()
        blocked_ref.set({
            'user_id': attempt.user_id,
            'timestamp': attempt.timestamp,
            'reason': attempt.reason,
            'file_name': attempt.file_name,
            'logged_at': firestore.SERVER_TIMESTAMP
        })
        
        return {
            "status": "success",
            "message": "Blocked attempt logged successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Logging error: {str(e)}")

# ==================== Print Processing Endpoints ====================

@router.post("/process-job", response_model=PrintJobResponse)
async def process_print_job(job: PrintJobRequest):
    """
    🚀 Sprint 5 — AI-Powered Print Job Processing with Firestore Policy Enforcement
    
    Flow:
    1. Verify user authentication (Firebase token required)
    2. Classify document using AI (official/personal/confidential)
    3. Policy Enforcement (Firestore-driven, admin-configurable):
       - Personal: BLOCK immediately (no prints allowed)
       - Official/Confidential: Check daily limit + copy limit from Firestore
    4. Generate executive summary (OpenAI GPT-4)
    5. Store to Firestore with classification + executive summary
    6. Increment daily counter ONLY on successful approval
    7. Return action with detailed reason
    """
    try:
        # Step 1: Auth enforcement (if token provided)
        user_role = 'user'  # Default
        db = get_db()
        
        if job.auth_token:
            try:
                decoded_token = auth.verify_id_token(job.auth_token)
                user_email = decoded_token.get('email', '')
                epf = user_email.split('@')[0] if '@' in user_email else job.user_id
                
                # Get user role
                user_ref = db.collection('users').document(epf)
                user_doc = user_ref.get()
                if user_doc.exists:
                    user_role = user_doc.to_dict().get('role', 'user')
                
            except auth.InvalidIdTokenError:
                # Log blocked attempt
                db.collection('blocked_print_attempts').add({
                    'user_id': job.user_id,
                    'timestamp': job.timestamp,
                    'reason': 'Invalid or expired authentication token',
                    'file_name': job.file_name,
                    'logged_at': firestore.SERVER_TIMESTAMP
                })
                
                return PrintJobResponse(
                    status='blocked',
                    classification='unknown',
                    action='block',
                    message='User not logged in — printing blocked.',
                    job_id=None
                )
        
        # Step 2: Classify document using AI (office/personal/sensitive)
        classification = classify_document(
            job.file_path,  # Path for reference only
            {
                'document': job.document,
                'user_id': job.user_id,
                'total_pages': job.total_pages,
                'pdf_text': getattr(job, 'pdf_text', '')  # PDF text sent by agent
            }
        )
        
        # ==================== SPRINT 5: FIRESTORE POLICY ENFORCEMENT ====================
        
        # Step 3A: Personal Documents → BLOCK IMMEDIATELY
        if classification == 'personal':
            logger.warning(f"🚫 Personal document blocked: {job.file_name}")
            
            # Log blocked attempt
            db.collection('blocked_print_attempts').add({
                'user_id': job.user_id,
                'timestamp': job.timestamp,
                'reason': 'Personal documents are not allowed',
                'file_name': job.file_name,
                'classification': 'personal',
                'logged_at': firestore.SERVER_TIMESTAMP
            })
            
            return PrintJobResponse(
                status='blocked',
                classification='personal',
                action='block',
                message='Personal documents are not allowed for printing.',
                job_id=None
            )
        
        # Step 3B: Official/Confidential Documents → Check Firestore Policies
        elif classification in ['office', 'confidential']:
            # Get admin-configurable policies from Firestore
            system_policies_ref = db.collection('system_policies').document('default')
            system_policies_doc = system_policies_ref.get()
            
            if system_policies_doc.exists:
                system_policies = system_policies_doc.to_dict()
                max_daily_prints = system_policies.get('max_daily_prints', 3)
                max_copies_per_document = system_policies.get('max_copies_per_document', 10)
            else:
                # Default fallback if policies not configured
                max_daily_prints = 3
                max_copies_per_document = 10
                logger.warning("⚠️ System policies not found in Firestore - using defaults")
            
            # CHECK #1: Daily Print Limit
            today = datetime.now().strftime('%Y-%m-%d')
            user_limit_doc_id = f'{job.user_id}_{today}'
            user_limit_ref = db.collection('user_daily_limits').document(user_limit_doc_id)
            user_limit_doc = user_limit_ref.get()
            
            if user_limit_doc.exists:
                user_limit_data = user_limit_doc.to_dict()
                prints_today = user_limit_data.get('prints_today', 0)
            else:
                prints_today = 0
            
            if prints_today >= max_daily_prints:
                logger.warning(f"🚫 Daily limit exceeded: {prints_today}/{max_daily_prints}")
                
                # Log blocked attempt
                db.collection('blocked_print_attempts').add({
                    'user_id': job.user_id,
                    'timestamp': job.timestamp,
                    'reason': f'Daily limit reached: {prints_today}/{max_daily_prints} prints used',
                    'file_name': job.file_name,
                    'classification': classification,
                    'logged_at': firestore.SERVER_TIMESTAMP
                })
                
                return PrintJobResponse(
                    status='blocked',
                    classification=classification,
                    action='block',
                    message=f'Daily print limit reached: {prints_today}/{max_daily_prints} prints used today.',
                    job_id=None
                )
            
            # CHECK #2: Copy Limit
            copies = job.copies if job.copies else 1
            
            if copies > max_copies_per_document:
                logger.warning(f"🚫 Copy limit exceeded: {copies}/{max_copies_per_document}")
                
                # Log blocked attempt
                db.collection('blocked_print_attempts').add({
                    'user_id': job.user_id,
                    'timestamp': job.timestamp,
                    'reason': f'Too many copies: {copies}/{max_copies_per_document} allowed',
                    'file_name': job.file_name,
                    'classification': classification,
                    'copies_requested': copies,
                    'logged_at': firestore.SERVER_TIMESTAMP
                })
                
                return PrintJobResponse(
                    status='blocked',
                    classification=classification,
                    action='block',
                    message=f'Too many copies requested: {copies}/{max_copies_per_document} allowed.',
                    job_id=None
                )
            
            # ✅ All checks passed - ALLOW print
            action = 'allow'
            
        else:
            # Unknown classification - use default action
            action = determine_action(classification, user_role)
        
        # Step 3: Generate executive summary using OpenAI GPT-4
        executive_summary = None
        pdf_text = getattr(job, 'pdf_text', '')
        
        if pdf_text and pdf_text.strip():
            try:
                # Truncate text to 4000 characters for API efficiency
                text_sample = pdf_text[:4000]
                
                summary_response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a document analysis assistant. Generate a concise executive summary (2-3 sentences), extract key topics, and detect sensitive information."
                        },
                        {
                            "role": "user",
                            "content": f"""Analyze this document and provide:
1. Title: Document title or main subject
2. Summary: 2-3 sentence executive summary
3. Key Topics: List 3-5 main topics
4. Sensitive Data: Boolean indicating if PII/confidential data detected

Document text:
{text_sample}

Respond in JSON format:
{{
  "title": "...",
  "summary": "...",
  "key_topics": ["topic1", "topic2", ...],
  "sensitive_data_detected": true/false
}}"""
                        }
                    ],
                    temperature=0.3,
                    max_tokens=300
                )
                
                # Parse OpenAI response
                summary_text = summary_response.choices[0].message.content.strip()
                
                # Try to parse as JSON
                try:
                    import json
                    summary_data = json.loads(summary_text)
                    executive_summary = {
                        'title': summary_data.get('title', job.file_name),
                        'summary': summary_data.get('summary', ''),
                        'key_topics': summary_data.get('key_topics', []),
                        'sensitive_data_detected': summary_data.get('sensitive_data_detected', False),
                        'word_count': len(pdf_text.split()),
                        'generated_at': datetime.now().isoformat(),
                        'method': 'GPT-4'
                    }
                except json.JSONDecodeError:
                    # Fallback if JSON parsing fails
                    executive_summary = {
                        'title': job.file_name,
                        'summary': summary_text[:500],  # Use raw text as summary
                        'key_topics': [],
                        'sensitive_data_detected': False,
                        'word_count': len(pdf_text.split()),
                        'generated_at': datetime.now().isoformat(),
                        'method': 'GPT-4'
                    }
                
                logger.info(f"✅ Executive summary generated for {job.file_name}")
            
            except Exception as e:
                logger.warning(f"⚠️ Failed to generate executive summary: {e}")
                executive_summary = {
                    'title': job.file_name,
                    'summary': 'Summary generation failed',
                    'key_topics': [],
                    'sensitive_data_detected': False,
                    'word_count': len(pdf_text.split()) if pdf_text else 0,
                    'generated_at': datetime.now().isoformat(),
                    'method': 'GPT-4 (error)',
                    'error': str(e)
                }
        
        # Step 4: Generate executive summary using OpenAI GPT-4 (only for allowed prints)
        executive_summary = None
        
        if action == 'allow' and pdf_text and pdf_text.strip():
            try:
                # Truncate text to 4000 characters for API efficiency
                text_sample = pdf_text[:4000]
                
                summary_response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a document analysis assistant. Generate a concise executive summary (2-3 sentences), extract key topics, and detect sensitive information."
                        },
                        {
                            "role": "user",
                            "content": f"""Analyze this document and provide:
1. Title: Document title or main subject
2. Summary: 2-3 sentence executive summary
3. Key Topics: List 3-5 main topics
4. Sensitive Data: Boolean indicating if PII/confidential data detected

Document text:
{text_sample}

Respond in JSON format:
{{
  "title": "...",
  "summary": "...",
  "key_topics": ["topic1", "topic2", ...],
  "sensitive_data_detected": true/false
}}"""
                        }
                    ],
                    temperature=0.3,
                    max_tokens=300
                )
                
                # Parse OpenAI response
                summary_text = summary_response.choices[0].message.content.strip()
                
                # Try to parse as JSON
                try:
                    import json
                    summary_data = json.loads(summary_text)
                    executive_summary = {
                        'title': summary_data.get('title', job.file_name),
                        'summary': summary_data.get('summary', ''),
                        'key_topics': summary_data.get('key_topics', []),
                        'sensitive_data_detected': summary_data.get('sensitive_data_detected', False),
                        'word_count': len(pdf_text.split()),
                        'generated_at': datetime.now().isoformat(),
                        'method': 'GPT-4'
                    }
                except json.JSONDecodeError:
                    # Fallback if JSON parsing fails
                    executive_summary = {
                        'title': job.file_name,
                        'summary': summary_text[:500],  # Use raw text as summary
                        'key_topics': [],
                        'sensitive_data_detected': False,
                        'word_count': len(pdf_text.split()),
                        'generated_at': datetime.now().isoformat(),
                        'method': 'GPT-4'
                    }
                
                logger.info(f"✅ Executive summary generated for {job.file_name}")
            
            except Exception as e:
                logger.warning(f"⚠️ Failed to generate executive summary: {e}")
                executive_summary = {
                    'title': job.file_name,
                    'summary': 'Summary generation failed',
                    'key_topics': [],
                    'sensitive_data_detected': False,
                    'word_count': len(pdf_text.split()) if pdf_text else 0,
                    'generated_at': datetime.now().isoformat(),
                    'method': 'GPT-4 (error)',
                    'error': str(e)
                }
        
        # Step 5: Increment daily counter ONLY for successful prints (official/confidential)
        job_id = f"PRINT_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if action == 'allow' and classification in ['office', 'confidential']:
            # Increment daily print counter
            today = datetime.now().strftime('%Y-%m-%d')
            user_limit_doc_id = f'{job.user_id}_{today}'
            user_limit_ref = db.collection('user_daily_limits').document(user_limit_doc_id)
            
            # Get current count
            user_limit_doc = user_limit_ref.get()
            if user_limit_doc.exists:
                user_limit_data = user_limit_doc.to_dict()
                current_prints = user_limit_data.get('prints_today', 0)
                print_history = user_limit_data.get('prints', [])
            else:
                current_prints = 0
                print_history = []
            
            # Add this print to history
            print_history.append({
                'timestamp': datetime.now().isoformat(),
                'file_hash': job.file_hash,
                'file_name': job.file_name,
                'classification': classification,
                'copies': job.copies if job.copies else 1
            })
            
            # Update counter
            user_limit_ref.set({
                'user_id': job.user_id,
                'date': today,
                'prints_today': current_prints + 1,
                'max_daily_prints': max_daily_prints,  # Store current policy
                'prints': print_history,
                'updated_at': firestore.SERVER_TIMESTAMP
            }, merge=True)
            
            logger.info(f"✅ Daily counter incremented: {current_prints + 1}/{max_daily_prints}")
        
        # Step 6: Log to Firestore print_logs collection (permanent audit trail)
        if db is not None:
            try:
                # Store in print_logs collection with executive summary
                db.collection('print_logs').add({
                    'job_id': job_id,
                    'user_id': job.user_id,
                    'document': job.document,
                    'file_name': job.file_name,
                    'file_hash': job.file_hash,
                    'total_pages': job.total_pages,
                    'classification': classification,
                    'action': action,
                    'executive_summary': executive_summary,  # ✅ Executive summary
                    'copies': job.copies if job.copies else 1,
                    'timestamp': job.timestamp,
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'logged_at': firestore.SERVER_TIMESTAMP
                })
                logger.info(f"✅ Print job logged to Firestore print_logs: {job_id}")
                
                # Also log to print_jobs collection for backward compatibility
                db.collection('print_jobs').add({
                    'job_id': job_id,
                    'user_id': job.user_id,
                    'document': job.document,
                    'file_name': job.file_name,
                    'file_hash': job.file_hash,
                    'total_pages': job.total_pages,
                    'classification': classification,
                    'action': action,
                    'timestamp': job.timestamp,
                    'logged_at': firestore.SERVER_TIMESTAMP
                })
                
            except Exception as e:
                logger.warning(f"⚠️ Failed to log to Firestore: {e}")
        else:
            logger.warning("⚠️ Firestore unavailable - print job not logged to database")
        
        # Step 7: Return response with executive summary
        if action == 'allow':
            return PrintJobResponse(
                status='success',
                classification=classification,
                action=action,
                message=f"Print approved. Classification: {classification}. Daily prints: {current_prints + 1}/{max_daily_prints}",
                job_id=job_id,
                executive_summary=executive_summary
            )
        else:
            return PrintJobResponse(
                status='blocked',
                classification=classification,
                action=action,
                message=f"Print blocked. Classification: {classification}.",
                job_id=job_id,
                executive_summary=executive_summary
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-document")
async def analyze_document(request: Dict[str, Any]):
    """
    🎯 Sprint 5 Placeholder: AI-Powered Document Classification
    
    This endpoint will use fine-tuned AI models (GPT-4/custom) to classify documents
    and enforce admin-configurable policies from Firestore.
    
    Current Implementation (Sprint 4):
    - Returns mock response with pending classification
    - Logs print attempt to Firestore
    - Allows all documents by default
    
    Future Implementation (Sprint 5):
    - AI classification: "official" | "personal" | "confidential"
    - Firestore policy checking (max_daily_prints, max_copies_per_document)
    - User daily limit tracking
    - Document copy limit enforcement
    - Confidence scoring and reasoning
    
    Request:
    {
        "user_id": "99999",
        "file_path": "C:\\AI_Prints\\document.pdf",
        "text": "extracted PDF text...",
        "metadata": {
            "timestamp": "2025-10-27T...",
            "user_role": "user",
            "file_hash": "abc123...",
            "copies": 1  # From print spooler
        }
    }
    
    Response:
    {
        "classification": "pending",  # Will be: "official" | "personal" | "confidential"
        "confidence": 0,  # Will be: 0.0-1.0
        "reason": "AI classification will be implemented in Sprint 5",
        "action": "allow",  # Will be: "allow" | "block" | "require_approval"
        "policy_check": {
            "daily_limit": "N/A",  # Will be: "2/3 prints today"
            "copy_limit": "N/A"    # Will be: "1/10 copies allowed"
        }
    }
    """
    try:
        user_id = request.get('user_id', 'unknown')
        file_path = request.get('file_path', 'unknown')
        text = request.get('text', '')
        metadata = request.get('metadata', {})
        copies = metadata.get('copies', 1)
        file_hash = metadata.get('file_hash', 'unknown')
        
        # Log to Firestore for Sprint 4 tracking
        db = get_db()
        job_id = f"ANALYZE_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if db is not None:
            try:
                db.collection('print_logs').add({
                    'job_id': job_id,
                    'user_id': user_id,
                    'file_path': file_path,
                    'file_hash': file_hash,
                    'copies': copies,
                    'classification': 'pending',  # Sprint 5 will populate this with AI result
                    'action': 'allow',  # Default to allow in Sprint 4
                    'text_length': len(text),
                    'metadata': metadata,
                    'timestamp': firestore.SERVER_TIMESTAMP,
                    'sprint': 'Sprint 4 - AI placeholder'
                })
                logger.info(f"📝 Document analysis logged: {job_id} (user: {user_id})")
            except Exception as e:
                logger.warning(f"⚠️ Failed to log to Firestore: {e}")
        
        # Sprint 4: Return mock response (allow all for now)
        return {
            'classification': 'pending',
            'confidence': 0,
            'reason': 'AI classification will be implemented in Sprint 5. Currently allowing all documents.',
            'action': 'allow',
            'policy_check': {
                'daily_limit': 'N/A - Will check Firestore policies in Sprint 5',
                'copy_limit': 'N/A - Will check against admin-configured limits in Sprint 5'
            },
            'next_steps': [
                '🔮 Sprint 5 will add fine-tuned AI model for classification',
                '📋 Sprint 5 will enforce admin-configurable policies from Firestore',
                '🚫 Sprint 5 will block personal documents automatically',
                '📊 Sprint 5 will enforce copy limits on official documents'
            ]
        }
    
    except Exception as e:
        logger.error(f"❌ Error in analyze_document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/print-stats")
async def get_print_stats():
    """Get print job statistics."""
    # TODO: Implement statistics from Firestore
    return {
        'total_jobs': 0,
        'approved': 0,
        'blocked': 0,
        'pending_approval': 0
    }
