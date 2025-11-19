#!/usr/bin/env python3
"""
Verify VC user document and role
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
print("VERIFY VC USER - EPF 60002")
print("="*80)

vc_email = '60002@ousl.edu.lk'

try:
    # Get Auth user
    auth_user = auth.get_user_by_email(vc_email)
    print(f"\n✅ Firebase Auth User:")
    print(f"   Email: {auth_user.email}")
    print(f"   UID: {auth_user.uid}")
    
    # Get Firestore document
    user_doc = db.collection('users').document(auth_user.uid).get()
    
    if user_doc.exists:
        data = user_doc.to_dict()
        print(f"\n✅ Firestore User Document:")
        print(f"   Document ID: {auth_user.uid}")
        print(f"   EPF: {data.get('epf')}")
        print(f"   Name: {data.get('name')}")
        print(f"   Email: {data.get('email')}")
        print(f"   Role: '{data.get('role')}'")
        print(f"   Role Type: {type(data.get('role'))}")
        print(f"   Department: {data.get('department')}")
        
        # Check role value
        role = data.get('role')
        if role == 'vc':
            print(f"\n✅ Role is correctly set to 'vc'")
        else:
            print(f"\n❌ Role is '{role}' instead of 'vc'")
            print(f"   Fixing role...")
            db.collection('users').document(auth_user.uid).update({'role': 'vc'})
            print(f"   ✅ Role updated to 'vc'")
    else:
        print(f"\n❌ Firestore document not found!")
        print(f"   Creating document...")
        db.collection('users').document(auth_user.uid).set({
            'uid': auth_user.uid,
            'epf': '60002',
            'email': vc_email,
            'name': 'Vice Chancellor',
            'role': 'vc',
            'department': 'Administration'
        })
        print(f"   ✅ Document created")
    
    # Verify final state
    print("\n" + "="*80)
    final_doc = db.collection('users').document(auth_user.uid).get()
    final_data = final_doc.to_dict()
    print("FINAL VERIFICATION:")
    print("="*80)
    print(f"EPF: {final_data.get('epf')}")
    print(f"Email: {final_data.get('email')}")
    print(f"Role: '{final_data.get('role')}'")
    print(f"Name: {final_data.get('name')}")
    print("\n✅ Ready to login with EPF: 60002, Password: 6000222")
    print("="*80)
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

print()
