"""
Script to create a Dean user in Firebase Auth and Firestore for testing.
Run this after initializing Firebase Admin SDK.
"""

import os
import sys
import firebase_admin
from firebase_admin import auth, credentials, firestore
from datetime import datetime

# Initialize Firebase Admin SDK
cred_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'C:\\Users\\user\\Desktop\\OUspms\\backend\\firebase-adminsdk.json')

if os.path.exists(cred_path):
    cred = credentials.Certificate(cred_path)
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    print(f"✓ Firebase Admin SDK initialized with credentials from: {cred_path}")
else:
    print(f"✗ Credentials file not found at: {cred_path}")
    sys.exit(1)

# Dean user details
DEAN_EPF = "60001"
DEAN_EMAIL = "dean@ousl.lk"
DEAN_PASSWORD = "Dean123456"
DEAN_NAME = "Dr. John Dean"
DEAN_DEPARTMENT = "Administration"

def create_dean_user():
    """Create a dean user in Firebase Auth and Firestore."""
    try:
        # Check if user already exists
        try:
            existing_user = auth.get_user_by_email(DEAN_EMAIL)
            print(f"⚠ User already exists with email: {DEAN_EMAIL}")
            print(f"  UID: {existing_user.uid}")
            user_record = existing_user
        except auth.UserNotFoundError:
            # Create user in Firebase Auth
            user_record = auth.create_user(
                email=DEAN_EMAIL,
                password=DEAN_PASSWORD,
                display_name=DEAN_NAME
            )
            print(f"✓ Created Dean user in Firebase Auth")
            print(f"  Email: {DEAN_EMAIL}")
            print(f"  UID: {user_record.uid}")
        
        # Create/update user document in Firestore
        db = firestore.client()
        user_doc_ref = db.collection('users').document(DEAN_EPF)
        
        user_data = {
            'uid': user_record.uid,
            'epf': DEAN_EPF,
            'email': DEAN_EMAIL,
            'name': DEAN_NAME,
            'role': 'dean',
            'department': DEAN_DEPARTMENT,
            'status': 'active',
            'createdAt': datetime.now().isoformat() + 'Z',
            'lastLogin': None
        }
        
        user_doc_ref.set(user_data)
        print(f"✓ Created/Updated Dean user document in Firestore")
        print(f"  EPF: {DEAN_EPF}")
        print(f"  Role: dean")
        
        print("\n" + "="*60)
        print("DEAN USER CREATED SUCCESSFULLY!")
        print("="*60)
        print(f"Email: {DEAN_EMAIL}")
        print(f"Password: {DEAN_PASSWORD}")
        print(f"EPF: {DEAN_EPF}")
        print(f"Name: {DEAN_NAME}")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"✗ Error creating dean user: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = create_dean_user()
    sys.exit(0 if success else 1)
