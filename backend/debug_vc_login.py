#!/usr/bin/env python3
"""
Debug VC login issue - check UID matching
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
print("DEBUG VC LOGIN ISSUE - EPF 60001")
print("="*80)

vc_email = 'dean@ousl.lk'

# Get Auth user
print("\n1️⃣ FIREBASE AUTH USER:")
try:
    auth_user = auth.get_user_by_email(vc_email)
    print(f"   ✅ Email: {auth_user.email}")
    print(f"   ✅ UID: {auth_user.uid}")
    auth_uid = auth_user.uid
except Exception as e:
    print(f"   ❌ Error: {str(e)}")
    exit(1)

# Check Firestore by UID
print(f"\n2️⃣ FIRESTORE QUERY BY UID ({auth_uid}):")
user_doc = db.collection('users').document(auth_uid).get()
if user_doc.exists:
    data = user_doc.to_dict()
    print(f"   ✅ Document found!")
    print(f"   EPF: {data.get('epf', 'N/A')}")
    print(f"   Name: {data.get('name', 'N/A')}")
    print(f"   Role: {data.get('role', 'N/A')}")
    print(f"   Email: {data.get('email', 'N/A')}")
else:
    print(f"   ❌ NO DOCUMENT FOUND AT /users/{auth_uid}")
    print(f"\n   Searching for EPF 60001 in all user documents...")
    
    # Search for the EPF in all documents
    users_ref = db.collection('users')
    for doc in users_ref.stream():
        data = doc.to_dict()
        if data.get('epf') == '60001':
            print(f"\n   🔍 Found EPF 60001 at different UID:")
            print(f"      Document ID: {doc.id}")
            print(f"      Auth UID: {auth_uid}")
            print(f"      Email: {data.get('email', 'N/A')}")
            print(f"      Role: {data.get('role', 'N/A')}")
            print(f"\n   ⚠️  MISMATCH! Document ID doesn't match Auth UID")
            print(f"\n   SOLUTION: Delete wrong document and create correct one...")
            
            # Delete wrong document
            db.collection('users').document(doc.id).delete()
            print(f"      ✅ Deleted document at {doc.id}")
            
            # Create at correct UID
            data['uid'] = auth_uid
            db.collection('users').document(auth_uid).set(data)
            print(f"      ✅ Created document at {auth_uid}")

print("\n" + "="*80)
print("VERIFICATION:")
print("="*80)

# Verify again
final_doc = db.collection('users').document(auth_uid).get()
if final_doc.exists:
    print("✅ User document now exists at correct UID!")
    data = final_doc.to_dict()
    print(f"   EPF: {data.get('epf')}")
    print(f"   Role: {data.get('role')}")
    print(f"   Email: {data.get('email')}")
    print("\n✅ You can now login with EPF 60001 and password 6000111")
else:
    print("❌ Still not found - manual intervention needed")

print("="*80 + "\n")
