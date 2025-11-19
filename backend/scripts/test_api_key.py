"""Quick test to verify Pinecone API key"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("PINECONE_API_KEY")

print("=" * 70)
print("PINECONE API KEY TEST")
print("=" * 70)

if api_key:
    print(f"\n✓ API key found: {api_key[:10]}...{api_key[-4:]}")
    print(f"  Length: {len(api_key)} characters")
    
    # Test connection
    print("\nTesting connection to Pinecone...")
    try:
        from pinecone import Pinecone
        pc = Pinecone(api_key=api_key)
        
        print("✓ Successfully connected to Pinecone!")
        
        # List indexes
        indexes = pc.list_indexes()
        print(f"\nExisting indexes: {len(indexes)}")
        for idx in indexes:
            print(f"  - {idx.name}")
        
        if len(indexes) == 0:
            print("  (No indexes yet - will create one)")
        
    except Exception as e:
        print(f"✗ Connection failed: {str(e)}")
else:
    print("\n✗ API key not found in environment")

print("=" * 70)
