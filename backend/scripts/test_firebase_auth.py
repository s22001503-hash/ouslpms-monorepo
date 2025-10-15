"""
Test Firebase Authentication using the REST API directly
This bypasses any potential API key restrictions
"""
import os
import json
import requests

# Your Firebase Web API Key from firebaseConfig.js
API_KEY = "AIzaSyBw98pSudMcx_4T6Y-_ICTveOcFfqSKZz0"
EMAIL = "50005@ousl.edu.lk"
PASSWORD = "5000555"

def test_auth():
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    
    payload = {
        "email": EMAIL,
        "password": PASSWORD,
        "returnSecureToken": True
    }
    
    print(f"Testing authentication for: {EMAIL}")
    print(f"API Key: {API_KEY[:20]}...")
    print()
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ AUTHENTICATION SUCCESSFUL!")
            print(f"   User ID: {data.get('localId')}")
            print(f"   Email: {data.get('email')}")
            print(f"   ID Token (first 50 chars): {data.get('idToken', '')[:50]}...")
        else:
            print("❌ AUTHENTICATION FAILED!")
            print(f"   Status Code: {response.status_code}")
            print(f"   Response: {response.text}")
            
            error_data = response.json()
            error_msg = error_data.get('error', {}).get('message', 'Unknown error')
            
            if error_msg == "INVALID_LOGIN_CREDENTIALS" or error_msg == "INVALID_PASSWORD":
                print("\n   → The email/password combination is incorrect")
                print("   → Check if the password was set correctly in Firebase Console")
            elif error_msg == "EMAIL_NOT_FOUND":
                print("\n   → The email doesn't exist in Firebase Auth")
            elif error_msg == "USER_DISABLED":
                print("\n   → The user account is disabled")
            elif error_msg == "API_KEY_INVALID":
                print("\n   → The API key is invalid or has restrictions")
            else:
                print(f"\n   → Error: {error_msg}")
                
    except Exception as e:
        print(f"❌ Exception occurred: {e}")

if __name__ == '__main__':
    test_auth()
