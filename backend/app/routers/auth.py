from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel
import os
import firebase_admin
from firebase_admin import auth as firebase_auth, credentials, firestore

router = APIRouter()

class TokenVerifyRequest(BaseModel):
    idToken: str

class CreateUserRequest(BaseModel):
    epf: str
    email: str
    password: str
    role: str = 'user'  # default to 'user'
    department: str = ''
    name: str = ''

class DeleteUserRequest(BaseModel):
    epf: str

class ChangePasswordRequest(BaseModel):
    currentPassword: str
    newPassword: str

# Admin verification dependency
async def verify_admin(authorization: str = Header(None)):
    """Verify that the request comes from an authenticated admin user."""
    if not authorization or not authorization.startswith('Bearer '):
        raise HTTPException(status_code=401, detail='Missing or invalid authorization header')
    
    token = authorization.split(' ', 1)[1]
    
    if not firebase_admin._apps:
        raise HTTPException(status_code=500, detail='Firebase Admin not configured')
    
    try:
        # Verify the token
        decoded = firebase_auth.verify_id_token(token)
        uid = decoded.get('uid')
        
        # Get user's role from Firestore
        db = firestore.client()
        
        # Try document by UID first
        doc_ref = db.collection('users').document(uid)
        doc = doc_ref.get()
        
        if doc.exists:
            role = doc.to_dict().get('role', 'user')
        else:
            # Try query by uid field
            users_ref = db.collection('users')
            query = users_ref.where('uid', '==', uid).limit(1)
            results = list(query.stream())
            
            if results:
                role = results[0].to_dict().get('role', 'user')
            else:
                raise HTTPException(status_code=403, detail='User not found in database')
        
        if role != 'admin':
            raise HTTPException(status_code=403, detail='Admin access required')
        
        return uid
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail=f'Token verification failed: {str(e)}')

# initialize firebase admin with better diagnostics and Certificate usage
cred = None
import json as _json
import sys as _sys
_sa_env = os.getenv('FIREBASE_SERVICE_ACCOUNT')
_gac_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
print(f"DEBUG: FIREBASE_SERVICE_ACCOUNT set: {_sa_env is not None}")
print(f"DEBUG: GOOGLE_APPLICATION_CREDENTIALS={_gac_path}")

if _sa_env:
    try:
        _sa = _json.loads(_sa_env)
        cred = credentials.Certificate(_sa)
    except Exception as _e:
        print(f"DEBUG: Failed to parse FIREBASE_SERVICE_ACCOUNT env var: {_e}", file=_sys.stderr)
elif _gac_path:
    # prefer reading the file with Certificate so project_id is available
    if os.path.exists(_gac_path):
        try:
            cred = credentials.Certificate(_gac_path)
        except Exception as _e:
            print(f"DEBUG: Failed to load credentials from {_gac_path}: {_e}", file=_sys.stderr)
    else:
        print(f"DEBUG: Service account file not found at {_gac_path}", file=_sys.stderr)
else:
    print("DEBUG: No Firebase credential environment variables found", file=_sys.stderr)

if cred:
    try:
        firebase_admin.initialize_app(cred)
        print("DEBUG: Firebase Admin initialized successfully")
    except Exception as _e:
        # already initialized or other issue
        print(f"DEBUG: firebase_admin.initialize_app exception: {_e}", file=_sys.stderr)

@router.post('/verify')
async def verify_token(req: TokenVerifyRequest):
    if not firebase_admin._apps:
        raise HTTPException(status_code=500, detail='Firebase Admin not configured')
    try:
        decoded = firebase_auth.verify_id_token(req.idToken)
        uid = decoded.get('uid')
        
        # Fetch user role from firestore
        # Strategy: Try to find user doc by searching for EPF or UID
        db = firestore.client()
        
        # First, try to find by UID (if user doc uses UID as ID)
        doc_ref = db.collection('users').document(uid)
        doc = doc_ref.get()
        
        role = 'user'
        epf = None
        
        if doc.exists:
            data = doc.to_dict()
            role = data.get('role', 'user')
            epf = data.get('epf')
        else:
            # UID lookup failed - try to find document where uid field matches
            # This handles the case where EPF is the document ID
            users_ref = db.collection('users')
            query = users_ref.where('uid', '==', uid).limit(1)
            results = query.stream()
            
            for doc in results:
                data = doc.to_dict()
                role = data.get('role', 'user')
                epf = doc.id  # The document ID is the EPF
                break
        
        return {'uid': uid, 'role': role, 'epf': epf}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post('/create-user')
async def create_user(req: CreateUserRequest, admin_uid: str = Depends(verify_admin)):
    """Create a new Firebase Auth user and corresponding Firestore document. (Admin only)"""
    if not firebase_admin._apps:
        raise HTTPException(status_code=500, detail='Firebase Admin not configured')
    
    try:
        # Create Firebase Auth user
        user_record = firebase_auth.create_user(
            email=req.email,
            password=req.password,
            display_name=req.name if req.name else None
        )
        
        uid = user_record.uid
        
        # Create Firestore document in users collection (keyed by EPF)
        db = firestore.client()
        user_doc_ref = db.collection('users').document(req.epf)
        user_doc_ref.set({
            'uid': uid,
            'epf': req.epf,
            'email': req.email,
            'role': req.role,
            'department': req.department,
            'name': req.name,
            'createdAt': firestore.SERVER_TIMESTAMP
        })
        
        # Log admin action
        try:
            db.collection('admin_actions').add({
                'action': 'create_user',
                'admin_uid': admin_uid,
                'target_epf': req.epf,
                'target_uid': uid,
                'target_email': req.email,
                'target_role': req.role,
                'timestamp': firestore.SERVER_TIMESTAMP,
                'details': f'Admin {admin_uid} created user {req.epf} ({req.email}) with role {req.role}'
            })
        except Exception as log_err:
            # Don't fail the request if logging fails
            print(f'Warning: Failed to log admin action: {log_err}')
        
        return {
            'success': True,
            'uid': uid,
            'epf': req.epf,
            'name': req.name,
            'message': f'"{req.name}" (EPF:{req.epf}) created successfully'
        }
    except firebase_auth.EmailAlreadyExistsError:
        raise HTTPException(status_code=400, detail='Email already exists')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to create user: {str(e)}')

