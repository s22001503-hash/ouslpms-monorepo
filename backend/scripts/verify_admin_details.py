"""
Verify the exact email and details in Firebase Auth for the admin user
"""
import os
import sys
import firebase_admin
from firebase_admin import credentials, auth

ADMIN_EPF = "50005"

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
        user = auth.get_user_by_email("50005@ousl.edu.lk")
        
        print("=" * 60)
        print("FIREBASE AUTH USER DETAILS")
        print("=" * 60)
        print(f"UID:           {user.uid}")
        print(f"Email:         {user.email}")
        print(f"Display Name:  {user.display_name}")
        print(f"Disabled:      {user.disabled}")
        print(f"Email Verified: {user.email_verified}")
        print(f"Provider Data: {user.provider_data}")
        print("=" * 60)
        
        # Now check Firestore
        from firebase_admin import firestore
        db = firestore.client()
        doc_ref = db.collection('users').document(ADMIN_EPF)
        doc = doc_ref.get()
        
        if doc.exists:
            data = doc.to_dict()
            print("\nFIRESTORE DOCUMENT (users/50005)")
            print("=" * 60)
            print(f"UID:        {data.get('uid')}")
            print(f"Email:      {data.get('email')}")
            print(f"EPF:        {data.get('epf')}")
            print(f"Role:       {data.get('role')}")
            print(f"Name:       {data.get('name')}")
            print("=" * 60)
            
            # Check for mismatches
            print("\nVERIFICATION")
            print("=" * 60)
            if user.uid == data.get('uid'):
                print("✓ UIDs match")
            else:
                print(f"✗ UID MISMATCH! Auth: {user.uid}, Firestore: {data.get('uid')}")
            
            if user.email == data.get('email'):
                print("✓ Emails match")
            else:
                print(f"✗ EMAIL MISMATCH! Auth: {user.email}, Firestore: {data.get('email')}")
            
            print("=" * 60)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
