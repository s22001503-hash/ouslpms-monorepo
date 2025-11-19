"""
Firebase User Setup Script
Creates test users in Firebase Authentication and Firestore
"""

import firebase_admin
from firebase_admin import credentials, auth, firestore
from datetime import datetime
import os

# Initialize Firebase Admin
cred = credentials.Certificate('serviceAccountKey.json')
try:
    firebase_admin.initialize_app(cred)
except ValueError:
    # Already initialized
    pass

db = firestore.client()

def create_test_users():
    """Create test users for the system"""
    
    test_users = [
        {
            'email': 'admin@ousl.lk',
            'password': 'Admin@123',
            'displayName': 'System Administrator',
            'role': 'admin',
            'department': 'IT',
            'employeeId': 'ADMIN001'
        },
        {
            'email': 'dean@ousl.lk',
            'password': 'Dean@123',
            'displayName': 'Dean of Faculty',
            'role': 'dean',
            'department': 'Engineering',
            'employeeId': 'DEAN001'
        },
        {
            'email': 'user@ousl.lk',
            'password': 'User@123',
            'displayName': 'Test User',
            'role': 'user',
            'department': 'Engineering',
            'employeeId': 'USER001'
        },
        {
            'email': 'lecturer@ousl.lk',
            'password': 'Lecturer@123',
            'displayName': 'Test Lecturer',
            'role': 'lecturer',
            'department': 'Computing',
            'employeeId': 'LECT001'
        }
    ]
    
    print("\n🔧 Creating Test Users in Firebase...\n")
    print("=" * 70)
    
    for user_data in test_users:
        try:
            # Create Firebase Auth user
            try:
                user = auth.create_user(
                    email=user_data['email'],
                    password=user_data['password'],
                    display_name=user_data['displayName'],
                    email_verified=True
                )
                uid = user.uid
                print(f"\n✅ Created Auth user: {user_data['email']}")
            except auth.EmailAlreadyExistsError:
                # User already exists in Auth, get UID
                user = auth.get_user_by_email(user_data['email'])
                uid = user.uid
                print(f"\n✓  Auth user exists: {user_data['email']}")
            
            # Create/Update Firestore user document
            user_doc = {
                'email': user_data['email'],
                'displayName': user_data['displayName'],
                'role': user_data['role'],
                'department': user_data['department'],
                'employeeId': user_data['employeeId'],
                'createdAt': firestore.SERVER_TIMESTAMP,
                'updatedAt': firestore.SERVER_TIMESTAMP,
                'isActive': True,
                'printQuota': {
                    'daily': 50,
                    'monthly': 500,
                    'used': 0
                }
            }
            
            db.collection('users').document(uid).set(user_doc, merge=True)
            print(f"✅ Created Firestore document for: {user_data['email']}")
            print(f"   UID: {uid}")
            print(f"   Role: {user_data['role']}")
            print(f"   Department: {user_data['department']}")
            
        except Exception as e:
            print(f"❌ Error creating user {user_data['email']}: {str(e)}")
    
    print("\n" + "=" * 70)
    print("\n✅ User Setup Complete!\n")
    
    # Display credentials
    print("📋 TEST CREDENTIALS:")
    print("-" * 70)
    for user_data in test_users:
        print(f"\n{user_data['displayName']} ({user_data['role'].upper()})")
        print(f"  Email:    {user_data['email']}")
        print(f"  Password: {user_data['password']}")
    print("\n" + "-" * 70)

def create_default_policies():
    """Create default print policies"""
    
    print("\n🔧 Creating Default Policies...\n")
    print("=" * 70)
    
    # System-wide fallback policy
    system_policy = {
        'name': 'System Default Policy',
        'description': 'Default fallback policy for all users',
        'type': 'system',
        'rules': {
            'official': {
                'allowed': True,
                'max_copies': 5,
                'max_pages': 50,
                'daily_limit': 100,
                'requires_approval': False
            },
            'personal': {
                'allowed': False,
                'max_copies': 0,
                'max_pages': 0,
                'daily_limit': 0,
                'requires_approval': True
            },
            'confidential': {
                'allowed': True,
                'max_copies': 1,
                'max_pages': 20,
                'daily_limit': 10,
                'requires_approval': True
            }
        },
        'createdAt': firestore.SERVER_TIMESTAMP,
        'updatedAt': firestore.SERVER_TIMESTAMP,
        'isActive': True
    }
    
    db.collection('policies').document('system_default').set(system_policy)
    print("✅ Created system default policy")
    
    # Admin role policy
    admin_policy = {
        'name': 'Administrator Policy',
        'description': 'Policy for administrators - no restrictions',
        'type': 'role',
        'roleId': 'admin',
        'rules': {
            'official': {
                'allowed': True,
                'max_copies': 999,
                'max_pages': 999,
                'daily_limit': 999,
                'requires_approval': False
            },
            'personal': {
                'allowed': True,
                'max_copies': 10,
                'max_pages': 100,
                'daily_limit': 50,
                'requires_approval': False
            },
            'confidential': {
                'allowed': True,
                'max_copies': 999,
                'max_pages': 999,
                'daily_limit': 999,
                'requires_approval': False
            }
        },
        'createdAt': firestore.SERVER_TIMESTAMP,
        'updatedAt': firestore.SERVER_TIMESTAMP,
        'isActive': True
    }
    
    db.collection('policies').document('role_admin').set(admin_policy)
    print("✅ Created admin role policy")
    
    # User role policy
    user_policy = {
        'name': 'Standard User Policy',
        'description': 'Policy for regular users',
        'type': 'role',
        'roleId': 'user',
        'rules': {
            'official': {
                'allowed': True,
                'max_copies': 3,
                'max_pages': 30,
                'daily_limit': 50,
                'requires_approval': False
            },
            'personal': {
                'allowed': False,
                'max_copies': 0,
                'max_pages': 0,
                'daily_limit': 0,
                'requires_approval': True
            },
            'confidential': {
                'allowed': False,
                'max_copies': 0,
                'max_pages': 0,
                'daily_limit': 0,
                'requires_approval': True
            }
        },
        'createdAt': firestore.SERVER_TIMESTAMP,
        'updatedAt': firestore.SERVER_TIMESTAMP,
        'isActive': True
    }
    
    db.collection('policies').document('role_user').set(user_policy)
    print("✅ Created user role policy")
    
    print("\n" + "=" * 70)
    print("\n✅ Policies Setup Complete!\n")

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("  FIREBASE USER & POLICY SETUP")
    print("=" * 70)
    
    create_test_users()
    create_default_policies()
    
    print("\n🎉 Setup Complete!")
    print("\nYou can now:")
    print("  1. Login to the frontend with any of the test credentials")
    print("  2. The file watcher will use service account (no login needed)")
    print("  3. Check Firebase console to verify users and policies\n")
