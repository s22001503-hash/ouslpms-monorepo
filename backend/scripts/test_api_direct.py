"""
Direct Groq API Key Test (bypasses cache)
"""

import sys
from pathlib import Path
from groq import Groq

# Read .env file directly
env_file = Path(__file__).parent.parent / ".env"
api_key = None

with open(env_file, 'r') as f:
    for line in f:
        if line.startswith('GROQ_API_KEY='):
            api_key = line.split('=', 1)[1].strip()
            break

print("=" * 70)
print("GROQ API KEY DIRECT TEST")
print("=" * 70)

if not api_key:
    print("\n✗ GROQ_API_KEY not found in .env file")
    sys.exit(1)

print(f"\n✓ API Key found: {api_key[:10]}...{api_key[-5:]}")
print(f"  Length: {len(api_key)} characters")

print("\nTesting API connection...")
print("-" * 70)

try:
    client = Groq(api_key=api_key)
    
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
    print("\n🎉 Ready to run full classification tests!")
    
except Exception as e:
    print(f"\n✗ API Connection Failed!")
    print(f"\nError: {str(e)}")
    
    if "401" in str(e):
        print("\nThe API key is invalid or expired.")
        print("Please get a new one from https://console.groq.com/keys")
    
    sys.exit(1)
