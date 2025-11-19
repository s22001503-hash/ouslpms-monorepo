import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta

# Initialize Firebase
cred = credentials.Certificate('serviceAccountKey.json')
try:
    firebase_admin.get_app()
except:
    firebase_admin.initialize_app(cred)

db = firestore.client()

print("\n" + "="*70)
print("PRINT JOBS FOR USER 'user' TODAY")
print("="*70)

# Get today's date
today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

# Query print jobs
jobs_ref = db.collection('print_jobs')
jobs = jobs_ref.where('user_id', '==', 'user').stream()

count = 0
for job in jobs:
    count += 1
    data = job.to_dict()
    print(f"\n{count}. Filename: {data.get('filename', 'N/A')}")
    print(f"   Classification: {data.get('classification', 'N/A')}")
    print(f"   Timestamp: {data.get('timestamp', 'N/A')}")
    print(f"   Status: {data.get('status', 'N/A')}")

print("\n" + "="*70)
print(f"Total prints today for 'user': {count}")
print("="*70)

print("\n⚠️  ISSUE IDENTIFIED:")
print("  • The file watcher uses Windows username 'user'")
print("  • But policies are for EPF numbers (99999, 60001, etc.)")
print("  • We need to link Windows user to EPF number!")
print("\n")
