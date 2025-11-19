"""
Simple test script to authenticate the virtual printer agent.
This simulates a user login by creating an auth token file.
"""
import json
import requests
from pathlib import Path

# Configuration
BACKEND_URL = "http://localhost:8000"
AUTH_TOKEN_FILE = r"C:\AI_Prints\auth_token.txt"

def login_with_firebase(email: str, password: str):
    """
    Authenticate with Firebase and save token to file.
    This simulates the frontend login process.
    """
    print(f"🔑 Attempting to authenticate: {email}")
    
    # Firebase Web API endpoint for authentication
    FIREBASE_API_KEY = "AIzaSyBw98pSudMcx_4T6Y-_ICTveOcFfqSKZz0"
    FIREBASE_AUTH_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    
    try:
        # Authenticate with Firebase
        response = requests.post(
            FIREBASE_AUTH_URL,
            json={
                "email": email,
                "password": password,
                "returnSecureToken": True
            }
        )
        
        if response.status_code != 200:
            print(f"❌ Firebase authentication failed: {response.text}")
            return None
        
        data = response.json()
        id_token = data.get('idToken')
        local_id = data.get('localId')
        
        print(f"✅ Firebase authentication successful!")
        print(f"   User ID: {local_id}")
        
        # Verify token with backend
        verify_response = requests.post(
            f"{BACKEND_URL}/print/authorize",
            json={
                "token": id_token,
                "user_id": local_id
            }
        )
        
        if verify_response.status_code == 200:
            backend_data = verify_response.json()
            print(f"✅ Backend verification successful!")
            print(f"   EPF: {backend_data.get('user_id')}")
            print(f"   Role: {backend_data.get('role')}")
            
            # Save token to file
            token_data = {
                'token': id_token,
                'user_id': backend_data.get('user_id'),
                'role': backend_data.get('role'),
                'email': email
            }
            
            # Ensure directory exists
            Path(AUTH_TOKEN_FILE).parent.mkdir(parents=True, exist_ok=True)
            
            with open(AUTH_TOKEN_FILE, 'w') as f:
                json.dump(token_data, f, indent=2)
            
            print(f"✅ Token saved to: {AUTH_TOKEN_FILE}")
            print(f"\n🎉 Agent authentication complete! You can now print.")
            return token_data
        else:
            print(f"❌ Backend verification failed: {verify_response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error during login: {e}")
        return None


def logout():
    """Remove auth token file."""
    try:
        if Path(AUTH_TOKEN_FILE).exists():
            Path(AUTH_TOKEN_FILE).unlink()
            print(f"✅ Logged out - Token file removed")
        else:
            print("ℹ️ No active session found")
    except Exception as e:
        print(f"❌ Error during logout: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("🖨️  EcoPrint Virtual Printer - Agent Login Utility")
    print("=" * 60)
    print()
    print("This utility authenticates the print agent with Firebase Auth.")
    print("Once authenticated, the agent can process print jobs.")
    print()
    
    print("Available test users:")
    print("1. Regular User - EPF: 99999 (Email: 99999@ousl.edu.lk, Password: 999999)")
    print("2. Admin User   - EPF: 50005 (Email: 50005@ousl.edu.lk, Password: 5000555)")
    print("3. Dean User    - EPF: 60001 (Email: 60001@ousl.edu.lk, Password: Dean123456)")
    print("4. Logout")
    print()
    
    choice = input("Select option (1-4): ").strip()
    
    if choice == "1":
        login_with_firebase("99999@ousl.edu.lk", "999999")
    elif choice == "2":
        login_with_firebase("50005@ousl.edu.lk", "5000555")
    elif choice == "3":
        login_with_firebase("60001@ousl.edu.lk", "Dean123456")
    elif choice == "4":
        logout()
    else:
        print("❌ Invalid choice")
