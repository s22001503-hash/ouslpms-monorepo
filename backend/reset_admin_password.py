"""
Utility script to reset admin password in Firebase
Usage: python reset_admin_password.py
"""
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth, firestore
import os

# Set up Firebase Admin
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\user\Desktop\OUspms\backend\firebase-adminsdk.json'
cred = credentials.Certificate(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

def reset_password(epf: str, new_password: str):
    """Reset password for a user by EPF"""
    try:
        # Get user document from Firestore
        db = firestore.client()
        user_doc = db.collection('users').document(epf).get()
        
        if not user_doc.exists:
            print(f'❌ User with EPF {epf} not found in Firestore')
            return False
        
        user_data = user_doc.to_dict()
        uid = user_data.get('uid')
        email = user_data.get('email')
        name = user_data.get('name')
        
        if not uid:
            print(f'❌ UID not found for EPF {epf}')
            return False
        
        # Update password in Firebase Auth
        firebase_auth.update_user(uid, password=new_password)
        
        print(f'✅ Password reset successfully!')
        print(f'   Name: {name}')
        print(f'   EPF: {epf}')
        print(f'   Email: {email}')
        print(f'   UID: {uid}')
        print(f'   New Password: {new_password}')
        
        return True
        
    except Exception as e:
        print(f'❌ Error resetting password: {e}')
        return False

if __name__ == '__main__':
    print('='*60)
    print('Firebase Admin Password Reset Utility')
    print('='*60)
    
    # Reset admin password
    epf = input('\nEnter EPF number (default: 50005): ').strip() or '50005'
    new_password = input('Enter new password (default: 5000555): ').strip() or '5000555'
    
    print(f'\n🔄 Resetting password for EPF {epf}...')
    
    if reset_password(epf, new_password):
        print(f'\n✅ You can now login with:')
        print(f'   EPF: {epf}')
        print(f'   Password: {new_password}')
    else:
        print(f'\n❌ Password reset failed')
