import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate('serviceAccountKey.json')
try:
    firebase_admin.get_app()
except:
    firebase_admin.initialize_app(cred)

db = firestore.client()

print("\n" + "="*70)
print("FIXING POLICIES - Setting allow_personal_prints")
print("="*70)

# Update all policies
policies_ref = db.collection('policies')
policies = policies_ref.stream()

for policy_doc in policies:
    data = policy_doc.to_dict()
    user_id = data.get('user_id', 'N/A')
    
    # Set allow_personal_prints based on role
    role = data.get('role', 'user')
    allow_personal = True if role == 'admin' else False
    
    # Update the policy
    policies_ref.document(policy_doc.id).update({
        'allow_personal_prints': allow_personal
    })
    
    if user_id != 'N/A':
        print(f"✅ Updated {user_id} ({role}): allow_personal = {allow_personal}")

print("\n" + "="*70)
print("POLICIES FIXED!")
print("="*70)
