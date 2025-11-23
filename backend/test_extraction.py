"""
Quick test to check which documents can be extracted
"""
from ai_classifier.document_loader import DocumentLoader
from ai_classifier.config import OFFICIAL_DIR, PERSONAL_DIR
from pathlib import Path

def test_extraction():
    print("Testing document extraction...\n")
    
    directories = [
        (OFFICIAL_DIR, "OFFICIAL"),
        (PERSONAL_DIR, "PERSONAL")
    ]
    
    for directory, label in directories:
        print(f"\n{'='*60}")
        print(f"Testing {label} documents from: {directory}")
        print('='*60)
        
        if not directory.exists():
            print(f"Directory not found!")
            continue
        
        # Get all files
        extensions = ('.pdf', '.docx', '.txt')
        files = [f for f in directory.rglob('*') if f.is_file() and f.suffix.lower() in extensions]
        
        success_count = 0
        fail_count = 0
        
        for file_path in files:
            text = DocumentLoader.load_document(str(file_path))
            
            if text and len(text) > 50:  # At least 50 characters
                success_count += 1
                status = "✅ OK"
                length = len(text)
            else:
                fail_count += 1
                status = "❌ FAILED"
                length = 0
            
            print(f"{status} | {length:>6} chars | {file_path.name}")
        
        print(f"\nSummary: {success_count} succeeded, {fail_count} failed")

if __name__ == "__main__":
    test_extraction()
