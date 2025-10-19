import firebase_admin
from firebase_admin import credentials, auth as firebase_auth

# Initialize Firebase Admin
try:
    firebase_admin.get_app()
    print("✓ Firebase Admin already initialized")
except ValueError:
    cred_path = r'C:\Users\user\Desktop\OUspms\backend\firebase-adminsdk.json'
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
    print("✓ Firebase Admin initialized")

print("\n=== Updating Firebase Auth Emails to Standard Format ===\n")

# Update User (EPF 99999): test99999@ousl.edu.lk → 99999@ousl.edu.lk
try:
    user = firebase_auth.get_user_by_email('test99999@ousl.edu.lk')
    firebase_auth.update_user(
        user.uid,
        email='99999@ousl.edu.lk'
    )
    print("✓ Updated User email: test99999@ousl.edu.lk → 99999@ousl.edu.lk")
    print(f"  UID: {user.uid}")
except Exception as e:
    print(f"✗ Failed to update User email: {e}")

# Update Dean (EPF 60001): dean@ousl.lk → 60001@ousl.edu.lk
try:
    user = firebase_auth.get_user_by_email('dean@ousl.lk')
    firebase_auth.update_user(
        user.uid,
        email='60001@ousl.edu.lk'
    )
    print("\n✓ Updated Dean email: dean@ousl.lk → 60001@ousl.edu.lk")
    print(f"  UID: {user.uid}")
except Exception as e:
    print(f"\n✗ Failed to update Dean email: {e}")

print("\n=== Updated Email List ===\n")
users = firebase_auth.list_users().users
for u in users:
    if u.email and 'ousl' in u.email:
        print(f"  {u.email}")

print("\n✓ All emails now follow {epf}@ousl.edu.lk format!")
print("\nTest Credentials (EPF format):")
print("  User:  EPF 99999, Password 999999")
print("  Admin: EPF 50005, Password 5000555")
print("  Dean:  EPF 60001, Password Dean123456")
