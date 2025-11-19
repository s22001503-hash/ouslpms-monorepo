"""
Initialize Firestore Collections for Policy Proposal System
Run this script once to set up the necessary collections and initial data
"""

import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os

def initialize_policy_collections():
    """Initialize Firestore collections for policy management"""
    
    # Initialize Firebase Admin (if not already initialized)
    try:
        firebase_admin.get_app()
    except ValueError:
        # Get the directory of this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        cred_path = os.path.join(script_dir, 'serviceAccountKey.json')
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    
    db = firestore.client()
    
    print("🚀 Initializing Policy Proposal System Collections...")
    
    # 1. Initialize Global Policies
    print("\n📋 Setting up global_policies collection...")
    global_policies_ref = db.collection('global_policies').document('current')
    global_policies_ref.set({
        'maxAttemptsPerDay': 5,
        'maxCopiesPerDoc': 5,
        'lastUpdated': datetime.utcnow().isoformat() + 'Z',
        'updatedBy': 'System Initialization'
    })
    print("✅ Global policies initialized with default values:")
    print("   - Max Attempts per Day: 5")
    print("   - Max Copies per Document: 5")
    
    # 2. Create sample policy proposals (optional - for testing)
    print("\n📝 Creating sample policy proposals...")
    
    # Sample Global Proposal
    sample_global = {
        'type': 'global',
        'adminEPF': '50001',
        'adminName': 'Sample Admin',
        'justification': 'Sample proposal for testing - increasing limits for exam season',
        'status': 'pending',
        'submittedAt': datetime.utcnow().isoformat() + 'Z',
        'changes': {
            'maxAttemptsPerDay': {
                'current': 5,
                'proposed': 7
            }
        },
        'vcDecision': None
    }
    
    db.collection('policy_proposals').add(sample_global)
    print("✅ Sample global policy proposal created")
    
    # Sample Special User Proposal
    sample_special = {
        'type': 'special_user',
        'adminEPF': '50001',
        'adminName': 'Sample Admin',
        'targetEPF': '60025',
        'targetName': 'Sample User',
        'targetDept': 'Computer Science',
        'justification': 'Sample special policy for testing - research assistant needs higher limits',
        'status': 'pending',
        'submittedAt': datetime.utcnow().isoformat() + 'Z',
        'proposedPolicy': {
            'maxAttemptsPerDay': 15,
            'maxCopiesPerDoc': 20
        },
        'vcDecision': None
    }
    
    db.collection('policy_proposals').add(sample_special)
    print("✅ Sample special user policy proposal created")
    
    # 3. Create indexes (note: these should be created via Firebase Console)
    print("\n⚠️  IMPORTANT: Create the following indexes in Firebase Console:")
    print("   Collection: policy_proposals")
    print("   - Index: type (ASC), status (ASC), submittedAt (DESC)")
    print("   - Index: status (ASC), submittedAt (DESC)")
    print("   Go to: https://console.firebase.google.com/project/_/firestore/indexes")
    
    print("\n✨ Initialization Complete!")
    print("\nNext steps:")
    print("1. Deploy Firestore security rules (see POLICY_BACKEND_SETUP.md)")
    print("2. Create composite indexes as shown above")
    print("3. Test the API endpoints")
    print("4. Update frontend API_BASE URL if needed")


def verify_collections():
    """Verify that collections were created successfully"""
    
    try:
        firebase_admin.get_app()
    except ValueError:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        cred_path = os.path.join(script_dir, 'serviceAccountKey.json')
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    
    db = firestore.client()
    
    print("\n🔍 Verifying collections...")
    
    # Check global_policies
    global_doc = db.collection('global_policies').document('current').get()
    if global_doc.exists:
        print("✅ global_policies collection exists")
        print(f"   Current values: {global_doc.to_dict()}")
    else:
        print("❌ global_policies collection not found")
    
    # Check policy_proposals
    proposals = list(db.collection('policy_proposals').limit(5).stream())
    print(f"✅ policy_proposals collection has {len(proposals)} documents")
    
    # Check user_special_policies
    special = list(db.collection('user_special_policies').limit(5).stream())
    print(f"✅ user_special_policies collection has {len(special)} documents")
    
    print("\n✨ Verification complete!")


def clear_sample_data():
    """Remove sample/test data (use with caution!)"""
    
    try:
        firebase_admin.get_app()
    except ValueError:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        cred_path = os.path.join(script_dir, 'serviceAccountKey.json')
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    
    db = firestore.client()
    
    print("⚠️  Clearing sample policy proposals...")
    
    # Delete sample proposals
    proposals = db.collection('policy_proposals').where('adminName', '==', 'Sample Admin').stream()
    count = 0
    for doc in proposals:
        doc.reference.delete()
        count += 1
    
    print(f"✅ Deleted {count} sample proposals")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'init':
            initialize_policy_collections()
        elif command == 'verify':
            verify_collections()
        elif command == 'clear':
            response = input("⚠️  This will delete all sample data. Continue? (yes/no): ")
            if response.lower() == 'yes':
                clear_sample_data()
            else:
                print("Cancelled.")
        else:
            print("Unknown command. Use: init, verify, or clear")
    else:
        print("Policy Proposal System Initialization")
        print("\nUsage:")
        print("  python init_policy_collections.py init    - Initialize collections")
        print("  python init_policy_collections.py verify  - Verify collections")
        print("  python init_policy_collections.py clear   - Clear sample data")
        print("\nExample:")
        print("  python init_policy_collections.py init")
