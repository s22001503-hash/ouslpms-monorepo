"""Check if test users exist in Firestore with correct roles"""
import os
import sys
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'C:\\Users\\user\\Desktop\\OUspms\\backend\\firebase-adminsdk.json')
cred = credentials.Certificate(cred_path)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Check test users
test_users = {
    '99999': 'user',
    '50005': 'admin',
    '60001': 'dean'
}

print("\n" + "="*60)
print("CHECKING TEST USERS IN FIRESTORE")
print("="*60)

for epf, expected_role in test_users.items():
    doc = db.collection('users').document(epf).get()
    if doc.exists:
        data = doc.to_dict()
        actual_role = data.get('role', 'NONE')
        email = data.get('email', 'NONE')
        name = data.get('name', 'NONE')
        status = "✓" if actual_role == expected_role else "✗"
        print(f"\n{status} EPF: {epf}")
        print(f"  Name: {name}")
        print(f"  Email: {email}")
        print(f"  Role: {actual_role} (Expected: {expected_role})")
    else:
        print(f"\n✗ EPF: {epf} - NOT FOUND IN FIRESTORE")

print("\n" + "="*60)
