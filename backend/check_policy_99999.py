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
print("CHECKING POLICY FOR EPF 99999")
print("="*70)

# Check policy
policies = db.collection('policies').where('user_id', '==', '99999').stream()

found = False
for policy in policies:
    found = True
    data = policy.to_dict()
    print("\n✅ Policy found!")
    print(f"  user_id: {data.get('user_id')}")
    print(f"  role: {data.get('role')}")
    print(f"  max_daily_print_attempts: {data.get('max_daily_print_attempts')}")
    print(f"  max_copies_per_document: {data.get('max_copies_per_document')}")
    print(f"  allow_personal_prints: {data.get('allow_personal_prints')}")

if not found:
    print("\n❌ NO POLICY FOUND for user_id='99999'")
    print("\nAll policies in database:")
    all_policies = db.collection('policies').stream()
    for p in all_policies:
        d = p.to_dict()
        user_id = d.get('user_id', 'N/A')
        if user_id != 'N/A':
            print(f"  - {user_id}")

print("\n" + "="*70)
