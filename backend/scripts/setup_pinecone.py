"""
Setup Pinecone Index
Creates the vector database index for document storage
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

from app.services.pinecone_service import PineconeService, PineconeConfig


def main():
    print("=" * 70)
    print("PINECONE INDEX SETUP")
    print("=" * 70)
    
    # Check for API key
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        print("\n❌ ERROR: PINECONE_API_KEY not found in environment")
        print("\nSteps to get your API key:")
        print("  1. Go to: https://app.pinecone.io/")
        print("  2. Sign up or log in")
        print("  3. Go to 'API Keys' section")
        print("  4. Copy your API key")
        print("\nThen add to backend/.env file:")
        print("  PINECONE_API_KEY=your_api_key_here")
        print("  PINECONE_INDEX_NAME=ousl-documents")
        return
    
    print(f"\n✓ API key found: {api_key[:10]}...{api_key[-4:]}")
    
    # Initialize service
    print("\n[1/3] Initializing Pinecone service...")
    service = PineconeService()
    
    print(f"  Index name: {service.config.index_name}")
    print(f"  Dimension: {service.config.dimension}")
    print(f"  Metric: {service.config.metric}")
    print(f"  Cloud: {service.config.cloud}")
    print(f"  Region: {service.config.region}")
    
    # Create index
    print("\n[2/3] Creating Pinecone index...")
    print("  (This may take 1-2 minutes for first-time setup)")
    
    success = service.create_index(delete_if_exists=False)
    
    if success:
        print("  ✓ Index created/verified successfully")
    else:
        print("  ❌ Failed to create index")
        return
    
    # Get stats
    print("\n[3/3] Verifying index...")
    stats = service.get_index_stats()
    
    print(f"  Total vectors: {stats.get('total_vector_count', 0)}")
    print(f"  Dimension: {stats.get('dimension', 'N/A')}")
    print(f"  Index fullness: {stats.get('index_fullness', 0):.2%}")
    
    # Summary
    print("\n" + "=" * 70)
    print("SETUP COMPLETE!")
    print("=" * 70)
    print("\nYour Pinecone index is ready for:")
    print("  ✓ Storing document embeddings")
    print("  ✓ Similarity search")
    print("  ✓ Training data uploads")
    print("\nNext steps:")
    print("  1. Upload training documents")
    print("  2. Test similarity search")
    print("  3. Integrate with classification system")
    print("=" * 70)


if __name__ == "__main__":
    main()
