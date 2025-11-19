#!/usr/bin/env python3
"""
Migrate user documents from EPF-based IDs to UID-based IDs
This ensures consistent storage and enables proper Firestore security rules
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
print("USER DOCUMENT MIGRATION - EPF to UID")
print("="*80)

# Get all Firebase Auth users indexed by email
auth_users_by_email = {}
page = auth.list_users()
for user in page.iterate_all():
    auth_users_by_email[user.email] = {
        'uid': user.uid,
        'email': user.email
    }

print(f"\n📊 Found {len(auth_users_by_email)} Firebase Auth users")

# Find EPF-based documents that need migration
users_ref = db.collection('users')
epf_based_docs = []

for doc in users_ref.stream():
    doc_id = doc.id
    data = doc.to_dict()
    
    # Check if this is an EPF-based document (numeric ID)
    if doc_id.isdigit():
        epf_based_docs.append({
            'old_doc_id': doc_id,
            'data': data
        })

print(f"\n⚠️  Found {len(epf_based_docs)} EPF-based documents to migrate:")
for doc in epf_based_docs:
    print(f"   - EPF: {doc['old_doc_id']} | Email: {doc['data'].get('email', 'N/A')}")

# Confirm migration
print("\n" + "="*80)
response = input("Do you want to proceed with migration? (yes/no): ").strip().lower()

if response != 'yes':
    print("❌ Migration cancelled.")
    exit(0)

print("\n🔄 Starting migration...")
print("="*80)

migrated_count = 0
failed_count = 0
skipped_count = 0

for doc in epf_based_docs:
    old_doc_id = doc['old_doc_id']
    data = doc['data']
    email = data.get('email')
    
    print(f"\n📝 Processing EPF {old_doc_id}...")
    
    if not email:
        print(f"   ⚠️  SKIP: No email found for EPF {old_doc_id}")
        skipped_count += 1
        continue
    
    # Find matching Auth user by email
    if email not in auth_users_by_email:
        print(f"   ⚠️  SKIP: No Auth user found for email {email}")
        skipped_count += 1
        continue
    
    new_uid = auth_users_by_email[email]['uid']
    
    try:
        # Check if UID-based document already exists
        uid_doc = db.collection('users').document(new_uid).get()
        
        if uid_doc.exists:
            print(f"   ℹ️  Document already exists at UID {new_uid[:20]}...")
            print(f"   🔄 Updating existing document with data from EPF {old_doc_id}")
            
            # Merge data, keeping UID document as primary
            existing_data = uid_doc.to_dict()
            merged_data = {**data, **existing_data}  # Existing data takes precedence
            merged_data['epf'] = old_doc_id  # Ensure EPF is stored as field
            merged_data['uid'] = new_uid  # Ensure UID is stored as field
            
            db.collection('users').document(new_uid).set(merged_data)
            print(f"   ✅ Updated UID document")
        else:
            # Create new UID-based document
            data['epf'] = old_doc_id  # Store EPF as field
            data['uid'] = new_uid  # Store UID as field
            
            db.collection('users').document(new_uid).set(data)
            print(f"   ✅ Created new document at UID {new_uid[:20]}...")
        
        # Delete old EPF-based document
        db.collection('users').document(old_doc_id).delete()
        print(f"   🗑️  Deleted old EPF document {old_doc_id}")
        
        migrated_count += 1
        
    except Exception as e:
        print(f"   ❌ FAILED: {str(e)}")
        failed_count += 1

# Summary
print("\n" + "="*80)
print("MIGRATION SUMMARY")
print("="*80)
print(f"✅ Successfully migrated: {migrated_count}")
print(f"⚠️  Skipped: {skipped_count}")
print(f"❌ Failed: {failed_count}")

if migrated_count > 0:
    print(f"\n🎉 Migration completed successfully!")
    print(f"\nNext steps:")
    print(f"1. Update frontend LoginPage.jsx to query by UID instead of EPF")
    print(f"2. Update Firestore rules to use request.auth.uid")
    print(f"3. Test authentication with migrated users")
else:
    print(f"\n⚠️  No documents were migrated.")

print("="*80)
