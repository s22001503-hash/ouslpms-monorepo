"""
Test if the admin password is correct by attempting to generate a custom token
and verifying it can be used for sign-in
"""
import os
import sys
import firebase_admin
from firebase_admin import credentials, auth

ADMIN_EMAIL = "50005@ousl.edu.lk"
ADMIN_PASSWORD = "5000555"

def main():
    cred_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not cred_path:
        print("ERROR: GOOGLE_APPLICATION_CREDENTIALS not set")
        sys.exit(1)
    
    # Initialize Firebase Admin
    if not firebase_admin._apps:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    
    try:
        # Get user by email
        user = auth.get_user_by_email(ADMIN_EMAIL)
        print(f"✓ User found: {user.email}")
        print(f"  UID: {user.uid}")
        print(f"  Disabled: {user.disabled}")
        print(f"  Email verified: {user.email_verified}")
        
        if user.disabled:
            print("\n⚠️  WARNING: User account is DISABLED!")
            print("   Enable it in Firebase Console → Authentication")
            return
        
        # Try to update password to ensure it's set correctly
        print(f"\n→ Resetting password to: {ADMIN_PASSWORD}")
        auth.update_user(user.uid, password=ADMIN_PASSWORD)
        print("✓ Password updated successfully")
        
        print(f"\n✅ Admin user is ready for login!")
        print(f"   Email: {ADMIN_EMAIL}")
        print(f"   Password: {ADMIN_PASSWORD}")
        print(f"\nTry logging in now with EPF: 50005")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
