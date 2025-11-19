#!/usr/bin/env python3
"""
Reset VC password for EPF 60001
"""
import firebase_admin
from firebase_admin import credentials, auth, firestore

# Initialize Firebase
cred = credentials.Certificate('serviceAccountKey.json')
try:
    firebase_admin.get_app()
except:
    firebase_admin.initialize_app(cred)

db = firestore.client()

print("\n" + "="*80)
print("RESET VC PASSWORD - EPF 60001")
print("="*80)

# Find VC user by email
vc_email = 'dean@ousl.lk'  # Based on migration results
new_password = '6000111'

try:
    # Get user by email
    user = auth.get_user_by_email(vc_email)
    
    print(f"\n✅ Found VC user:")
    print(f"   Email: {user.email}")
    print(f"   UID: {user.uid}")
    
    # Update password
    auth.update_user(user.uid, password=new_password)
    print(f"\n✅ Password updated to: {new_password}")
    
    # Verify user document in Firestore
    user_doc = db.collection('users').document(user.uid).get()
    if user_doc.exists:
        data = user_doc.to_dict()
        print(f"\n📄 Firestore User Document:")
        print(f"   EPF: {data.get('epf', 'N/A')}")
        print(f"   Name: {data.get('name', 'N/A')}")
        print(f"   Role: {data.get('role', 'N/A')}")
        print(f"   Department: {data.get('department', 'N/A')}")
        
        # Update role to 'vc' if not already
        if data.get('role') != 'vc':
            print(f"\n⚠️  Current role is '{data.get('role')}', updating to 'vc'...")
            db.collection('users').document(user.uid).update({'role': 'vc'})
            print(f"   ✅ Role updated to 'vc'")
    else:
        print(f"\n⚠️  Warning: User document not found in Firestore")
    
    print("\n" + "="*80)
    print("LOGIN CREDENTIALS:")
    print("="*80)
    print(f"EPF: 60001")
    print(f"Password: {new_password}")
    print(f"Email: {vc_email}")
    print("="*80)
    
except auth.UserNotFoundError:
    print(f"\n❌ Error: No user found with email {vc_email}")
    print(f"\nAvailable VC users in the system:")
    
    # Search for users with VC role
    users_ref = db.collection('users')
    for doc in users_ref.stream():
        data = doc.to_dict()
        if data.get('role') == 'vc':
            print(f"   - EPF: {data.get('epf', 'N/A')} | Email: {data.get('email', 'N/A')} | UID: {doc.id[:20]}...")

except Exception as e:
    print(f"\n❌ Error: {str(e)}")

print()
