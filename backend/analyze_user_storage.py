#!/usr/bin/env python3
"""
Analyze user document storage patterns and identify inconsistencies
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
print("USER STORAGE ANALYSIS - Checking for UID vs EPF inconsistencies")
print("="*80)

# Get all Firebase Auth users
auth_users = {}
page = auth.list_users()
for user in page.iterate_all():
    auth_users[user.uid] = {
        'email': user.email,
        'uid': user.uid
    }

print(f"\n📊 Found {len(auth_users)} Firebase Auth users")

# Get all Firestore user documents
firestore_docs = {}
users_ref = db.collection('users')
for doc in users_ref.stream():
    firestore_docs[doc.id] = doc.to_dict()

print(f"📊 Found {len(firestore_docs)} Firestore user documents")

# Analyze patterns
print("\n" + "="*80)
print("DOCUMENT ID PATTERNS")
print("="*80)

uid_pattern = []
epf_pattern = []
unknown_pattern = []

for doc_id, data in firestore_docs.items():
    # Check if doc_id looks like a UID (Firebase UIDs are 28 characters alphanumeric)
    if len(doc_id) > 20 and any(c.isalpha() for c in doc_id):
        uid_pattern.append({
            'doc_id': doc_id,
            'email': data.get('email', 'N/A'),
            'epf': data.get('epf', 'N/A'),
            'role': data.get('role', 'N/A')
        })
    # Check if doc_id is numeric (likely EPF)
    elif doc_id.isdigit():
        epf_pattern.append({
            'doc_id': doc_id,
            'email': data.get('email', 'N/A'),
            'epf': data.get('epf', 'N/A'),
            'role': data.get('role', 'N/A')
        })
    else:
        unknown_pattern.append({
            'doc_id': doc_id,
            'email': data.get('email', 'N/A'),
            'epf': data.get('epf', 'N/A'),
            'role': data.get('role', 'N/A')
        })

print(f"\n✅ Documents using UID as ID: {len(uid_pattern)}")
for user in uid_pattern:
    print(f"   - {user['doc_id'][:20]}... | Email: {user['email']} | EPF: {user['epf']} | Role: {user['role']}")

print(f"\n⚠️  Documents using EPF as ID: {len(epf_pattern)}")
for user in epf_pattern:
    print(f"   - {user['doc_id']} | Email: {user['email']} | EPF: {user['epf']} | Role: {user['role']}")

if unknown_pattern:
    print(f"\n❓ Documents with unknown pattern: {len(unknown_pattern)}")
    for user in unknown_pattern:
        print(f"   - {user['doc_id']} | Email: {user['email']} | EPF: {user['epf']} | Role: {user['role']}")

# Check for orphaned documents
print("\n" + "="*80)
print("ORPHAN CHECK")
print("="*80)

orphaned = []
for doc_id, data in firestore_docs.items():
    # If doc_id looks like UID, check if it exists in auth
    if len(doc_id) > 20 and doc_id not in auth_users:
        orphaned.append({
            'doc_id': doc_id,
            'email': data.get('email', 'N/A'),
            'reason': 'UID-based doc but no matching Auth user'
        })

if orphaned:
    print(f"⚠️  Found {len(orphaned)} orphaned documents:")
    for doc in orphaned:
        print(f"   - {doc['doc_id']} | {doc['email']} | {doc['reason']}")
else:
    print("✅ No orphaned documents found")

# Recommendation
print("\n" + "="*80)
print("RECOMMENDATION")
print("="*80)

print(f"""
Current State:
- UID-based documents: {len(uid_pattern)}
- EPF-based documents: {len(epf_pattern)}

⚠️  INCONSISTENT STORAGE DETECTED!

Recommended Solution:
1. Migrate all EPF-based documents to UID-based storage
2. Keep EPF as a field within the document (not as doc ID)
3. Update all code that queries by EPF to query by UID
4. Update Firestore rules to use request.auth.uid consistently

This will:
✅ Ensure proper security rules (can use request.auth.uid)
✅ Align with Firebase best practices
✅ Simplify authentication flow
✅ Enable proper role-based access control
""")

print("="*80)
