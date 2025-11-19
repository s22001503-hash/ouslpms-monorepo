"""
🔧 Initialize Firestore System Policies
========================================

This script creates the initial system_policies document in Firestore
with default admin-configurable limits for Sprint 5.

Run this once to set up the policy structure.

Usage:
    python scripts/init_firestore_policies.py
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

def initialize_firestore():
    """Initialize Firebase Admin SDK."""
    if not firebase_admin._apps:
        try:
            # Try to use service account key
            cred_path = Path(__file__).parent.parent / 'serviceAccountKey.json'
            if cred_path.exists():
                cred = credentials.Certificate(str(cred_path))
                firebase_admin.initialize_app(cred)
                print("✅ Firebase initialized with service account key")
            else:
                print("❌ Error: serviceAccountKey.json not found")
                print("Please download it from Firebase Console and place it in backend/ folder")
                sys.exit(1)
        except Exception as e:
            print(f"❌ Firebase initialization failed: {e}")
            sys.exit(1)
    
    return firestore.client()

def create_system_policies(db):
    """Create default system policies in Firestore."""
    
    system_policies = {
        # Print Limits
        'max_daily_prints': 3,              # Default: 3 prints per day per user
        'max_copies_per_document': 10,      # Default: 10 copies max per document
        
        # Document Classification Rules
        'personal_documents_allowed': False,  # Personal docs are blocked
        'official_documents_allowed': True,   # Official docs follow limits
        'confidential_documents_allowed': True, # Confidential docs follow limits
        
        # Admin Configuration
        'updated_at': firestore.SERVER_TIMESTAMP,
        'updated_by': 'system',
        'created_at': firestore.SERVER_TIMESTAMP,
        'version': '1.0',
        
        # Metadata
        'description': 'Default system-wide print policies (admin-configurable)',
        'notes': 'These limits can be changed by admins via Firebase Console or Admin Panel'
    }
    
    # Create or update the default policies document
    policies_ref = db.collection('system_policies').document('default')
    policies_ref.set(system_policies, merge=True)
    
    print("✅ System policies created successfully!")
    print("\n📋 Default Policies:")
    print(f"   • Max daily prints: {system_policies['max_daily_prints']}")
    print(f"   • Max copies per document: {system_policies['max_copies_per_document']}")
    print(f"   • Personal documents: {'Allowed' if system_policies['personal_documents_allowed'] else 'Blocked'}")
    print(f"   • Official documents: {'Allowed' if system_policies['official_documents_allowed'] else 'Blocked'}")
    print(f"   • Confidential documents: {'Allowed' if system_policies['confidential_documents_allowed'] else 'Blocked'}")

def create_sample_user_limit(db):
    """Create a sample user daily limit document (for testing)."""
    
    # Example: User 99999 has printed 1 document today
    today = datetime.now().strftime('%Y-%m-%d')
    user_id = '99999'
    
    user_limit_data = {
        'user_id': user_id,
        'date': today,
        'prints_today': 1,
        'max_daily_prints': 3,  # Copied from system_policies
        'prints': [
            {
                'timestamp': datetime.now().isoformat(),
                'file_hash': 'abc123...example',
                'file_name': 'Sample_Report.pdf',
                'classification': 'office',
                'copies': 1
            }
        ],
        'updated_at': firestore.SERVER_TIMESTAMP
    }
    
    # Create user limit document
    user_limit_ref = db.collection('user_daily_limits').document(f'{user_id}_{today}')
    user_limit_ref.set(user_limit_data, merge=True)
    
    print(f"\n✅ Sample user limit created for user {user_id}")
    print(f"   • Prints today: {user_limit_data['prints_today']}/{user_limit_data['max_daily_prints']}")

def main():
    """Main initialization function."""
    print("🚀 Initializing Firestore System Policies for Sprint 5...")
    print("=" * 60)
    
    # Initialize Firestore
    db = initialize_firestore()
    
    # Create system policies
    create_system_policies(db)
    
    # Create sample user limit (optional - for testing)
    create_sample = input("\n❓ Create sample user limit for testing? (y/n): ").strip().lower()
    if create_sample == 'y':
        create_sample_user_limit(db)
    
    print("\n" + "=" * 60)
    print("✅ Firestore initialization complete!")
    print("\n📝 Next Steps:")
    print("   1. Restart the backend server")
    print("   2. Test printing with the new Firestore-driven policies")
    print("   3. Admins can modify policies in Firebase Console:")
    print("      → Firestore Database → system_policies → default")

if __name__ == '__main__':
    main()
