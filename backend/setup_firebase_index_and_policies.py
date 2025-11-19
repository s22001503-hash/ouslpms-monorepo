"""
Setup Firebase Composite Index and User Policies
=================================================

This script:
1. Provides instructions to create the required Firebase composite index
2. Creates user-specific policies in Firestore for existing users

Author: OUSL Print Management System
Date: November 5, 2025
"""

import firebase_admin
from firebase_admin import credentials, firestore, auth
from datetime import datetime

# Initialize Firebase
cred = credentials.Certificate('serviceAccountKey.json')
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

def print_index_instructions():
    """Print instructions for creating the Firebase composite index"""
    print("\n" + "="*70)
    print("📊 FIREBASE COMPOSITE INDEX SETUP")
    print("="*70)
    print("\n⚠️  IMPORTANT: You need to create a composite index in Firebase Console")
    print("\nThe system requires an index on the 'print_jobs' collection with:")
    print("  • Field: user_id (Ascending)")
    print("  • Field: timestamp (Ascending)")
    print("\n📋 STEPS TO CREATE INDEX:")
    print("\n1️⃣  Open this URL in your browser:")
    print("   https://console.firebase.google.com/project/oct-project-25fad/firestore/indexes")
    print("\n2️⃣  Click 'Add Index' button")
    print("\n3️⃣  Configure the index:")
    print("   Collection ID: print_jobs")
    print("   Field 1: user_id (Ascending)")
    print("   Field 2: timestamp (Ascending)")
    print("   Query scope: Collection")
    print("\n4️⃣  Click 'Create Index'")
    print("\n5️⃣  Wait for index to finish building (usually 1-2 minutes)")
    print("\n" + "="*70)
    print("\nAlternatively, click this auto-generated URL:")
    print("https://console.firebase.google.com/v1/r/project/oct-project-25fad/firestore/indexes?create_composite=ClRwcm9qZWN0cy9vY3QtcHJvamVjdC0yNWZhZC9kYXRhYmFzZXMvKGRlZmF1bHQpL2NvbGxlY3Rpb25Hcm91cHMvcHJpbnRfam9icy9pbmRleGVzL18QARoLCgd1c2VyX2lkEAEaDQoJdGltZXN0YW1wEAEaDAoIX19uYW1lX18QAQ")
    print("\n" + "="*70 + "\n")

def create_user_policies():
    """Create user-specific policies for all users"""
    print("\n" + "="*70)
    print("👥 CREATING USER-SPECIFIC POLICIES")
    print("="*70 + "\n")
    
    try:
        # Get all users from Firestore
        users_ref = db.collection('users')
        users = users_ref.stream()
        
        created_count = 0
        updated_count = 0
        
        for user_doc in users:
            user_data = user_doc.to_dict()
            user_id = user_doc.id
            role = user_data.get('role', 'user')
            epf = user_data.get('epf', 'unknown')
            
            # Define policy based on role
            if role == 'admin':
                policy_data = {
                    'user_id': user_id,
                    'epf': epf,
                    'role': role,
                    'max_copies': 100,  # High limit for admins
                    'max_daily_print_attempts': 100,  # High limit for admins
                    'allow_personal': True,  # Admins can print personal
                    'allow_confidential': True,
                    'created_at': datetime.now(),
                    'updated_at': datetime.now(),
                    'policy_type': 'user_specific'
                }
            elif role in ['dean', 'lecturer']:
                policy_data = {
                    'user_id': user_id,
                    'epf': epf,
                    'role': role,
                    'max_copies': 20,
                    'max_daily_print_attempts': 20,
                    'allow_personal': False,
                    'allow_confidential': True,
                    'created_at': datetime.now(),
                    'updated_at': datetime.now(),
                    'policy_type': 'user_specific'
                }
            else:  # Regular user
                policy_data = {
                    'user_id': user_id,
                    'epf': epf,
                    'role': role,
                    'max_copies': 5,
                    'max_daily_print_attempts': 10,
                    'allow_personal': False,
                    'allow_confidential': True,
                    'created_at': datetime.now(),
                    'updated_at': datetime.now(),
                    'policy_type': 'user_specific'
                }
            
            # Check if policy already exists
            policy_ref = db.collection('policies').document(f'user_{user_id}')
            existing_policy = policy_ref.get()
            
            if existing_policy.exists:
                # Update existing policy
                policy_ref.update({
                    **policy_data,
                    'updated_at': datetime.now()
                })
                print(f"✅ Updated policy for {epf} ({role})")
                updated_count += 1
            else:
                # Create new policy
                policy_ref.set(policy_data)
                print(f"✅ Created policy for {epf} ({role})")
                created_count += 1
        
        print(f"\n📊 Summary:")
        print(f"   Created: {created_count} policies")
        print(f"   Updated: {updated_count} policies")
        print(f"   Total:   {created_count + updated_count} policies")
        
    except Exception as e:
        print(f"❌ Error creating policies: {e}")
        raise

def verify_policies():
    """Verify that policies were created correctly"""
    print("\n" + "="*70)
    print("🔍 VERIFYING POLICIES")
    print("="*70 + "\n")
    
    try:
        policies_ref = db.collection('policies')
        policies = policies_ref.where('policy_type', '==', 'user_specific').stream()
        
        print("User-specific policies:")
        print("-" * 70)
        
        for policy_doc in policies:
            policy_data = policy_doc.to_dict()
            print(f"EPF: {policy_data.get('epf', 'N/A'):10} | "
                  f"Role: {policy_data.get('role', 'N/A'):10} | "
                  f"Daily: {policy_data.get('max_daily_print_attempts', 0):3} | "
                  f"Copies: {policy_data.get('max_copies', 0):3} | "
                  f"Personal: {policy_data.get('allow_personal', False)}")
        
        print("-" * 70)
        
    except Exception as e:
        print(f"❌ Error verifying policies: {e}")

def main():
    """Main execution"""
    print("\n" + "="*70)
    print("🚀 FIREBASE SETUP UTILITY")
    print("="*70)
    print("\nThis script will:")
    print("  1. Show instructions for creating Firebase composite index")
    print("  2. Create user-specific policies in Firestore")
    print("  3. Verify the policies were created")
    print("\n" + "="*70)
    
    input("\nPress Enter to continue...")
    
    # Step 1: Show index instructions
    print_index_instructions()
    
    print("\n⚠️  Have you created the Firebase index?")
    print("   (If not, do it now and come back)")
    response = input("\nContinue to create policies? (y/n): ")
    
    if response.lower() != 'y':
        print("\n❌ Cancelled. Run this script again after creating the index.")
        return
    
    # Step 2: Create user policies
    create_user_policies()
    
    # Step 3: Verify policies
    verify_policies()
    
    print("\n" + "="*70)
    print("✅ SETUP COMPLETE!")
    print("="*70)
    print("\nNext steps:")
    print("  1. Verify the Firebase index is built (green checkmark in console)")
    print("  2. Restart the print job watcher service")
    print("  3. Test printing with different users")
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()
