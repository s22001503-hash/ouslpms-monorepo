"""
Simple test login - Creates a mock token for testing authentication.
For production, use the actual Firebase login flow from the frontend.
"""
import json
from pathlib import Path

AUTH_TOKEN_FILE = r"C:\AI_Prints\auth_token.txt"

print("="*60)
print("🔑 Mock Login for Testing")
print("="*60)
print()
print("Creating a test authentication token...")
print("Note: This is for TESTING ONLY. In production, use Firebase Auth.")
print()

# Create a mock token (in production, this would be a real Firebase ID token)
token_data = {
    'token': 'mock_token_for_testing',
    'user_id': '99999',
    'role': 'user',
    'email': '99999@ousl.edu.lk'
}

try:
    Path(AUTH_TOKEN_FILE).parent.mkdir(parents=True, exist_ok=True)
    with open(AUTH_TOKEN_FILE, 'w') as f:
        json.dump(token_data, f, indent=2)
    
    print(f"✅ Mock token created: {AUTH_TOKEN_FILE}")
    print(f"   User: {token_data['user_id']}")
    print(f"   Role: {token_data['role']}")
    print()
    print("⚠️  IMPORTANT: Restart the agent to load the new token!")
    print()
    print("After restarting, REQUIRE_AUTH must be set to False for mock tokens to work,")
    print("OR implement a test mode in the backend that accepts mock tokens.")
    
except Exception as e:
    print(f"❌ Failed to create token: {e}")

input("\nPress Enter to close...")
