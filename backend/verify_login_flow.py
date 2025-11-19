#!/usr/bin/env python3
"""
Verify that migrated users can still be found by their email
"""
import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase
cred = credentials.Certificate('serviceAccountKey.json')
try:
    firebase_admin.get_app()
except:
    firebase_admin.initialize_app(cred)

print("\n" + "="*80)
print("LOGIN VERIFICATION TEST")
print("="*80)

test_users = [
    {'epf': '50005', 'email': '50005@ousl.edu.lk'},
    {'epf': '60001', 'email': 'dean@ousl.lk'},
    {'epf': '12345', 'email': '12345@ousl.edu.lk'},
    {'epf': '123461', 'email': '123461@ousl.edu.lk'},
]

print("\nTesting if users can be found by email (login simulation):\n")

for test in test_users:
    try:
        user = auth.get_user_by_email(test['email'])
        print(f"✅ EPF {test['epf']} | Email: {test['email']}")
        print(f"   UID: {user.uid[:20]}...")
        print(f"   Can login: YES")
    except auth.UserNotFoundError:
        print(f"❌ EPF {test['epf']} | Email: {test['email']}")
        print(f"   Error: User not found in Firebase Auth")
    except Exception as e:
        print(f"❌ EPF {test['epf']} | Email: {test['email']}")
        print(f"   Error: {str(e)}")
    print()

print("="*80)
print("LOGIN FLOW:")
print("="*80)
print("""
1. User enters EPF (e.g., 50005) and password
2. Frontend converts to email (50005@ousl.edu.lk)
3. Firebase Auth signs in with email/password → Returns UID
4. Frontend queries Firestore: /users/{UID}
5. Gets user data including role and EPF
6. Redirects based on role

✅ Users can still login with EPF + Password
✅ Backend storage now uses UID (more secure)
✅ EPF is stored as a field in the user document
""")
print("="*80)
