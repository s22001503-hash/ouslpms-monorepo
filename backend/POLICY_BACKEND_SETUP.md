# Policy Proposals Backend Integration Guide

## Overview
This guide explains how to integrate the policy proposal system into your existing backend.

## Files Created

### 1. `policy_proposals.py`
Core business logic for policy management:
- `get_current_global_policies()` - Get current global policy values
- `create_policy_proposal()` - Create new proposal (global or special user)
- `get_policy_proposals()` - Retrieve proposals with filters
- `approve_policy_proposal()` - Approve and apply policy changes
- `reject_policy_proposal()` - Reject a proposal
- `get_special_policy_users()` - Get all users with special policies
- `remove_special_policy()` - Remove special policy from user
- `get_user_policy()` - Get effective policy for a user

### 2. `api_policy_endpoints.py`
FastAPI routes for policy management:

**Admin Endpoints:**
- `GET /admin/current-policies` - Get current global policies
- `GET /admin/user-by-epf/{epf}` - Search user by EPF
- `POST /admin/propose-policy` - Submit policy proposal
- `GET /admin/policy-proposals` - Get proposals (with filters)
- `GET /admin/special-policy-users` - Get users with special policies
- `POST /admin/remove-special-policy` - Remove special policy

**VC Endpoints:**
- `GET /vc/policy-proposals` - View all proposals
- `POST /vc/policy-proposals/approve` - Approve proposal
- `POST /vc/policy-proposals/reject` - Reject proposal

**User Endpoints:**
- `GET /user/my-policy/{epf}` - Get own policy limits

## Firestore Collections

### 1. `global_policies`
Stores current global policy values.

**Document: `current`**
```json
{
  "maxAttemptsPerDay": 5,
  "maxCopiesPerDoc": 5
}
```

### 2. `policy_proposals`
Stores all policy proposals.

**Global Policy Proposal:**
```json
{
  "id": "GP001",
  "type": "global",
  "adminEPF": "50001",
  "adminName": "Admin User",
  "justification": "High demand during exam season...",
  "status": "pending",
  "submittedAt": "2025-11-10T14:30:00Z",
  "changes": {
    "maxAttemptsPerDay": {
      "current": 5,
      "proposed": 7
    },
    "maxCopiesPerDoc": {
      "current": 5,
      "proposed": 8
    }
  },
  "vcDecision": null
}
```

**Special User Policy Proposal:**
```json
{
  "id": "SP001",
  "type": "special_user",
  "adminEPF": "50001",
  "adminName": "Admin User",
  "targetEPF": "60025",
  "targetName": "Maria Research",
  "targetDept": "Computer Science",
  "justification": "Research assistant needs higher limits...",
  "status": "pending",
  "submittedAt": "2025-11-11T09:00:00Z",
  "proposedPolicy": {
    "maxAttemptsPerDay": 15,
    "maxCopiesPerDoc": 20
  },
  "vcDecision": null
}
```

**After VC Decision:**
```json
{
  "vcDecision": {
    "decision": "approved",
    "notes": "Approved for academic purposes",
    "decidedBy": "VC 60001",
    "decidedAt": "2025-11-12T10:00:00Z"
  }
}
```

### 3. `user_special_policies`
Stores active special policies for users.

**Document ID: {userEPF}**
```json
{
  "epf": "60025",
  "name": "Maria Research",
  "department": "Computer Science",
  "specialPolicy": {
    "maxAttemptsPerDay": 15,
    "maxCopiesPerDoc": 20
  },
  "approvedAt": "2025-11-12T10:00:00Z",
  "approvedBy": "VC 60001",
  "justification": "Research assistant needs higher limits...",
  "proposalId": "SP001"
}
```

## Integration Steps

### Step 1: Add to Main FastAPI App

In your main FastAPI application file (e.g., `main.py` or `app.py`):

```python
from fastapi import FastAPI
from .api_policy_endpoints import router as policy_router

app = FastAPI()

# Include policy routes
app.include_router(policy_router, prefix="/api", tags=["policies"])
```

### Step 2: Update Authentication Middleware

