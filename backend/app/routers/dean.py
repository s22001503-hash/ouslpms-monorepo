from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import firestore
from .auth import verify_dean

router = APIRouter()

# ==================== Pydantic Models ====================

class ApproveSettingsRequest(BaseModel):
    proposalId: str
    deanId: str
    deanName: str
    notes: Optional[str] = None

class RejectSettingsRequest(BaseModel):
    proposalId: str
    deanId: str
    deanName: str
    reason: Optional[str] = None

class NotificationItem(BaseModel):
    id: str
    type: str
    title: str
    message: str
    timestamp: str
    read: bool
    priority: str

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
async def get_dean_overview(current_user: dict = Depends(verify_dean)):
    """
    Get overview statistics for Dean Dashboard.
    Returns: todayPrintJobs, pendingProposals, blockedAttempts, activeUsers
    """
    try:
        db = get_firestore_db()
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Today's print jobs
        print_logs_ref = db.collection('print_logs')
        today_jobs_query = print_logs_ref.where('timestamp', '>=', today)
        today_print_jobs = len(list(today_jobs_query.stream()))
        
        # Pending proposals
        settings_requests_ref = db.collection('settings_requests')
        pending_proposals_query = settings_requests_ref.where('status', '==', 'pending')
        pending_proposals_count = len(list(pending_proposals_query.stream()))
        
        # Blocked attempts (today)
        blocked_query = print_logs_ref.where('status', '==', 'blocked').where('timestamp', '>=', today)
        blocked_attempts = len(list(blocked_query.stream()))
        
        # Active users
        users_ref = db.collection('users')
        active_users_query = users_ref.where('status', '==', 'active')
        active_users_count = len(list(active_users_query.stream()))
        
        return {
            'todayPrintJobs': today_print_jobs,
            'pendingProposals': pending_proposals_count,
            'blockedAttempts': blocked_attempts,
            'activeUsers': active_users_count
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to fetch dean overview stats: {str(e)}')


@router.get("/settings-requests")
async def get_pending_proposals(
    status: Optional[str] = 'pending',
    current_user: dict = Depends(verify_dean)
):
    """
    Get settings proposals filtered by status.
    Default: pending proposals
    """
    try:
        db = get_firestore_db()
        settings_requests_ref = db.collection('settings_requests')
        
        # Query by status
        query = settings_requests_ref.where('status', '==', status).order_by('submittedAt', direction=firestore.Query.DESCENDING)
        docs = query.stream()
        
        proposals = []
        for doc in docs:
            data = doc.to_dict()
            proposals.append({
                'id': doc.id,
                'adminId': data.get('adminId'),
                'adminEmail': data.get('adminEmail'),
                'adminName': data.get('adminName', 'Unknown Admin'),
                'proposedSettings': data.get('proposedSettings', {}),
                'currentSettings': data.get('currentSettings', {}),
                'status': data.get('status'),
                'submittedAt': data.get('submittedAt'),
                'reviewedAt': data.get('reviewedAt'),
                'reviewedBy': data.get('reviewedBy'),
                'reviewedByName': data.get('reviewedByName'),
                'deanNotes': data.get('deanNotes')
            })
        
        return {'proposals': proposals, 'count': len(proposals)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to fetch settings proposals: {str(e)}')


@router.post("/settings/approve")
async def approve_settings(
    request: ApproveSettingsRequest,
    current_user: dict = Depends(verify_dean)
):
    """
    Approve a settings proposal and update system settings.
    """
    try:
        db = get_firestore_db()
        
        # Get the proposal
        proposal_ref = db.collection('settings_requests').document(request.proposalId)
        proposal_doc = proposal_ref.get()
        
        if not proposal_doc.exists:
            raise HTTPException(status_code=404, detail='Proposal not found')
        
        proposal_data = proposal_doc.to_dict()
        
        if proposal_data.get('status') != 'pending':
            raise HTTPException(status_code=400, detail=f'Proposal already {proposal_data.get("status")}')
        
        # Update proposal status
        proposal_ref.update({
            'status': 'approved',
            'reviewedAt': format_timestamp(datetime.now()),
            'reviewedBy': request.deanId,
            'reviewedByName': request.deanName,
            'deanNotes': request.notes or ''
        })
        
        # Update system settings with approved values
        proposed_settings = proposal_data.get('proposedSettings', {})
        settings_ref = db.collection('system_settings').document('current')
        
        # Check if settings document exists
        settings_doc = settings_ref.get()
        if settings_doc.exists:
            settings_ref.update({
                **proposed_settings,
                'lastUpdated': format_timestamp(datetime.now()),
                'updatedBy': request.deanName
            })
        else:
            settings_ref.set({
                **proposed_settings,
                'lastUpdated': format_timestamp(datetime.now()),
                'updatedBy': request.deanName
            })
        
        # Log the approval action
        db.collection('admin_actions').add({
            'type': 'approve_settings',
            'deanId': request.deanId,
            'deanName': request.deanName,
            'proposalId': request.proposalId,
            'adminId': proposal_data.get('adminId'),
            'settings': proposed_settings,
            'timestamp': datetime.now(),
            'details': f'Dean approved settings proposal from {proposal_data.get("adminName", "Admin")}'
        })
        
        return {
            'success': True,
            'message': 'Settings proposal approved successfully',
            'proposalId': request.proposalId
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to approve settings: {str(e)}')


@router.post("/settings/reject")
async def reject_settings(
    request: RejectSettingsRequest,
    current_user: dict = Depends(verify_dean)
):
    """
    Reject a settings proposal.
    """
    try:
        db = get_firestore_db()
        
        # Get the proposal
        proposal_ref = db.collection('settings_requests').document(request.proposalId)
        proposal_doc = proposal_ref.get()
        
        if not proposal_doc.exists:
            raise HTTPException(status_code=404, detail='Proposal not found')
        
        proposal_data = proposal_doc.to_dict()
        
        if proposal_data.get('status') != 'pending':
            raise HTTPException(status_code=400, detail=f'Proposal already {proposal_data.get("status")}')
        
        # Update proposal status
        proposal_ref.update({
            'status': 'rejected',
            'reviewedAt': format_timestamp(datetime.now()),
            'reviewedBy': request.deanId,
            'reviewedByName': request.deanName,
            'deanNotes': request.reason or 'No reason provided'
        })
        
        # Log the rejection action
        db.collection('admin_actions').add({
            'type': 'reject_settings',
            'deanId': request.deanId,
            'deanName': request.deanName,
            'proposalId': request.proposalId,
            'adminId': proposal_data.get('adminId'),
            'reason': request.reason,
            'timestamp': datetime.now(),
            'details': f'Dean rejected settings proposal from {proposal_data.get("adminName", "Admin")}'
        })
        
        return {
            'success': True,
            'message': 'Settings proposal rejected',
            'proposalId': request.proposalId
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to reject settings: {str(e)}')


@router.get("/notifications")
async def get_dean_notifications(current_user: dict = Depends(verify_dean)):
    """
    Get notifications for Dean (new proposals, security alerts, etc.)
    """
    try:
        db = get_firestore_db()
        notifications = []
        
        # Get pending proposals as notifications
        settings_requests_ref = db.collection('settings_requests')
        pending_query = settings_requests_ref.where('status', '==', 'pending').order_by('submittedAt', direction=firestore.Query.DESCENDING).limit(10)
        
        for doc in pending_query.stream():
            data = doc.to_dict()
            submitted_at = data.get('submittedAt', '')
            notifications.append({
                'id': doc.id,
                'type': 'proposal',
                'title': 'New Settings Proposal',
                'message': f'{data.get("adminName", "An admin")} proposed new system settings',
                'timestamp': submitted_at,
                'read': False,
                'priority': 'high'
            })
        
        # Get recent blocked attempts (security alerts)
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        print_logs_ref = db.collection('print_logs')
        blocked_query = print_logs_ref.where('status', '==', 'blocked').where('timestamp', '>=', today).limit(5)
        
        for doc in blocked_query.stream():
            data = doc.to_dict()
            timestamp = data.get('timestamp')
            if isinstance(timestamp, datetime):
                timestamp_str = format_timestamp(timestamp)
            else:
                timestamp_str = str(timestamp)
            
            notifications.append({
                'id': doc.id,
                'type': 'security',
                'title': 'Blocked Print Attempt',
                'message': f'User {data.get("userId", "Unknown")} attempted to print blocked content',
                'timestamp': timestamp_str,
                'read': False,
                'priority': 'medium'
            })
        
        # Sort by timestamp (most recent first)
        notifications.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return {
            'notifications': notifications,
            'count': len(notifications),
            'unreadCount': len([n for n in notifications if not n['read']])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to fetch notifications: {str(e)}')


@router.get("/reports")
async def get_dean_reports(current_user: dict = Depends(verify_dean)):
    """
    Generate oversight reports for Dean.
    """
    try:
        db = get_firestore_db()
        
        # Calculate date ranges
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # Print jobs by user (top 10)
        print_logs_ref = db.collection('print_logs')
        all_jobs = print_logs_ref.where('timestamp', '>=', month_ago).stream()
        
        user_job_counts = {}
        for doc in all_jobs:
            data = doc.to_dict()
            user_id = data.get('userId', 'Unknown')
            user_job_counts[user_id] = user_job_counts.get(user_id, 0) + 1
        
        top_users = sorted(user_job_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Proposal statistics
        settings_requests_ref = db.collection('settings_requests')
        all_proposals = list(settings_requests_ref.stream())
        
        proposal_stats = {
            'total': len(all_proposals),
            'pending': 0,
            'approved': 0,
            'rejected': 0
        }
        
        for doc in all_proposals:
            status = doc.to_dict().get('status', 'pending')
            if status in proposal_stats:
                proposal_stats[status] += 1
        
        # Blocked attempts by day (last 7 days)
        blocked_by_day = {}
        for i in range(7):
            day = today - timedelta(days=i)
            day_str = day.strftime('%Y-%m-%d')
            blocked_by_day[day_str] = 0
        
        blocked_query = print_logs_ref.where('status', '==', 'blocked').where('timestamp', '>=', week_ago)
        for doc in blocked_query.stream():
            data = doc.to_dict()
            timestamp = data.get('timestamp')
            if isinstance(timestamp, datetime):
                day_str = timestamp.strftime('%Y-%m-%d')
                if day_str in blocked_by_day:
                    blocked_by_day[day_str] += 1
        
        return {
            'reportGenerated': format_timestamp(datetime.now()),
            'topUsers': [{'userId': uid, 'printJobs': count} for uid, count in top_users],
            'proposalStats': proposal_stats,
            'blockedAttemptsByDay': blocked_by_day,
            'totalPrintJobs': sum(user_job_counts.values()),
            'totalBlockedAttempts': sum(blocked_by_day.values())
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to generate reports: {str(e)}')
