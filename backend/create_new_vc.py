#!/usr/bin/env python3
"""
Create new VC user with EPF 60002
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
print("CREATE NEW VC USER - EPF 60002")
print("="*80)

# Step 1: Delete old VC (EPF 60001) if exists
print("\n1️⃣ Deleting old VC (EPF 60001)...")
try:
    # Find by email
    old_vc = auth.get_user_by_email('dean@ousl.lk')
    # Delete from Auth
    auth.delete_user(old_vc.uid)
    print(f"   ✅ Deleted from Firebase Auth: {old_vc.uid}")
    
    # Delete from Firestore
    db.collection('users').document(old_vc.uid).delete()
    print(f"   ✅ Deleted from Firestore")
except auth.UserNotFoundError:
    print(f"   ℹ️  Old VC not found in Auth (already deleted)")
except Exception as e:
    print(f"   ⚠️  Error: {str(e)}")

# Step 2: Create new VC user
print("\n2️⃣ Creating new VC user...")
new_epf = '60002'
new_email = f'{new_epf}@ousl.edu.lk'
new_password = '6000222'

try:
    # Create in Firebase Auth
    user = auth.create_user(
        email=new_email,
        password=new_password,
        display_name='Vice Chancellor'
    )
    print(f"   ✅ Created in Firebase Auth")
    print(f"      Email: {user.email}")
    print(f"      UID: {user.uid}")
    
    # Create in Firestore
    user_data = {
        'uid': user.uid,
        'epf': new_epf,
        'email': new_email,
        'name': 'Vice Chancellor',
        'role': 'vc',
        'department': 'Administration',
        'createdAt': firestore.SERVER_TIMESTAMP
    }
    
    db.collection('users').document(user.uid).set(user_data)
    print(f"   ✅ Created in Firestore at /users/{user.uid}")
    
    print("\n" + "="*80)
    print("✅ NEW VC USER CREATED SUCCESSFULLY!")
    print("="*80)
    print(f"EPF: {new_epf}")
    print(f"Password: {new_password}")
    print(f"Email: {new_email}")
    print(f"Role: vc")
    print("="*80)
    
except auth.EmailAlreadyExistsError:
    print(f"   ❌ Email {new_email} already exists")
    print(f"   Trying to update existing user...")
    
    # Get existing user and update
    existing_user = auth.get_user_by_email(new_email)
    auth.update_user(existing_user.uid, password=new_password)
    
    # Update Firestore
    db.collection('users').document(existing_user.uid).set({
        'uid': existing_user.uid,
        'epf': new_epf,
        'email': new_email,
        'name': 'Vice Chancellor',
        'role': 'vc',
        'department': 'Administration'
    })
    
    print(f"   ✅ Updated existing user")
    print(f"   EPF: {new_epf}")
    print(f"   Password: {new_password}")
    
except Exception as e:
    print(f"   ❌ Error: {str(e)}")

print()
