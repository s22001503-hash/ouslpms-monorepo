"""
Policy Proposal Backend Implementation
Handles policy proposal creation, approval workflow, and special user policies
"""

from datetime import datetime
from typing import Dict, List, Optional
from firebase_admin import firestore

# Initialize Firestore client
db = firestore.client()

# Collection references
POLICY_PROPOSALS_COLLECTION = 'policy_proposals'
USER_SPECIAL_POLICIES_COLLECTION = 'user_special_policies'
GLOBAL_POLICIES_COLLECTION = 'global_policies'

# Default global policies
DEFAULT_GLOBAL_POLICIES = {
    'maxAttemptsPerDay': 5,
    'maxCopiesPerDoc': 5
}


def get_current_global_policies() -> Dict:
    """Get current global policies"""
    try:
        doc = db.collection(GLOBAL_POLICIES_COLLECTION).document('current').get()
        if doc.exists:
            return doc.to_dict()
        else:
            # Initialize with defaults if not exists
            db.collection(GLOBAL_POLICIES_COLLECTION).document('current').set(DEFAULT_GLOBAL_POLICIES)
            return DEFAULT_GLOBAL_POLICIES
    except Exception as e:
        print(f"Error getting global policies: {e}")
        return DEFAULT_GLOBAL_POLICIES


def create_policy_proposal(proposal_data: Dict) -> Dict:
    """
    Create a new policy proposal
    
    Args:
        proposal_data: {
            'type': 'global' or 'special_user',
            'adminEPF': str,
            'adminName': str,
            'justification': str,
            'changes': Dict (for global),
            'targetEPF': str (for special_user),
            'targetName': str (for special_user),
            'targetDept': str (for special_user),
            'proposedPolicy': Dict (for special_user)
        }
    
    Returns:
        Created proposal document with ID
    """
    try:
        proposal = {
            'type': proposal_data['type'],
            'adminEPF': proposal_data['adminEPF'],
            'adminName': proposal_data['adminName'],
            'justification': proposal_data['justification'],
            'status': 'pending',
            'submittedAt': datetime.utcnow().isoformat() + 'Z',
            'vcDecision': None
        }
        
        if proposal_data['type'] == 'global':
            proposal['changes'] = proposal_data['changes']
        else:  # special_user
            proposal['targetEPF'] = proposal_data['targetEPF']
            proposal['targetName'] = proposal_data['targetName']
            proposal['targetDept'] = proposal_data['targetDept']
            proposal['proposedPolicy'] = proposal_data['proposedPolicy']
        
        # Add to Firestore
        doc_ref = db.collection(POLICY_PROPOSALS_COLLECTION).add(proposal)
        proposal['id'] = doc_ref[1].id
        
        return proposal
    except Exception as e:
        raise Exception(f"Failed to create policy proposal: {str(e)}")


def create_removal_proposal(target_epf: str, admin_epf: str, justification: str) -> Dict:
    """
    Create a proposal to remove special policy from a user
    
    Args:
        target_epf: EPF of user to remove special policy from
        admin_epf: EPF of admin requesting removal
        justification: Reason for removal
    
    Returns:
        Created proposal document with ID
    """
    try:
        # Get user info from users collection or special policies
        user_doc = db.collection('users').document(target_epf).get()
        user_name = user_doc.to_dict().get('name', 'Unknown') if user_doc.exists else 'Unknown'
        user_dept = user_doc.to_dict().get('department', 'Unknown') if user_doc.exists else 'Unknown'
        
        # Get admin info
        admin_doc = db.collection('users').document(admin_epf).get()
        admin_name = admin_doc.to_dict().get('name', 'Admin') if admin_doc.exists else 'Admin'
        
        proposal = {
            'type': 'removal',
            'adminEPF': admin_epf,
            'adminName': admin_name,
            'targetEPF': target_epf,
            'targetName': user_name,
            'targetDept': user_dept,
            'justification': justification,
            'status': 'pending',
            'submittedAt': datetime.utcnow().isoformat() + 'Z',
            'vcDecision': None
        }
        
        # Add to Firestore
        doc_ref = db.collection(POLICY_PROPOSALS_COLLECTION).add(proposal)
        proposal['id'] = doc_ref[1].id
        
        return proposal
    except Exception as e:
        raise Exception(f"Failed to create removal proposal: {str(e)}")


