"""
Create or verify admin user exists in Firebase Auth and Firestore
"""
import os
import sys
import firebase_admin
from firebase_admin import credentials, auth, firestore

# Admin user details
ADMIN_EPF = "50005"
ADMIN_EMAIL = "50005@ousl.edu.lk"
ADMIN_PASSWORD = "5000555"
ADMIN_NAME = "Admin User"
ADMIN_DEPARTMENT = "IT"

def main():
    cred_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not cred_path:
        print("ERROR: GOOGLE_APPLICATION_CREDENTIALS not set")
        sys.exit(1)
    
    print(f"Using credentials: {cred_path}")
    
    # Initialize Firebase Admin
    if not firebase_admin._apps:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    
    db = firestore.client()
    
    # Check if user exists in Auth
    auth_user_exists = False
    auth_uid = None
    try:
        user = auth.get_user_by_email(ADMIN_EMAIL)
        auth_user_exists = True
        auth_uid = user.uid
        print(f"✓ Auth user exists: {ADMIN_EMAIL} (UID: {auth_uid})")
    except auth.UserNotFoundError:
        print(f"✗ Auth user NOT found: {ADMIN_EMAIL}")
    except Exception as e:
        print(f"✗ Error checking Auth user: {e}")
        sys.exit(1)
    
    # Check if Firestore doc exists
    firestore_doc_exists = False
    firestore_uid = None
    try:
        doc_ref = db.collection('users').document(ADMIN_EPF)
        doc = doc_ref.get()
        if doc.exists:
            firestore_doc_exists = True
            data = doc.to_dict()
            firestore_uid = data.get('uid')
            print(f"✓ Firestore doc exists: users/{ADMIN_EPF} (UID: {firestore_uid}, role: {data.get('role')})")
        else:
            print(f"✗ Firestore doc NOT found: users/{ADMIN_EPF}")
    except Exception as e:
        print(f"✗ Error checking Firestore: {e}")
        sys.exit(1)
    
    # Create or fix as needed
    if not auth_user_exists:
        print(f"\n→ Creating Auth user: {ADMIN_EMAIL}")
        try:
            user = auth.create_user(
                email=ADMIN_EMAIL,
                password=ADMIN_PASSWORD,
                display_name=ADMIN_NAME
            )
            auth_uid = user.uid
            print(f"✓ Created Auth user: UID={auth_uid}")
        except Exception as e:
            print(f"✗ Failed to create Auth user: {e}")
            sys.exit(1)
    
    if not firestore_doc_exists or firestore_uid != auth_uid:
        print(f"\n→ Creating/updating Firestore doc: users/{ADMIN_EPF}")
        try:
            doc_ref = db.collection('users').document(ADMIN_EPF)
            doc_ref.set({
                'uid': auth_uid,
                'epf': ADMIN_EPF,
                'email': ADMIN_EMAIL,
                'role': 'admin',
                'name': ADMIN_NAME,
                'department': ADMIN_DEPARTMENT,
                'status': 'active',
                'createdAt': firestore.SERVER_TIMESTAMP
            })
            print(f"✓ Created/updated Firestore doc: users/{ADMIN_EPF}")
        except Exception as e:
            print(f"✗ Failed to create Firestore doc: {e}")
            sys.exit(1)
    
    print("\n✅ Admin user is ready!")
    print(f"   Email: {ADMIN_EMAIL}")
    print(f"   Password: {ADMIN_PASSWORD}")
    print(f"   EPF: {ADMIN_EPF}")
    print(f"   UID: {auth_uid}")
    print(f"   Role: admin")

if __name__ == '__main__':
    main()