Ensure your `auth.py` has these functions:

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify Firebase token and return user"""
    # Your existing token verification logic
    pass

async def verify_admin(current_user: dict = Depends(get_current_user)):
    """Verify user is admin"""
    if current_user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

async def verify_vc(current_user: dict = Depends(get_current_user)):
    """Verify user is VC"""
    if current_user.get('role') != 'vc':
        raise HTTPException(status_code=403, detail="VC access required")
    return current_user
```

### Step 3: Initialize Firestore Collections

Run this script once to initialize the collections:

```python
from firebase_admin import firestore

db = firestore.client()

# Initialize global policies
db.collection('global_policies').document('current').set({
    'maxAttemptsPerDay': 5,
    'maxCopiesPerDoc': 5
})

print("Global policies initialized!")
```

### Step 4: Update Firestore Security Rules

Add these rules to your `firestore.rules`:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    
    // Policy Proposals
    match /policy_proposals/{proposalId} {
      allow read: if request.auth != null && (
        get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role in ['admin', 'vc']
      );
      allow create: if request.auth != null && 
        get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'admin';
      allow update: if request.auth != null && 
        get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'vc';
    }
    
    // User Special Policies
    match /user_special_policies/{epf} {
      allow read: if request.auth != null && (
        get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role in ['admin', 'vc'] ||
        request.auth.uid == epf
      );
      allow write: if request.auth != null && 
        get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'vc';
    }
    
    // Global Policies
    match /global_policies/{docId} {
      allow read: if request.auth != null;
      allow write: if request.auth != null && 
        get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'vc';
    }
  }
}
```

Deploy the rules:
```bash
firebase deploy --only firestore:rules
```

### Step 5: Integrate with Print Job Validation

Update your print job validation to check user policies:

```python
from .policy_proposals import get_user_policy

async def validate_print_request(user_epf: str, num_copies: int):
    """Validate print request against user's policy"""
    
    # Get user's effective policy (special or global)
    policy = get_user_policy(user_epf)
    
    # Check copies limit
    if num_copies > policy['maxCopiesPerDoc']:
        raise Exception(f"Copies exceed limit of {policy['maxCopiesPerDoc']}")
    
    # Check daily attempts (you'll need to implement daily counter)
    # daily_attempts = get_user_daily_attempts(user_epf)
    # if daily_attempts >= policy['maxAttemptsPerDay']:
    #     raise Exception(f"Daily attempt limit of {policy['maxAttemptsPerDay']} reached")
    
    return True
```

## Testing

### Test 1: Create Global Policy Proposal
```bash
curl -X POST http://localhost:8000/api/admin/propose-policy \
  -H "Authorization: Bearer {admin_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "global",
    "adminEPF": "50001",
    "adminName": "Admin User",
    "justification": "Increasing limits for exam season",
    "changes": {
      "maxAttemptsPerDay": {"current": 5, "proposed": 7}
    }
  }'
```

### Test 2: Create Special User Policy Proposal
```bash
curl -X POST http://localhost:8000/api/admin/propose-policy \
  -H "Authorization: Bearer {admin_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "special_user",
    "adminEPF": "50001",
    "adminName": "Admin User",
    "targetEPF": "60025",
    "targetName": "Maria Research",
    "targetDept": "Computer Science",
    "justification": "Research assistant needs higher limits",
    "proposedPolicy": {
      "maxAttemptsPerDay": 15,
      "maxCopiesPerDoc": 20
    }
  }'
```

### Test 3: Approve Proposal (VC)
```bash
curl -X POST http://localhost:8000/api/vc/policy-proposals/approve \
  -H "Authorization: Bearer {vc_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "proposalId": "SP001",
    "vcId": "60001",
    "notes": "Approved for academic purposes"
  }'
```

### Test 4: Get User Policy
```bash
curl -X GET http://localhost:8000/api/user/my-policy/60025 \
  -H "Authorization: Bearer {user_token}"
```

## Frontend Integration

The frontend components are already created and ready:

1. **PolicyProposalTab.jsx** - Admin creates proposals
2. **SpecialUsersManagementTab.jsx** - Admin manages special users
3. **PolicyManagementTab.jsx** - VC approves/rejects proposals

Update `frontend/src/services/api.js` to use your backend URL:
```javascript
const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api'
```

## Troubleshooting

### Issue: 403 Forbidden on policy endpoints
**Solution:** Verify user role in Firestore users collection matches 'admin' or 'vc'

### Issue: Proposals not appearing
**Solution:** Check Firestore rules are deployed and token is valid

### Issue: Special policy not applying
**Solution:** Verify `user_special_policies` collection has document with user's EPF as ID

## Next Steps

1. ✅ Test all endpoints with Postman/curl
2. ✅ Deploy Firestore rules
3. ✅ Initialize global policies collection
4. ✅ Integrate policy checking into print workflow
5. ✅ Add usage statistics tracking for special users
6. ✅ Set up notification system for proposal approvals/rejections

## Support

For issues or questions:
- Check Firestore console for collection structure
- Verify Firebase Authentication tokens
- Check FastAPI logs for detailed error messages
