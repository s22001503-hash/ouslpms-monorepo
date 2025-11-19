"""Quick login script - no user input required."""
import json
import requests
from pathlib import Path

BACKEND_URL = "http://localhost:8000"
AUTH_TOKEN_FILE = r"C:\AI_Prints\auth_token.txt"
FIREBASE_API_KEY = "AIzaSyBw98pSudMcx_4T6Y-_ICTveOcFfqSKZz0"

# Default to regular user
email = "99999@ousl.edu.lk"
password = "999999"

print(f"🔑 Logging in as: {email}")

FIREBASE_AUTH_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"

try:
    # Authenticate with Firebase
    response = requests.post(
        FIREBASE_AUTH_URL,
        json={"email": email, "password": password, "returnSecureToken": True}
    )
    
    if response.status_code != 200:
        print(f"❌ Firebase authentication failed: {response.text}")
        exit(1)
    
    data = response.json()
    id_token = data.get('idToken')
    local_id = data.get('localId')
    
    print(f"✅ Firebase authentication successful!")
    
    # Verify with backend
    verify_response = requests.post(
        f"{BACKEND_URL}/print/authorize",
        json={"token": id_token, "user_id": local_id}
    )
    
    if verify_response.status_code == 200:
        backend_data = verify_response.json()
        print(f"✅ Backend verification successful!")
        print(f"   EPF: {backend_data.get('user_id')}")
        print(f"   Role: {backend_data.get('role')}")
        
        # Save token
        token_data = {
            'token': id_token,
            'user_id': backend_data.get('user_id'),
            'role': backend_data.get('role'),
            'email': email
        }
        
        Path(AUTH_TOKEN_FILE).parent.mkdir(parents=True, exist_ok=True)
        with open(AUTH_TOKEN_FILE, 'w') as f:
            json.dump(token_data, f, indent=2)
        
        print(f"✅ Token saved to: {AUTH_TOKEN_FILE}")
        print(f"\n🎉 Login complete! You can now print.")
    else:
        print(f"❌ Backend verification failed: {verify_response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")
