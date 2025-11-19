"""
Update Firebase users with EPF numbers for login
"""

import firebase_admin
from firebase_admin import credentials, auth, firestore
from datetime import datetime

# Initialize Firebase Admin
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate('serviceAccountKey.json')
    firebase_admin.initialize_app(cred)

db = firestore.client()

def update_users_with_epf():
    """Update existing users with EPF numbers"""
    
    # Get all users from Firestore
    users_ref = db.collection('users')
    users = users_ref.stream()
    
    print("\n🔧 Updating users with EPF numbers...\n")
    print("=" * 70)
    
    # EPF mapping based on existing employee IDs
    epf_mapping = {
        'ADMIN001': 'EPF001',
        'DEAN001': 'EPF002', 
        'USER001': 'EPF003',
        'LECT001': 'EPF004'
    }
    
    for user in users:
        user_data = user.to_dict()
        employee_id = user_data.get('employeeId')
        
        if employee_id in epf_mapping:
            epf = epf_mapping[employee_id]
            
            # Update Firestore document
            users_ref.document(user.id).update({
                'epf': epf,
                'updatedAt': firestore.SERVER_TIMESTAMP
            })
            
            print(f"\n✅ Updated {user_data.get('displayName')}")
            print(f"   Email: {user_data.get('email')}")
            print(f"   EPF: {epf}")
            print(f"   Password: (same as before)")
    
    print("\n" + "=" * 70)
    print("\n✅ All users updated with EPF numbers!\n")

def display_epf_credentials():
    """Display all EPF-based credentials"""
    
    print("\n📋 EPF LOGIN CREDENTIALS:")
    print("━" * 70)
    
    credentials_list = [
        {
            'name': 'System Administrator',
            'epf': 'EPF001',
            'email': 'admin@ousl.lk',
            'password': 'Admin@123',
            'role': 'admin'
        },
        {
            'name': 'Dean of Faculty',
            'epf': 'EPF002',
            'email': 'dean@ousl.lk',
            'password': 'Dean@123',
            'role': 'dean'
        },
        {
            'name': 'Test User',
            'epf': 'EPF003',
            'email': 'user@ousl.lk',
            'password': 'User@123',
            'role': 'user'
        },
        {
            'name': 'Test Lecturer',
            'epf': 'EPF004',
            'email': 'lecturer@ousl.lk',
            'password': 'Lecturer@123',
            'role': 'lecturer'
        }
    ]
    
    for cred in credentials_list:
        print(f"\n{cred['name']} ({cred['role'].upper()})")
        print(f"  EPF:      {cred['epf']}")
        print(f"  Password: {cred['password']}")
        print(f"  Email:    {cred['email']} (for reference)")
    
    print("\n" + "━" * 70)
    print("\n🎯 USE EPF AND PASSWORD TO LOGIN")
    print("   Example: EPF003 / User@123\n")

if __name__ == '__main__':
    update_users_with_epf()
    display_epf_credentials()
