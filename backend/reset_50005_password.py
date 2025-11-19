#!/usr/bin/env python3
"""Reset password for user 50005"""
import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase
cred = credentials.Certificate('serviceAccountKey.json')
try:
    firebase_admin.get_app()
except:
    firebase_admin.initialize_app(cred)

EPF = '50005'
EMAIL = f'{EPF}@ousl.edu.lk'
NEW_PASSWORD = '5000555'  # User's requested password

try:
    # Get user
    user = auth.get_user_by_email(EMAIL)
    print(f"✅ Found user: {user.email}")
    print(f"   UID: {user.uid}")
    
    # Update password
    auth.update_user(user.uid, password=NEW_PASSWORD)
    print(f"\n✅ Password updated to: {NEW_PASSWORD}")
    print(f"\n🎯 You can now login with:")
    print(f"   EPF: {EPF}")
    print(f"   Password: {NEW_PASSWORD}")
    
except auth.UserNotFoundError:
    print(f"❌ User {EMAIL} not found")
    print("\nAvailable admin users:")
    print("  - admin@ousl.lk")
    print("  - 99999@ousl.edu.lk")
except Exception as e:
    print(f"❌ Error: {e}")
