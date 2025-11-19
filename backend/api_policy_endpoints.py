"""
Policy Proposal API Endpoints
FastAPI routes for policy proposal management
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, List
from .policy_proposals import (
    get_current_global_policies,
    create_policy_proposal,
    get_policy_proposals,
    approve_policy_proposal,
    reject_policy_proposal,
    get_special_policy_users,
    remove_special_policy,
    get_user_policy
)
from .auth import verify_admin, verify_vc, get_current_user

router = APIRouter()


# Request/Response Models
class GlobalPolicyChange(BaseModel):
    current: int
    proposed: int


class GlobalPolicyProposalRequest(BaseModel):
    type: str = 'global'
    adminEPF: str
    adminName: str
    justification: str
    changes: Dict[str, GlobalPolicyChange]


class SpecialUserPolicyRequest(BaseModel):
    type: str = 'special_user'
    adminEPF: str
    adminName: str
    targetEPF: str
    targetName: str
    targetDept: str
    justification: str
    proposedPolicy: Dict[str, int]


class RemovalProposalRequest(BaseModel):
    targetEpf: str
    requestedBy: str
    justification: str


class ApproveProposalRequest(BaseModel):
    proposalId: str
    vcId: str
    notes: str = ''


class RejectProposalRequest(BaseModel):
    proposalId: str
    vcId: str
    reason: str


class RemoveSpecialPolicyRequest(BaseModel):
    epf: str


# Admin Endpoints
@router.get("/admin/current-policies")
async def get_current_policies(current_user: dict = Depends(verify_admin)):
    """Get current global policies"""
    try:
        policies = get_current_global_policies()
        return policies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/admin/user-by-epf/{epf}")
async def get_user_by_epf(epf: str, current_user: dict = Depends(verify_admin)):
    """Get user details by EPF number"""
    try:
        # TODO: Implement actual user lookup from users collection
        # For now, return mock data
        from firebase_admin import firestore
        db = firestore.client()
        
        doc = db.collection('users').document(epf).get()
        if not doc.exists:
            raise HTTPException(status_code=404, detail="User not found")
        
        user = doc.to_dict()
        return {
            'epf': epf,
            'name': user.get('name', 'Unknown'),
            'email': user.get('email', ''),
            'department': user.get('department', 'Unknown'),
            'role': user.get('role', 'user')
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/admin/propose-policy")
async def propose_policy(
    request: dict,
    current_user: dict = Depends(verify_admin)
):
    """Create a new policy proposal"""
    try:
        proposal = create_policy_proposal(request)
        return {
            'success': True,
            'message': 'Policy proposal submitted for VC approval',
            'proposal': proposal
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/admin/policy-proposals")
async def get_proposals(
    type: Optional[str] = None,
    status: Optional[str] = None,
    current_user: dict = Depends(verify_admin)
):
    """Get policy proposals with optional filters"""
    try:
        proposals = get_policy_proposals(type, status)
        return proposals
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/admin/special-policy-users")
async def get_special_users(current_user: dict = Depends(verify_admin)):
    """Get all users with active special policies"""
    try:
        users = get_special_policy_users()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/admin/remove-special-policy")
async def remove_user_special_policy(
    request: RemoveSpecialPolicyRequest,
    current_user: dict = Depends(verify_admin)
):
    """Remove special policy from a user (direct removal - deprecated, use request-removal-proposal instead)"""
    try:
        success = remove_special_policy(request.epf)
        return {
            'success': success,
            'message': f'Special policy removed from user {request.epf}'
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/admin/request-removal-proposal")
async def request_removal_proposal(
    request: RemovalProposalRequest,
    current_user: dict = Depends(verify_admin)
):
    """Create a proposal to remove special policy from a user"""
    try:
        from .policy_proposals import create_removal_proposal
        proposal = create_removal_proposal(
            target_epf=request.targetEpf,
            admin_epf=request.requestedBy,
            justification=request.justification
        )
        return {
            'success': True,
            'message': f'Removal request submitted for user {request.targetEpf}',
            'proposal': proposal
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# VC Endpoints
@router.get("/vc/policy-proposals")
async def get_proposals_vc(
    type: Optional[str] = None,
    status: Optional[str] = None,
    current_user: dict = Depends(verify_vc)
):
    """Get policy proposals (VC view)"""
    try:
        proposals = get_policy_proposals(type, status)
        return proposals
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/vc/policy-proposals/approve")
async def approve_proposal(
    request: ApproveProposalRequest,
    current_user: dict = Depends(verify_vc)
):
    """Approve a policy proposal"""
    try:
        proposal = approve_policy_proposal(
            request.proposalId,
            request.vcId,
            request.notes
        )
        return {
            'success': True,
            'message': 'Policy proposal approved and applied',
            'proposal': proposal
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/vc/policy-proposals/reject")
async def reject_proposal(
    request: RejectProposalRequest,
    current_user: dict = Depends(verify_vc)
):
    """Reject a policy proposal"""
    try:
        proposal = reject_policy_proposal(
            request.proposalId,
            request.vcId,
            request.reason
        )
        return {
            'success': True,
            'message': 'Policy proposal rejected',
            'proposal': proposal
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Public/User Endpoints
@router.get("/user/my-policy/{epf}")
async def get_my_policy(epf: str, current_user: dict = Depends(get_current_user)):
    """Get effective policy for current user"""
    try:
        # Verify user is requesting their own policy or is admin/vc
        if current_user.get('epf') != epf and current_user.get('role') not in ['admin', 'vc']:
            raise HTTPException(status_code=403, detail="Access denied")
        
        policy = get_user_policy(epf)
        return policy
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
