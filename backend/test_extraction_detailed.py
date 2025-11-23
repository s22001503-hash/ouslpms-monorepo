"""
Detailed test to check document extraction with text samples
"""
from ai_classifier.document_loader import DocumentLoader
from ai_classifier.config import OFFICIAL_DIR, PERSONAL_DIR
from pathlib import Path

def test_extraction_detailed():
    print("="*80)
    print("DETAILED DOCUMENT EXTRACTION TEST")
    print("="*80)
    
    directories = [
        (OFFICIAL_DIR, "OFFICIAL"),
        (PERSONAL_DIR, "PERSONAL")
    ]
    
    for directory, label in directories:
        print(f"\n{'='*80}")
        print(f"{label} DOCUMENTS")
        print('='*80)
        
        if not directory.exists():
            print(f"❌ Directory not found: {directory}")
            continue
        
        # Get all files
        extensions = ('.pdf', '.docx', '.txt')
        files = sorted([f for f in directory.rglob('*') if f.is_file() and f.suffix.lower() in extensions])
        
        success_files = []
        failed_files = []
        
        for file_path in files:
            text = DocumentLoader.load_document(str(file_path))
            
            if text and len(text) > 50:
                success_files.append((file_path, len(text), text))
            else:
                failed_files.append(file_path)
        
        # Print successful extractions
        print(f"\n✅ SUCCESSFUL EXTRACTIONS ({len(success_files)} files):")
        print("-" * 80)
        for file_path, length, text in success_files:
            # Show relative path from training_documents
            rel_path = file_path.relative_to(directory.parent.parent)
            print(f"\n📄 {rel_path}")
            print(f"   Length: {length:,} characters")
            # Show first 150 characters
            preview = text[:150].replace('\n', ' ')
            print(f"   Preview: {preview}...")
        
        # Print failed extractions
        if failed_files:
            print(f"\n\n❌ FAILED EXTRACTIONS ({len(failed_files)} files):")
            print("-" * 80)
            for file_path in failed_files:
                rel_path = file_path.relative_to(directory.parent.parent)
                print(f"   {rel_path}")
        
        # Summary
        print(f"\n{'='*80}")
        print(f"SUMMARY for {label}:")
        print(f"  ✅ Success: {len(success_files)} files")
        print(f"  ❌ Failed:  {len(failed_files)} files")
        print(f"  📊 Success Rate: {len(success_files)/(len(success_files)+len(failed_files))*100:.1f}%")

if __name__ == "__main__":
    test_extraction_detailed()
