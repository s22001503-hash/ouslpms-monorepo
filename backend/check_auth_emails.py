import firebase_admin
from firebase_admin import auth as firebase_auth

# Initialize Firebase Admin (if not already initialized)
try:
    firebase_admin.get_app()
    print("✓ Firebase Admin already initialized")
except ValueError:
    import os
    cred_path = r'C:\Users\user\Desktop\OUspms\backend\firebase-adminsdk.json'
    cred = firebase_admin.credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
    print("✓ Firebase Admin initialized")

print("\n=== Checking Firebase Auth Users ===\n")

# List all users
page = firebase_auth.list_users()
users_found = []

for user in page.users:
    users_found.append({
        'uid': user.uid,
        'email': user.email,
        'display_name': user.display_name
    })

# Sort by email
users_found.sort(key=lambda x: x['email'] or '')

print(f"Found {len(users_found)} users in Firebase Auth:\n")
for user in users_found:
    print(f"Email: {user['email']}")
    print(f"  UID: {user['uid']}")
    print(f"  Display Name: {user['display_name'] or 'N/A'}")
    print()

print("\n=== Expected Emails for Login ===")
print("If using EPF format {epf}@ousl.edu.lk:")
print("  - EPF 99999 → 99999@ousl.edu.lk")
print("  - EPF 50005 → 50005@ousl.edu.lk")
print("  - EPF 60001 → 60001@ousl.edu.lk")
print("\nActual emails may differ!")