@router.post('/delete-user')
async def delete_user(req: DeleteUserRequest, admin_uid: str = Depends(verify_admin)):
    """Delete a Firebase Auth user and corresponding Firestore document. (Admin only)"""
    if not firebase_admin._apps:
        raise HTTPException(status_code=500, detail='Firebase Admin not configured')
    
    db = firestore.client()
    doc_ref = db.collection('users').document(req.epf)
    doc = doc_ref.get()
    
    if not doc.exists:
        raise HTTPException(status_code=404, detail=f'User with EPF {req.epf} not found')
    
    user_data = doc.to_dict()
    uid = user_data.get('uid')
    email = user_data.get('email')
    name = user_data.get('name', 'Unknown User')
    
    try:
        # Delete from Firestore first
        doc_ref.delete()
        
        # Then delete from Auth
        if uid:
            try:
                firebase_auth.delete_user(uid)
            except Exception as auth_err:
                # User might already be deleted from Auth but not Firestore
                print(f'Warning: Failed to delete Auth user {uid}: {auth_err}')
        
        # Log admin action
        try:
            db.collection('admin_actions').add({
                'action': 'delete_user',
                'admin_uid': admin_uid,
                'target_epf': req.epf,
                'target_uid': uid or 'unknown',
                'target_email': email or 'unknown',
                'timestamp': firestore.SERVER_TIMESTAMP,
                'details': f'Admin {admin_uid} deleted user {req.epf} ({email})'
            })
        except Exception as log_err:
            print(f'Warning: Failed to log admin action: {log_err}')
        
        return {
            'status': 'success',
            'epf': req.epf,
            'name': name,
            'message': f'"{name}" (EPF:{req.epf}) deleted successfully'
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Failed to delete user: {str(e)}')

@router.post('/change-password')
async def change_password(req: ChangePasswordRequest, authorization: str = Header(None)):
    """Change password for the authenticated user. Requires current password verification."""
    if not firebase_admin._apps:
        raise HTTPException(status_code=500, detail='Firebase Admin not configured')
    
    # Verify authorization
    if not authorization or not authorization.startswith('Bearer '):
        raise HTTPException(status_code=401, detail='Missing or invalid authorization header')
    
    token = authorization.split(' ', 1)[1]
    
    try:
        # Verify the ID token and get user info
        decoded_token = firebase_auth.verify_id_token(token)
        uid = decoded_token.get('uid')
        email = decoded_token.get('email')
        
        if not uid or not email:
            raise HTTPException(status_code=401, detail='Invalid token: missing user information')
        
        # Verify current password by attempting to sign in
        # Note: Firebase Admin SDK doesn't have a direct way to verify password
        # We need to use the Firebase Authentication REST API for this
        import requests
        import json
        
        # Get the API key from environment or Firebase config
        firebase_api_key = os.environ.get('FIREBASE_API_KEY', 'AIzaSyBw98pSudMcx_4T6Y-_ICTveOcFfqSKZz0')
        
        # Verify current password using Firebase REST API
        verify_url = f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={firebase_api_key}'
        verify_payload = {
            'email': email,
            'password': req.currentPassword,
            'returnSecureToken': True
        }
        
        print(f'[DEBUG] Verifying password for email: {email}')
        print(f'[DEBUG] Current password length: {len(req.currentPassword)}')
        
        verify_response = requests.post(verify_url, json=verify_payload)
        
        print(f'[DEBUG] Firebase REST API response status: {verify_response.status_code}')
        print(f'[DEBUG] Firebase REST API response: {verify_response.text}')
        
        if verify_response.status_code != 200:
            # Try to get more specific error message from Firebase
            try:
                error_data = verify_response.json()
                error_message = error_data.get('error', {}).get('message', 'Current password is incorrect')
                raise HTTPException(status_code=400, detail=f'Current password is incorrect: {error_message}')
            except:
                raise HTTPException(status_code=400, detail='Current password is incorrect')
        
        # Update password using Admin SDK
        firebase_auth.update_user(uid, password=req.newPassword)
        
        # Optional: Log the password change
        try:
            db = firestore.client()
            db.collection('admin_actions').add({
                'action': 'change_password',
                'user_uid': uid,
                'user_email': email,
                'timestamp': firestore.SERVER_TIMESTAMP,
                'details': f'User {email} changed their password'
            })
        except Exception as log_err:
            print(f'Warning: Failed to log password change: {log_err}')
        
        return {
            'success': True,
            'message': 'Password changed successfully'
        }
        
    except HTTPException:
        raise
    except firebase_auth.InvalidIdTokenError:
        raise HTTPException(status_code=401, detail='Invalid or expired token')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to change password: {str(e)}')
