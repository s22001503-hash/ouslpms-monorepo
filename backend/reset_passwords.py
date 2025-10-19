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

print("\n=== Resetting Passwords for Test Users ===\n")

# Reset User password (EPF 99999)
try:
    user = firebase_auth.get_user_by_email('99999@ousl.edu.lk')
    firebase_auth.update_user(
        user.uid,
        password='999999'
    )
    print("✓ User (99999@ousl.edu.lk)")
    print("  Password reset to: 999999")
    print(f"  UID: {user.uid}\n")
except Exception as e:
    print(f"✗ Failed to reset User password: {e}\n")

# Reset Admin password (EPF 50005)
try:
    user = firebase_auth.get_user_by_email('50005@ousl.edu.lk')
    firebase_auth.update_user(
        user.uid,
        password='5000555'
    )
    print("✓ Admin (50005@ousl.edu.lk)")
    print("  Password reset to: 5000555")
    print(f"  UID: {user.uid}\n")
except Exception as e:
    print(f"✗ Failed to reset Admin password: {e}\n")

# Reset Dean password (EPF 60001)
try:
    user = firebase_auth.get_user_by_email('60001@ousl.edu.lk')
    firebase_auth.update_user(
        user.uid,
        password='Dean123456'
    )
    print("✓ Dean (60001@ousl.edu.lk)")
    print("  Password reset to: Dean123456")
    print(f"  UID: {user.uid}\n")
except Exception as e:
    print(f"✗ Failed to reset Dean password: {e}\n")

print("\n=== Login Credentials Summary ===")
print("User Login:")
print("  EPF: 99999")
print("  Password: 999999")
print("  Email: 99999@ousl.edu.lk\n")

print("Admin Login:")
print("  EPF: 50005")
print("  Password: 5000555")
print("  Email: 50005@ousl.edu.lk\n")

print("Dean Login:")
print("  EPF: 60001")
print("  Password: Dean123456")
print("  Email: 60001@ousl.edu.lk\n")

print("✓ All passwords have been reset!")
