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
print("UPDATING POLICIES WITH COPY LIMITS")
print("="*70)

# Update all policies with max_copies_per_document
policies_ref = db.collection('policies')
policies = policies_ref.stream()

for policy_doc in policies:
    data = policy_doc.to_dict()
    user_id = data.get('user_id', 'N/A')
    role = data.get('role', 'user')
    
    # Set copy limits based on role
    if role == 'admin':
        max_copies = 100
    elif role in ['dean', 'lecturer']:
        max_copies = 20
    else:  # user
        max_copies = 5
    
    # Update the policy
    policies_ref.document(policy_doc.id).update({
        'max_copies_per_document': max_copies
    })
    
    print(f"✅ Updated {user_id} ({role}): max_copies = {max_copies}")

print("\n" + "="*70)
print("FINAL POLICIES:")
print("="*70)

policies = db.collection('policies').stream()
for policy in policies:
    data = policy.to_dict()
    user_id = data.get('user_id', 'N/A')
    if user_id != 'N/A':
        print(f"\nEPF: {user_id}")
        print(f"  Role: {data.get('role', 'N/A')}")
        print(f"  Max Daily: {data.get('max_daily_print_attempts', 0)}")
        print(f"  Max Copies: {data.get('max_copies_per_document', 0)}")
        print(f"  Allow Personal: {data.get('allow_personal_prints', False)}")

print("\n" + "="*70)
