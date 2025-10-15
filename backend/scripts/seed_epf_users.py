"""
Seed script to create test users with EPF mapping in Firebase.

This script:
1. Creates users in Firebase Authentication
2. Creates EPF→email mappings in Firestore (epf_mapping collection)
3. Sets user roles in Firestore (users collection)

Usage:
    cd backend
    .venv\Scripts\python.exe scripts\seed_epf_users.py
"""

import firebase_admin
from firebase_admin import credentials, auth, firestore
import os
import sys

# Sample test users with EPF numbers
TEST_USERS = [
    {
        "epf": "12345",
        "email": "admin@ou.ac.lk",
        "password": "admin123",
        "display_name": "Admin User",
        "role": "admin"
    },
    {
        "epf": "67890",
        "email": "user@ou.ac.lk",
        "password": "user123",
        "display_name": "Regular User",
        "role": "user"
    },
    {
        "epf": "11111",
        "email": "john.doe@ou.ac.lk",
        "password": "john123",
        "display_name": "John Doe",
        "role": "user"
    }
]

def initialize_firebase():
    """Initialize Firebase Admin SDK."""
    # Check if already initialized
    if len(firebase_admin._apps) > 0:
        print("✓ Firebase already initialized")
        return firestore.client()
    
    # Look for service account file
    service_account_paths = [
        os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'),
        'firebase-adminsdk.json',
        '../firebase-adminsdk.json',
    ]
    
    cred_path = None
    for path in service_account_paths:
        if path and os.path.exists(path):
            cred_path = path
            break
    
    if not cred_path:
        print("❌ Error: Firebase service account JSON not found!")
        print("Please set GOOGLE_APPLICATION_CREDENTIALS environment variable")
        print("or place firebase-adminsdk.json in the backend directory.")
        sys.exit(1)
    
    print(f"✓ Using service account: {cred_path}")
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
    return firestore.client()

def create_or_update_user(user_data):
    """Create or update a Firebase Auth user."""
    try:
        # Try to get existing user
        try:
            user = auth.get_user_by_email(user_data['email'])
            print(f"  ↻ User {user_data['email']} already exists (uid: {user.uid})")
            # Update password if needed
            auth.update_user(user.uid, password=user_data['password'])
            return user.uid
        except auth.UserNotFoundError:
            # Create new user
            user = auth.create_user(
                email=user_data['email'],
                password=user_data['password'],
                display_name=user_data['display_name']
            )
            print(f"  ✓ Created user {user_data['email']} (uid: {user.uid})")
            return user.uid
    except Exception as e:
        print(f"  ❌ Error creating user {user_data['email']}: {e}")
        return None

def set_epf_mapping(db, epf, email, uid):
    """Set EPF→email mapping in Firestore."""
    try:
        db.collection('epf_mapping').document(epf).set({
            'email': email,
            'uid': uid
        })
        print(f"  ✓ EPF mapping: {epf} → {email}")
    except Exception as e:
        print(f"  ❌ Error setting EPF mapping: {e}")

def set_user_role(db, uid, role):
    """Set user role in Firestore."""
    try:
        db.collection('users').document(uid).set({
            'role': role
        })
        print(f"  ✓ Role set: {role}")
    except Exception as e:
        print(f"  ❌ Error setting role: {e}")

def main():
    print("=" * 60)
    print("🔥 Firebase EPF User Seeding Script")
    print("=" * 60)
    print()
    
    # Initialize Firebase
    db = initialize_firebase()
    print()
    
    # Create users
    print(f"Creating {len(TEST_USERS)} test users...")
    print()
    
    for user_data in TEST_USERS:
        print(f"Processing EPF {user_data['epf']} ({user_data['display_name']}):")
        
        # Create Firebase Auth user
        uid = create_or_update_user(user_data)
        if not uid:
            continue
        
        # Set EPF mapping
        set_epf_mapping(db, user_data['epf'], user_data['email'], uid)
        
        # Set user role
        set_user_role(db, uid, user_data['role'])
        
        print()
    
    print("=" * 60)
    print("✓ Seeding complete!")
    print()
    print("Test credentials:")
    print("-" * 60)
    for user_data in TEST_USERS:
        print(f"EPF: {user_data['epf']:10} | Email: {user_data['email']:25} | Password: {user_data['password']:10} | Role: {user_data['role']}")
    print("=" * 60)

if __name__ == '__main__':
    main()
