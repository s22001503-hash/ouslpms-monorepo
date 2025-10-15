# EPF Login Setup Guide

## How EPF Login Works

EPF login maps Employee Provident Fund (EPF) numbers to email addresses in Firestore, allowing users to log in with their EPF number instead of remembering their email.

### Architecture

```
User enters EPF + Password
        ↓
Frontend queries Firestore: epf_mapping/{epf}
        ↓
Gets email address
        ↓
Firebase Authentication (signInWithEmailAndPassword)
        ↓
Success! User logged in
```

## Firestore Collections

### 1. `epf_mapping` Collection
Maps EPF numbers to email addresses.

**Document ID**: EPF number (e.g., `"12345"`)

**Fields**:
```json
{
  "email": "user@ou.ac.lk",
  "uid": "firebase_user_uid"
}
```

### 2. `users` Collection
Stores user roles for authorization.

**Document ID**: Firebase UID

**Fields**:
```json
{
  "role": "admin" // or "user"
}
```

## Setup Steps

### Option A: Use the Seed Script (Fastest)

1. **Run the seeding script** (creates test users automatically):
   ```powershell
   cd backend
   .venv\Scripts\python.exe scripts\seed_epf_users.py
   ```

2. **Test credentials created**:
   - **Admin**: EPF `12345` / Password `admin123` / Email `admin@ou.ac.lk`
   - **User**: EPF `67890` / Password `user123` / Email `user@ou.ac.lk`
   - **User**: EPF `11111` / Password `john123` / Email `john.doe@ou.ac.lk`

### Option B: Manual Setup in Firebase Console

#### Step 1: Create Users in Firebase Authentication
1. Go to Firebase Console → Authentication → Users
2. Click "Add user"
3. Enter:
   - Email: `admin@ou.ac.lk`
   - Password: `admin123`
4. Copy the User UID

#### Step 2: Create EPF Mapping in Firestore
1. Go to Firebase Console → Firestore Database
2. Create collection: `epf_mapping`
3. Add document with ID: `12345`
4. Add fields:
   ```
   email: admin@ou.ac.lk
   uid: <paste the User UID from step 1>
   ```

#### Step 3: Set User Role
1. In Firestore, create collection: `users`
2. Add document with ID: `<the User UID>`
3. Add field:
   ```
   role: admin
   ```

## Testing EPF Login

1. **Start the frontend**:
   ```powershell
   cd frontend
   npm run dev
   ```

2. **Open** http://localhost:5174

3. **Login with EPF**:
   - Make sure "EPF Login" tab is selected (not Email Login)
   - Enter EPF: `12345`
   - Enter Password: `admin123`
   - Click "Sign In"

4. **Expected behavior**:
   - Frontend queries Firestore for EPF `12345`
   - Gets email `admin@ou.ac.lk`
   - Signs in with that email + password
   - Redirects to `/admin` dashboard (because role is `admin`)

## Adding More Users

### Using the Script
Edit `backend/scripts/seed_epf_users.py` and add to the `TEST_USERS` list:

```python
{
    "epf": "99999",
    "email": "newuser@ou.ac.lk",
    "password": "password123",
    "display_name": "New User",
    "role": "user"
}
```

Then run the script again.

### Programmatically (Python)
```python
from firebase_admin import auth, firestore

# Create user in Auth
user = auth.create_user(
    email='newuser@ou.ac.lk',
    password='password123',
    display_name='New User'
)

db = firestore.client()

# Create EPF mapping
db.collection('epf_mapping').document('99999').set({
    'email': 'newuser@ou.ac.lk',
    'uid': user.uid
})

# Set role
db.collection('users').document(user.uid).set({
    'role': 'user'
})
```

## Security Considerations

1. **EPF numbers are not secret** - They identify the user but shouldn't be used as authentication alone
2. **Password is still required** - EPF just maps to email for convenience
3. **Firestore Security Rules** - Add rules to protect the `epf_mapping` collection:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Only authenticated users can read their own EPF mapping
    match /epf_mapping/{epf} {
      allow read: if request.auth != null;
      allow write: if false; // Only admins via backend
    }
    
    // Users can read their own role
    match /users/{userId} {
      allow read: if request.auth != null && request.auth.uid == userId;
      allow write: if false; // Only backend can write
    }
  }
}
```

## Troubleshooting

### Error: "EPF number not found"
- The EPF mapping doesn't exist in Firestore
- Run the seed script or manually create the mapping

### Error: "Permission denied"
- Firestore security rules are blocking access
- Temporarily set rules to allow read (for testing only)
- Or set proper rules as shown above

### Login works but redirects to wrong page
- Check the role in Firestore `users/{uid}` collection
- Role should be `"admin"` or `"user"` (lowercase)

## Production Recommendations

1. **Import EPF data from HR system** - Create a script to bulk import from CSV/database
2. **Admin UI for user management** - Build an admin page to add/edit EPF mappings
3. **Secure the backend** - Only allow backend to write EPF mappings
4. **Add audit logging** - Track EPF mapping changes
5. **Password reset flow** - Allow users to reset password with EPF number
