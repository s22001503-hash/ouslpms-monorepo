"""
Script to delete existing Dean user and create a new one in Firebase Auth and Firestore.
Run this to reset the Dean account with new credentials.
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

def delete_existing_dean_user():
    """Delete existing dean user from Firebase Auth and Firestore."""
    try:
        db = firestore.client()
        
        # Try to delete from Firebase Auth by email
        try:
            existing_user = auth.get_user_by_email(DEAN_EMAIL)
            auth.delete_user(existing_user.uid)
            print(f"✓ Deleted existing user from Firebase Auth (UID: {existing_user.uid})")
        except auth.UserNotFoundError:
            print(f"  No existing user found in Firebase Auth with email: {DEAN_EMAIL}")
        except Exception as e:
            print(f"⚠ Warning: Could not delete from Firebase Auth: {str(e)}")
        
        # Delete from Firestore
        user_doc_ref = db.collection('users').document(DEAN_EPF)
        if user_doc_ref.get().exists:
            user_doc_ref.delete()
            print(f"✓ Deleted existing user document from Firestore (EPF: {DEAN_EPF})")
        else:
            print(f"  No existing user document found in Firestore with EPF: {DEAN_EPF}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error deleting existing dean user: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def create_new_dean_user():
    """Create a new dean user in Firebase Auth and Firestore."""
    try:
        # Create user in Firebase Auth
        user_record = auth.create_user(
            email=DEAN_EMAIL,
            password=DEAN_PASSWORD,
            display_name=DEAN_NAME
        )
        print(f"✓ Created new Dean user in Firebase Auth")
        print(f"  Email: {DEAN_EMAIL}")
        print(f"  UID: {user_record.uid}")
        
        # Create user document in Firestore
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
        print(f"✓ Created new Dean user document in Firestore")
        print(f"  EPF: {DEAN_EPF}")
        print(f"  Role: dean")
        
        return True
        
    except Exception as e:
        print(f"✗ Error creating new dean user: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def reset_dean_user():
    """Delete existing dean user and create a new one."""
    print("\n" + "="*60)
    print("RESETTING DEAN USER")
    print("="*60 + "\n")
    
    print("Step 1: Deleting existing Dean user...")
    print("-" * 60)
    if not delete_existing_dean_user():
        print("\n⚠ Warning: Deletion had issues, but continuing with creation...")
    
    print("\n" + "-" * 60)
    print("Step 2: Creating new Dean user...")
    print("-" * 60)
    if not create_new_dean_user():
        print("\n✗ Failed to create new dean user")
        return False
    
    print("\n" + "="*60)
    print("DEAN USER RESET SUCCESSFULLY!")
    print("="*60)
    print(f"Email:    {DEAN_EMAIL}")
    print(f"Password: {DEAN_PASSWORD}")
    print(f"EPF:      {DEAN_EPF}")
    print(f"Name:     {DEAN_NAME}")
    print(f"Role:     dean")
    print("="*60 + "\n")
    
    print("You can now log in to the Dean Dashboard with these credentials.")
    
    return True

if __name__ == '__main__':
    success = reset_dean_user()
    sys.exit(0 if success else 1)
