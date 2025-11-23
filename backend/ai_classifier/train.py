"""
Train the AI classifier by ingesting training documents
Run this script to populate ChromaDB with training data
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from ai_classifier.document_loader import DocumentLoader
from ai_classifier.chroma_manager import ChromaDBManager
from ai_classifier.config import OFFICIAL_DIR, PERSONAL_DIR

def train_classifier():
    """
    Load training documents and add to ChromaDB
    """
    print("\n" + "="*60)
    print("TRAINING AI DOCUMENT CLASSIFIER")
    print("="*60 + "\n")
    
    # Initialize ChromaDB
    chroma = ChromaDBManager()
    
    # Ask if user wants to reset collection
    stats = chroma.get_collection_stats()
    if stats['total_chunks'] > 0:
        print(f"Current collection has {stats['total_chunks']} chunks:")
        print(f"Label distribution: {stats['label_distribution']}")
        
        reset = input("\nReset collection and retrain from scratch? (y/n): ").lower()
        if reset == 'y':
            chroma.reset_collection()
            print("Collection reset.\n")
    
    # Load OFFICIAL documents
    print("Loading OFFICIAL documents...")
    official_docs = DocumentLoader.load_directory(str(OFFICIAL_DIR), label="OFFICIAL")
    print(f"Loaded {len(official_docs)} OFFICIAL documents\n")
    
    # Load PERSONAL documents
    print("Loading PERSONAL documents...")
    personal_docs = DocumentLoader.load_directory(str(PERSONAL_DIR), label="PERSONAL")
    print(f"Loaded {len(personal_docs)} PERSONAL documents\n")
    
    # Check if we have documents
    total_docs = len(official_docs) + len(personal_docs)
    if total_docs == 0:
        print("⚠️  WARNING: No training documents found!")
        print(f"\nPlease add documents to:")
        print(f"  - OFFICIAL: {OFFICIAL_DIR}")
        print(f"  - PERSONAL: {PERSONAL_DIR}")
        print(f"\nSupported formats: PDF, DOCX, TXT")
        return
    
    # Add to ChromaDB
    print("Adding documents to ChromaDB...")
    all_docs = official_docs + personal_docs
    chroma.add_documents_batch(all_docs)
    
    # Show final statistics
    final_stats = chroma.get_collection_stats()
    print("\n" + "="*60)
    print("TRAINING COMPLETE")
    print("="*60)
    print(f"Total chunks in collection: {final_stats['total_chunks']}")
    print(f"Label distribution: {final_stats['label_distribution']}")
    print("\nYou can now use the classifier to classify new documents!")
    print("="*60 + "\n")

if __name__ == "__main__":
    train_classifier()
