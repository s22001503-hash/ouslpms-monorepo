#!/usr/bin/env python3
"""Check Firebase Authentication users"""
import firebase_admin
from firebase_admin import credentials, auth, firestore

# Initialize Firebase
cred = credentials.Certificate('serviceAccountKey.json')
try:
    firebase_admin.get_app()
except:
    firebase_admin.initialize_app(cred)

print("\n" + "="*70)
print("FIREBASE AUTHENTICATION USERS")
print("="*70)

# List all Firebase Auth users
page = auth.list_users()
count = 0
for user in page.iterate_all():
    count += 1
    print(f"\n{count}. Email: {user.email}")
    print(f"   UID: {user.uid}")
    print(f"   Disabled: {user.disabled}")
    if count >= 10:  # Limit to first 10
        break

print("\n" + "="*70)
print(f"Total Firebase Auth users: {count}")
print("="*70)

# Check Firestore users collection
print("\n" + "="*70)
print("FIRESTORE USERS COLLECTION")
print("="*70)

db = firestore.client()
users_ref = db.collection('users')
users = users_ref.limit(10).stream()

count = 0
for user in users:
    count += 1
    data = user.to_dict()
    print(f"\n{count}. Doc ID: {user.id}")
    print(f"   Email: {data.get('email', 'N/A')}")
    print(f"   Role: {data.get('role', 'N/A')}")
    print(f"   EPF: {data.get('epf', 'N/A')}")
    print(f"   UID: {data.get('uid', 'N/A')}")

print("\n" + "="*70)
print(f"Total Firestore user documents: {count}")
print("="*70)
print("\n✅ If you see users listed, Firebase is working correctly.")
print("⚠️  The permission error is likely from the browser - make sure you're logged in to the web app!\n")
