from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import firestore
from .auth import verify_admin

router = APIRouter()

# ==================== Pydantic Models ====================

class ProposeSettingsRequest(BaseModel):
    adminId: str
    proposedSettings: Dict[str, Any]

class SystemSettings(BaseModel):
    maxCopiesPerDocument: int
    maxPrintAttemptsPerDay: int

class SettingsProposal(BaseModel):
    id: str
    adminId: str
    adminEmail: str
    adminName: Optional[str] = None
    proposedSettings: Dict[str, Any]
    status: str  # pending, approved, rejected
    submittedAt: str
    reviewedAt: Optional[str] = None
    reviewedBy: Optional[str] = None
    reviewedByName: Optional[str] = None
    deanNotes: Optional[str] = None

# ==================== Helper Functions ====================

def get_firestore_db():
    """Get Firestore database instance."""
    if not firebase_admin._apps:
        raise HTTPException(status_code=500, detail='Firebase Admin not configured')
    return firestore.client()

def format_timestamp(dt: datetime) -> str:
    """Format datetime to ISO string."""
    return dt.isoformat() + 'Z'

# ==================== Endpoints ====================

@router.get("/overview")
async def get_overview_stats(current_user: dict = Depends(verify_admin)):
    """
    Get admin dashboard overview statistics.
    Returns: todayPrintJobs, pendingProposals, blockedAttempts, activeUsers, recentActivity
    """
    try:
        db = get_firestore_db()
        
        # Get today's date range
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # ===== Count today's print jobs =====
        # TODO: Replace with actual print_jobs collection query
        today_print_jobs = 0  # Placeholder
        
        # ===== Count pending proposals =====
        pending_proposals_ref = db.collection('settings_requests').where('status', '==', 'pending')
        pending_proposals_count = len(list(pending_proposals_ref.stream()))
        
        # ===== Count blocked attempts today =====
        # TODO: Query blocked_attempts collection for today
        blocked_attempts = 0  # Placeholder
        
        # ===== Count active users =====
        users_ref = db.collection('users')
        active_users_count = len(list(users_ref.stream()))
        
        # ===== Get recent activity =====
        # Query admin_actions collection for recent activities
        recent_activity = []
        try:
            admin_actions_ref = db.collection('admin_actions').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(10)
            for doc in admin_actions_ref.stream():
                data = doc.to_dict()
                activity_type = data.get('action', 'unknown')
                
                # Map action types to activity descriptions
                type_map = {
                    'create_user': 'user_added',
                    'delete_user': 'user_deleted',
                    'change_password': 'password_changed',
                    'propose_settings': 'settings_proposed'
                }
                
                status_map = {
                    'create_user': 'success',
                    'delete_user': 'warning',
                    'change_password': 'success',
                    'propose_settings': 'pending'
                }
                
                # Calculate time ago
                timestamp = data.get('timestamp')
                if isinstance(timestamp, datetime):
                    time_diff = datetime.now() - timestamp
                    if time_diff.days > 0:
                        time_ago = f"{time_diff.days} day{'s' if time_diff.days > 1 else ''} ago"
                    elif time_diff.seconds >= 3600:
                        hours = time_diff.seconds // 3600
                        time_ago = f"{hours} hour{'s' if hours > 1 else ''} ago"
                    elif time_diff.seconds >= 60:
                        minutes = time_diff.seconds // 60
                        time_ago = f"{minutes} min ago"
                    else:
                        time_ago = "Just now"
                else:
                    time_ago = "Recently"
                
                recent_activity.append({
                    'id': doc.id,
                    'type': type_map.get(activity_type, 'system'),
                    'description': data.get('details', 'System activity'),
                    'timestamp': time_ago,
                    'status': status_map.get(activity_type, 'success')
                })
        except Exception as e:
            print(f"Error fetching recent activity: {e}")
            # Return empty activity if collection doesn't exist yet
            pass
        
        return {
            'todayPrintJobs': today_print_jobs,
            'pendingProposals': pending_proposals_count,
            'blockedAttempts': blocked_attempts,
            'activeUsers': active_users_count,
            'recentActivity': recent_activity
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to fetch overview stats: {str(e)}')


@router.get("/system-settings")
async def get_system_settings(current_user: dict = Depends(verify_admin)):
    """
    Get current approved system settings.
    Returns: maxCopiesPerDocument (per day), maxPrintAttemptsPerDay
    """
    try:
        db = get_firestore_db()
        
        # Get current settings from Firestore
        settings_ref = db.collection('system_settings').document('current')
        settings_doc = settings_ref.get()
        
        if settings_doc.exists:
            data = settings_doc.to_dict()
            return {
                'maxCopiesPerDocument': data.get('maxCopiesPerDocument', 10),
                'maxPrintAttemptsPerDay': data.get('maxPrintAttemptsPerDay', 50),
                'lastModified': data.get('lastModified'),
                'modifiedBy': data.get('modifiedBy'),
                'modifiedByName': data.get('modifiedByName')
            }
        else:
            # Return default settings if document doesn't exist
            # Also create the document with defaults
            default_settings = {
                'maxCopiesPerDocument': 10,
                'maxPrintAttemptsPerDay': 50,
                'lastModified': format_timestamp(datetime.now()),
                'modifiedBy': 'system',
                'modifiedByName': 'System Default'
            }
            settings_ref.set(default_settings)
            return default_settings
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to fetch system settings: {str(e)}')


@router.get("/settings-requests")
async def get_settings_requests(
    adminId: Optional[str] = None,
    current_user: dict = Depends(verify_admin)
):
    """
    Get settings proposal history.
    Query params: adminId (optional) - filter by admin ID
    Returns: list of proposals with status
    """
    try:
        db = get_firestore_db()
        
        # Build query
        query = db.collection('settings_requests')
        
        # Filter by adminId if provided
        if adminId:
            query = query.where('adminId', '==', adminId)
        
        # Order by submission date (newest first)
        query = query.order_by('submittedAt', direction=firestore.Query.DESCENDING)
        
        # Execute query
        proposals = []
        for doc in query.stream():
            data = doc.to_dict()
            proposals.append({
                'id': doc.id,
                'adminId': data.get('adminId'),
                'adminEmail': data.get('adminEmail'),
                'adminName': data.get('adminName'),
                'proposedSettings': data.get('proposedSettings', {}),
                'status': data.get('status', 'pending'),
                'submittedAt': data.get('submittedAt'),
                'reviewedAt': data.get('reviewedAt'),
                'reviewedBy': data.get('reviewedBy'),
                'reviewedByName': data.get('reviewedByName'),
                'deanNotes': data.get('deanNotes')
            })
        
        return proposals
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to fetch settings requests: {str(e)}')


@router.post("/propose-settings")
async def propose_settings(
    request: ProposeSettingsRequest,
    current_user: dict = Depends(verify_admin)
):
    """
    Submit new settings proposal for Dean approval.
    Body: { adminId, proposedSettings }
    Returns: { success, message, requestId }
    """
    try:
        db = get_firestore_db()
        
        # Validate proposed settings
        proposed = request.proposedSettings
        
        # Check required fields
        required_fields = ['maxCopiesPerDocument', 'maxPrintAttemptsPerDay']
        for field in required_fields:
            if field not in proposed:
                raise HTTPException(status_code=400, detail=f'Missing required field: {field}')
        
        # Validate ranges
        if not (1 <= proposed.get('maxCopiesPerDocument', 0) <= 100):
            raise HTTPException(status_code=400, detail='maxCopiesPerDocument must be between 1 and 100')
        
        if not (1 <= proposed.get('maxPrintAttemptsPerDay', 0) <= 200):
            raise HTTPException(status_code=400, detail='maxPrintAttemptsPerDay must be between 1 and 200')
        
        # Check if admin already has a pending proposal
        existing_pending = db.collection('settings_requests')\
            .where('adminId', '==', request.adminId)\
            .where('status', '==', 'pending')\
            .limit(1)\
            .stream()
        
        if len(list(existing_pending)) > 0:
            raise HTTPException(
                status_code=400, 
                detail='You already have a pending proposal. Please wait for Dean approval before submitting a new one.'
            )
        
        # Get admin details from current_user
        admin_email = current_user.get('email', '')
        admin_name = current_user.get('name', '')
        
        # Create proposal document
        proposal_data = {
            'adminId': request.adminId,
            'adminEmail': admin_email,
            'adminName': admin_name,
            'proposedSettings': proposed,
            'status': 'pending',
            'submittedAt': format_timestamp(datetime.now()),
            'reviewedAt': None,
            'reviewedBy': None,
            'reviewedByName': None,
            'deanNotes': None
        }
        
        # Add to Firestore
        doc_ref = db.collection('settings_requests').add(proposal_data)
        request_id = doc_ref[1].id
        
        # Log to admin_actions
        try:
            db.collection('admin_actions').add({
                'action': 'propose_settings',
                'adminId': request.adminId,
                'timestamp': datetime.now(),
                'details': f'Settings proposal submitted by {admin_name or admin_email}',
                'proposalId': request_id
            })
        except Exception as log_error:
            print(f"Failed to log admin action: {log_error}")
        
        return {
            'success': True,
            'message': 'Settings proposal submitted successfully',
            'requestId': request_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to propose settings: {str(e)}')


@router.post("/dean/review-proposal/{proposal_id}")
async def review_proposal(
    proposal_id: str,
    approve: bool,
    dean_notes: Optional[str] = None,
    current_user: dict = Depends(verify_admin)  # TODO: Change to verify_dean when implemented
):
    """
    Dean approves or rejects a settings proposal.
    Path param: proposal_id
    Body: { approve: bool, dean_notes: str (optional) }
    """
    try:
        db = get_firestore_db()
        
        # TODO: Verify current_user is Dean role
        dean_id = current_user.get('epf')
        dean_name = current_user.get('name', '')
        
        # Get proposal
        proposal_ref = db.collection('settings_requests').document(proposal_id)
        proposal_doc = proposal_ref.get()
        
        if not proposal_doc.exists:
            raise HTTPException(status_code=404, detail='Proposal not found')
        
        proposal_data = proposal_doc.to_dict()
        
        # Check if already reviewed
        if proposal_data.get('status') != 'pending':
            raise HTTPException(status_code=400, detail='Proposal has already been reviewed')
        
        # Update proposal status
        new_status = 'approved' if approve else 'rejected'
        proposal_ref.update({
            'status': new_status,
            'reviewedAt': format_timestamp(datetime.now()),
            'reviewedBy': dean_id,
            'reviewedByName': dean_name,
            'deanNotes': dean_notes
        })
        
        # If approved, update system_settings
        if approve:
            settings_ref = db.collection('system_settings').document('current')
            proposed_settings = proposal_data.get('proposedSettings', {})
            
            settings_ref.update({
                'maxCopiesPerDocument': proposed_settings.get('maxCopiesPerDocument'),
                'maxPrintAttemptsPerDay': proposed_settings.get('maxPrintAttemptsPerDay'),
                'maxPagesPerJob': proposed_settings.get('maxPagesPerJob'),
                'dailyQuota': proposed_settings.get('dailyQuota'),
                'allowColorPrinting': proposed_settings.get('allowColorPrinting'),
                'lastModified': format_timestamp(datetime.now()),
                'modifiedBy': dean_id,
                'modifiedByName': dean_name
            })
        
        # Log action
        try:
            db.collection('admin_actions').add({
                'action': 'review_proposal',
                'deanId': dean_id,
                'timestamp': datetime.now(),
                'details': f'Proposal {new_status} by {dean_name}',
                'proposalId': proposal_id,
                'approved': approve
            })
        except Exception as log_error:
            print(f"Failed to log admin action: {log_error}")
        
        return {
            'success': True,
            'message': f'Proposal {new_status} successfully',
            'status': new_status
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to review proposal: {str(e)}')
