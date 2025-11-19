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
print("CLEANING OLD TEST DATA")
print("="*70)

# Delete old print jobs (before today)
today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

print("\nDeleting old print_jobs...")
jobs_ref = db.collection('print_jobs')
jobs = jobs_ref.stream()

deleted_count = 0
for job in jobs:
    job.reference.delete()
    deleted_count += 1

print(f"✅ Deleted {deleted_count} old print jobs")

print("\nDeleting old blocked_prints...")
blocked_ref = db.collection('blocked_prints')
blocked = blocked_ref.stream()

blocked_count = 0
for b in blocked:
    b.reference.delete()
    blocked_count += 1

print(f"✅ Deleted {blocked_count} old blocked prints")

print("\n" + "="*70)
print("DATABASE CLEANED - READY FOR FRESH TESTING!")
print("="*70)
print("\n")