def get_policy_proposals(proposal_type: Optional[str] = None, status: Optional[str] = None) -> List[Dict]:
    """
    Get policy proposals with optional filters
    
    Args:
        proposal_type: 'global', 'special_user', or None for all
        status: 'pending', 'approved', 'rejected', or None for all
    
    Returns:
        List of proposal documents
    """
    try:
        query = db.collection(POLICY_PROPOSALS_COLLECTION)
        
        if proposal_type:
            query = query.where('type', '==', proposal_type)
        if status:
            query = query.where('status', '==', status)
        
        docs = query.order_by('submittedAt', direction=firestore.Query.DESCENDING).stream()
        
        proposals = []
        for doc in docs:
            proposal = doc.to_dict()
            proposal['id'] = doc.id
            proposals.append(proposal)
        
        return proposals
    except Exception as e:
        raise Exception(f"Failed to get policy proposals: {str(e)}")


def approve_policy_proposal(proposal_id: str, vc_epf: str, notes: str = '') -> Dict:
    """
    Approve a policy proposal and apply changes
    
    Args:
        proposal_id: Proposal document ID
        vc_epf: VC's EPF number
        notes: Optional approval notes
    
    Returns:
        Updated proposal document
    """
    try:
        doc_ref = db.collection(POLICY_PROPOSALS_COLLECTION).document(proposal_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise Exception("Proposal not found")
        
        proposal = doc.to_dict()
        
        if proposal['status'] != 'pending':
            raise Exception("Proposal is not pending")
        
        # Update proposal status
        vc_decision = {
            'decision': 'approved',
            'notes': notes,
            'decidedBy': f'VC {vc_epf}',
            'decidedAt': datetime.utcnow().isoformat() + 'Z'
        }
        
        doc_ref.update({
            'status': 'approved',
            'vcDecision': vc_decision
        })
        
        # Apply the changes
        if proposal['type'] == 'global':
            # Update global policies
            current_policies = get_current_global_policies()
            for field, change in proposal['changes'].items():
                current_policies[field] = change['proposed']
            
            db.collection(GLOBAL_POLICIES_COLLECTION).document('current').set(current_policies)
        
        elif proposal['type'] == 'removal':
            # Remove special user policy
            db.collection(USER_SPECIAL_POLICIES_COLLECTION).document(proposal['targetEPF']).delete()
        
        else:  # special_user
            # Create or update special user policy
            user_policy = {
                'epf': proposal['targetEPF'],
                'name': proposal['targetName'],
                'department': proposal['targetDept'],
                'specialPolicy': proposal['proposedPolicy'],
                'approvedAt': vc_decision['decidedAt'],
                'approvedBy': vc_decision['decidedBy'],
                'justification': proposal['justification'],
                'proposalId': proposal_id
            }
            
            db.collection(USER_SPECIAL_POLICIES_COLLECTION).document(proposal['targetEPF']).set(user_policy)
        
        proposal['status'] = 'approved'
        proposal['vcDecision'] = vc_decision
        proposal['id'] = proposal_id
        
        return proposal
    except Exception as e:
        raise Exception(f"Failed to approve policy proposal: {str(e)}")


def reject_policy_proposal(proposal_id: str, vc_epf: str, reason: str) -> Dict:
    """
    Reject a policy proposal
    
    Args:
        proposal_id: Proposal document ID
        vc_epf: VC's EPF number
        reason: Rejection reason
    
    Returns:
        Updated proposal document
    """
    try:
        doc_ref = db.collection(POLICY_PROPOSALS_COLLECTION).document(proposal_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise Exception("Proposal not found")
        
        proposal = doc.to_dict()
        
        if proposal['status'] != 'pending':
            raise Exception("Proposal is not pending")
        
        vc_decision = {
            'decision': 'rejected',
            'notes': reason,
            'decidedBy': f'VC {vc_epf}',
            'decidedAt': datetime.utcnow().isoformat() + 'Z'
        }
        
        doc_ref.update({
            'status': 'rejected',
            'vcDecision': vc_decision
        })
        
        proposal['status'] = 'rejected'
        proposal['vcDecision'] = vc_decision
        proposal['id'] = proposal_id
        
        return proposal
    except Exception as e:
        raise Exception(f"Failed to reject policy proposal: {str(e)}")


def get_special_policy_users() -> List[Dict]:
    """
    Get all users with active special policies
    
    Returns:
        List of users with special policies including usage statistics
    """
    try:
        docs = db.collection(USER_SPECIAL_POLICIES_COLLECTION).stream()
        
        users = []
        for doc in docs:
            user_policy = doc.to_dict()
            
            # TODO: Add actual usage statistics from print_jobs collection
            # For now, return mock statistics
            user_policy['usage'] = {
                'totalPrints': 0,
                'averageDaily': 0,
                'lastPrint': None
            }
            
            users.append(user_policy)
        
        return users
    except Exception as e:
        raise Exception(f"Failed to get special policy users: {str(e)}")


def remove_special_policy(epf: str) -> bool:
    """
    Remove special policy from a user
    
    Args:
        epf: User's EPF number
    
    Returns:
        True if successful
    """
    try:
        db.collection(USER_SPECIAL_POLICIES_COLLECTION).document(epf).delete()
        return True
    except Exception as e:
        raise Exception(f"Failed to remove special policy: {str(e)}")


def get_user_policy(epf: str) -> Dict:
    """
    Get effective policy for a user (special if exists, otherwise global)
    
    Args:
        epf: User's EPF number
    
    Returns:
        Policy limits for the user
    """
    try:
        # Check if user has special policy
        doc = db.collection(USER_SPECIAL_POLICIES_COLLECTION).document(epf).get()
        
        if doc.exists:
            user_policy = doc.to_dict()
            return {
                'type': 'special',
                'maxAttemptsPerDay': user_policy['specialPolicy']['maxAttemptsPerDay'],
                'maxCopiesPerDoc': user_policy['specialPolicy']['maxCopiesPerDoc'],
                'source': 'special_policy'
            }
        else:
            # Return global policies
            global_policies = get_current_global_policies()
            return {
                'type': 'global',
                'maxAttemptsPerDay': global_policies['maxAttemptsPerDay'],
                'maxCopiesPerDoc': global_policies['maxCopiesPerDoc'],
                'source': 'global_policy'
            }
    except Exception as e:
        raise Exception(f"Failed to get user policy: {str(e)}")


# Firestore security rules to add:
"""
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    
    // Policy Proposals - Admin can create, VC can approve/reject
    match /policy_proposals/{proposalId} {
      allow read: if request.auth != null && (
        get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role in ['admin', 'vc']
      );
      allow create: if request.auth != null && 
        get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'admin';
      allow update: if request.auth != null && 
        get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'vc';
    }
    
    // User Special Policies - Admin/VC read, system writes after VC approval
    match /user_special_policies/{epf} {
      allow read: if request.auth != null && (
        get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role in ['admin', 'vc'] ||
        request.auth.uid == epf
      );
      allow write: if request.auth != null && 
        get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'vc';
    }
    
    // Global Policies - Admin/VC read, VC write
    match /global_policies/{docId} {
      allow read: if request.auth != null;
      allow write: if request.auth != null && 
        get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'vc';
    }
  }
}
"""
