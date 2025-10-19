"""
Initialize Firestore collections for the Admin Dashboard upgrade.
This script creates the necessary collections and documents with default data.

Run this script once to set up:
- system_settings collection with default configuration
- Test data for settings_requests (optional)
"""

import os
import sys
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

def format_timestamp(dt: datetime) -> str:
    """Format datetime to ISO string."""
    return dt.isoformat() + 'Z'

def init_firestore():
    """Initialize Firestore with default collections and data."""
    
    # Initialize Firebase Admin if not already initialized
    if not firebase_admin._apps:
        # Update this path to your service account key
        cred_path = r'C:\Users\user\Desktop\OUspms\backend\firebase-adminsdk.json'
        
        if not os.path.exists(cred_path):
            print(f"❌ Error: Service account key not found at {cred_path}")
            print("Please update the cred_path variable in this script.")
            sys.exit(1)
        
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        print("✅ Firebase Admin initialized")
    
    db = firestore.client()
    
    # ==================== Create system_settings collection ====================
    print("\n📝 Creating system_settings collection...")
    
    settings_ref = db.collection('system_settings').document('current')
    settings_doc = settings_ref.get()
    
    if settings_doc.exists:
        print("⚠️  system_settings/current already exists. Skipping...")
        print(f"   Current settings: {settings_doc.to_dict()}")
    else:
        default_settings = {
            'maxCopiesPerDocument': 10,
            'maxPrintAttemptsPerDay': 50,
            'maxPagesPerJob': 100,
            'dailyQuota': 500,
            'allowColorPrinting': True,
            'lastModified': format_timestamp(datetime.now()),
            'modifiedBy': 'system',
            'modifiedByName': 'System Initialization'
        }
        settings_ref.set(default_settings)
        print("✅ system_settings/current created with default values:")
        print(f"   - Max Copies per Document: {default_settings['maxCopiesPerDocument']}")
        print(f"   - Max Print Attempts per Day: {default_settings['maxPrintAttemptsPerDay']}")
        print(f"   - Max Pages per Job: {default_settings['maxPagesPerJob']}")
        print(f"   - Daily Quota: {default_settings['dailyQuota']} pages")
        print(f"   - Color Printing: {'Enabled' if default_settings['allowColorPrinting'] else 'Disabled'}")
    
    # ==================== Create settings_requests collection (empty) ====================
    print("\n📝 Checking settings_requests collection...")
    
    # Check if collection exists by trying to query it
    try:
        requests_ref = db.collection('settings_requests')
        existing_requests = list(requests_ref.limit(1).stream())
        
        if existing_requests:
            count = len(list(requests_ref.stream()))
            print(f"⚠️  settings_requests collection already exists with {count} document(s)")
        else:
            print("✅ settings_requests collection exists but is empty (ready for proposals)")
    except Exception as e:
        print(f"⚠️  settings_requests collection may not exist yet (will be created on first proposal)")
    
    # ==================== Optional: Create sample proposal for testing ====================
    create_sample = input("\n❓ Do you want to create a sample pending proposal for testing? (y/n): ").lower().strip()
    
    if create_sample == 'y':
        sample_proposal = {
            'adminId': '50005',
            'adminEmail': '50005@ousl.edu.lk',
            'adminName': 'Admin User',
            'proposedSettings': {
                'maxCopiesPerDocument': 15,
                'maxPrintAttemptsPerDay': 60,
                'maxPagesPerJob': 120,
                'dailyQuota': 600,
                'allowColorPrinting': False
            },
            'status': 'pending',
            'submittedAt': format_timestamp(datetime.now()),
            'reviewedAt': None,
            'reviewedBy': None,
            'reviewedByName': None,
            'deanNotes': None
        }
        
        doc_ref = db.collection('settings_requests').add(sample_proposal)
        print(f"✅ Sample proposal created with ID: {doc_ref[1].id}")
        print("   Status: pending")
        print("   Proposed changes: max copies=15, max attempts=60, max pages=120, daily quota=600, color=disabled")
    
    print("\n" + "="*60)
    print("✅ Firestore initialization complete!")
    print("="*60)
    print("\nYou can now:")
    print("1. Start your backend server: python -m uvicorn app.main:app --reload")
    print("2. Login to admin dashboard at http://localhost:5173")
    print("3. View Overview tab to see stats")
    print("4. Submit settings proposals via Settings Proposal tab")
    print("\n")

if __name__ == '__main__':
    try:
        init_firestore()
    except KeyboardInterrupt:
        print("\n\n⚠️  Initialization cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error during initialization: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
