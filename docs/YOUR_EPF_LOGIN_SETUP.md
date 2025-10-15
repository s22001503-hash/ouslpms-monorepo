# EPF Login Setup - Your Current Configuration

## Your Firestore Structure

```
users (collection)
  └─ 12345 (document ID = EPF number)
      ├─ role: "user" (string)
      └─ email: "user@ou.ac.lk" (string) ← Add this field if not present
```

## How It Works Now

1. **User enters EPF number** (e.g., `12345`) and password
2. **Frontend queries** Firestore: `users/12345`
3. **Gets email** from the document (or constructs `12345@ou.ac.lk` if no email field)
4. **Signs in** using Firebase Auth with that email + password
5. **Stores EPF** in sessionStorage for role lookup
6. **Gets role** from the same `users/12345` document

## Setup Steps for Your Database

### Step 1: Make sure your Firestore document has an email field

In Firebase Console → Firestore → `users` collection → document `12345`:

```
Document ID: 12345
Fields:
  - role: "user"
  - email: "user@ou.ac.lk"  ← Add this if missing
```

### Step 2: Create a user in Firebase Authentication

1. Go to Firebase Console → Authentication → Users
2. Click "Add user"
3. Enter the **same email** as in Firestore: `user@ou.ac.lk`
4. Set password: `yourpassword123`

### Step 3: Test EPF Login

1. Open your app: http://localhost:5174
2. Make sure "EPF Login" is selected (not Email Login)
3. Enter EPF: `12345`
4. Enter Password: `yourpassword123`
5. Click "Sign In"

## Example: Adding More Users

### In Firestore (`users` collection):

```
Document ID: 67890
Fields:
  - role: "admin"
  - email: "admin@ou.ac.lk"
```

### In Firebase Authentication:

```
Email: admin@ou.ac.lk
Password: admin123
```

Now user can login with:
- EPF: `67890`
- Password: `admin123`

## Quick Setup Script

If you want to add users programmatically, here's a Python script:

```python
from firebase_admin import auth, firestore

# Initialize Firebase Admin (do this once)
# ... your initialization code ...

db = firestore.client()

# Function to add a user
def add_user(epf, email, password, role):
    # 1. Create user in Firebase Auth
    user = auth.create_user(
        email=email,
        password=password
    )
    print(f"Created auth user: {email} (UID: {user.uid})")
    
    # 2. Create Firestore document with EPF as ID
    db.collection('users').document(epf).set({
        'email': email,
        'role': role,
        'uid': user.uid  # Optional: store UID for reference
    })
    print(f"Created Firestore doc: users/{epf}")

# Add users
add_user('12345', 'user@ou.ac.lk', 'user123', 'user')
add_user('67890', 'admin@ou.ac.lk', 'admin123', 'admin')
```

## Troubleshooting

### Error: "EPF number not found"
**Solution:** Make sure the document exists in Firestore `users` collection with the EPF as document ID.

```
users/12345  ← Document must exist
```

### Error: "Wrong password" or "User not found"
**Solution:** 
1. Check that the email in Firestore matches the email in Firebase Authentication
2. Make sure you created the user in Firebase Authentication (not just Firestore)

### Login works but wrong role
**Solution:** Check the `role` field in Firestore `users/{epf}` document. It should be lowercase: `"user"` or `"admin"`

### Role doesn't load after login
**Solution:** 
1. Check browser console for errors
2. Make sure sessionStorage is enabled
3. Check Firestore security rules (should allow authenticated users to read their own doc)

## Firestore Security Rules

Add these rules to protect your data:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users can read their own document if they know the EPF
    match /users/{epf} {
      allow read: if request.auth != null;
      allow write: if false; // Only admin/backend can write
    }
  }
}
```

## What Changed in the Code

I updated `useAuth.jsx` to:
1. ✅ Query Firestore `users/{epf}` instead of `epf_mapping/{epf}`
2. ✅ Get email from the document or construct it from EPF
3. ✅ Store EPF in sessionStorage for role lookup after auth
4. ✅ Look up role using the stored EPF (not UID)

## Testing Checklist

- [ ] EPF document exists in Firestore `users` collection
- [ ] Document has `role` and `email` fields
- [ ] User exists in Firebase Authentication with matching email
- [ ] Login with EPF works
- [ ] Role is correctly loaded and user redirects to the right dashboard
- [ ] Logout works
- [ ] Can login again after logout

## Next Steps

1. **Add more users** to your Firestore `users` collection
2. **Test login** with different EPF numbers
3. **Add proper Firestore security rules** (see above)
4. **Consider adding** a `uid` field to each user document for easier reverse lookup
