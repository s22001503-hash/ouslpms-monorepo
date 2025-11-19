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
print("CURRENT USER POLICIES")
print("="*70)

policies = db.collection('policies').stream()
for policy in policies:
    data = policy.to_dict()
    print(f"\nEPF: {data.get('user_id', 'N/A')}")
    print(f"  Role: {data.get('role', 'N/A')}")
    print(f"  Max Daily Prints: {data.get('max_daily_print_attempts', 0)}")
    print(f"  Max Copies/Doc: {data.get('max_copies_per_document', 0)}")
    print(f"  Allow Personal: {data.get('allow_personal_prints', False)}")

print("\n" + "="*70)
print("DEAN ACCOUNTS (for testing):")
print("="*70)
print("  EPF002: max 20 daily, 20 copies, NO personal")
print("  60001:  max 20 daily, 20 copies, NO personal")
print("\n" + "="*70)
