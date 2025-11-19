"""
Simple Groq API Key Verification Script
Tests if the API key is valid and working
"""

import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

def test_groq_api_key():
    """Test if Groq API key is valid"""
    
    print("=" * 70)
    print("GROQ API KEY VERIFICATION")
    print("=" * 70)
    
    # Get API key
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("\n✗ GROQ_API_KEY not found in environment variables")
        print("\nPlease add it to backend/.env file:")
        print("GROQ_API_KEY=gsk_xxxxxxxxxxxxx")
        return False
    
    print(f"\n✓ API Key found: {api_key[:10]}...{api_key[-5:]}")
    print(f"  Length: {len(api_key)} characters")
    
    # Test API connection
    print("\nTesting API connection...")
    print("-" * 70)
    
    try:
        client = Groq(api_key=api_key)
        
        # Simple test request
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": "Say 'Hello, API is working!' in exactly 5 words."
                }
            ],
            temperature=0.1,
            max_tokens=20
        )
        
        result = response.choices[0].message.content
        
        print(f"\n✓ API Connection Successful!")
        print(f"\nResponse from Groq:")
        print(f"  {result}")
        
        print(f"\nModel: {response.model}")
        print(f"Tokens used: {response.usage.total_tokens}")
        
        print("\n" + "=" * 70)
        print("✓ GROQ API KEY IS VALID AND WORKING!")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        error_message = str(e)
        
        print(f"\n✗ API Connection Failed!")
        print(f"\nError: {error_message}")
        
        if "401" in error_message or "Invalid API Key" in error_message:
            print("\n" + "=" * 70)
            print("ISSUE: Invalid or Expired API Key")
            print("=" * 70)
            print("\nPossible solutions:")
            print("1. Go to https://console.groq.com/keys")
            print("2. Delete the existing API key")
            print("3. Create a new API key")
            print("4. Copy the new key (starts with 'gsk_')")
            print("5. Replace GROQ_API_KEY in backend/.env file")
            print("\nNOTE: API keys can expire or be revoked.")
            
        elif "429" in error_message or "rate limit" in error_message.lower():
            print("\n" + "=" * 70)
            print("ISSUE: Rate Limit Exceeded")
            print("=" * 70)
            print("\nYou've exceeded the API rate limit.")
            print("Wait a few minutes and try again.")
            
        elif "network" in error_message.lower() or "connection" in error_message.lower():
            print("\n" + "=" * 70)
            print("ISSUE: Network Connection Problem")
            print("=" * 70)
            print("\nCheck your internet connection.")
            
        else:
            print("\n" + "=" * 70)
            print("ISSUE: Unknown Error")
            print("=" * 70)
            print("\nPlease check:")
            print("1. Your Groq account is active")
            print("2. The API key hasn't been deleted")
            print("3. Your internet connection")
        
        print("\n" + "=" * 70)
        
        return False


if __name__ == "__main__":
    success = test_groq_api_key()
    
    if not success:
        print("\n⚠️  Please fix the API key issue before running tests.")
        exit(1)
    else:
        print("\n🎉 Ready to run classification tests!")
        exit(0)
