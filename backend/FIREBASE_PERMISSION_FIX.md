# Firebase Permission Fix Guide

## Problem
"Missing or insufficient permissions" error when logging in

## Solution Completed ✅

### 1. Created Test Users
We've created 4 test users in Firebase:

| Role | Email | Password | Department |
|------|-------|----------|------------|
| Admin | admin@ousl.lk | Admin@123 | IT |
| Dean | dean@ousl.lk | Dean@123 | Engineering |
| User | user@ousl.lk | User@123 | Engineering |
| Lecturer | lecturer@ousl.lk | Lecturer@123 | Computing |

### 2. Created Default Policies
- System default policy (fallback)
- Admin role policy (no restrictions)
- User role policy (standard limits)

### 3. Created Firestore Security Rules
File: `firestore.rules`

## If You Still Get Permission Errors

### Option 1: Deploy Security Rules (Recommended)

1. Open Firebase Console:
   https://console.firebase.google.com/project/oct-project-25fad/firestore/rules

2. Copy content from `firestore.rules` file

3. Paste into Firebase Console

4. Click "Publish"

### Option 2: Temporary Open Rules (Testing Only)

⚠️ **WARNING: Not for production!**

Go to Firebase Console and use these rules temporarily:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if true;
    }
  }
}
```

Then after testing, replace with the secure rules from `firestore.rules`.

## Verify Users Were Created

1. Go to Firebase Console: https://console.firebase.google.com/project/oct-project-25fad

2. Navigate to:
   - **Authentication** → Users (should see 4 users)
   - **Firestore Database** → users collection (should see 4 documents)
   - **Firestore Database** → policies collection (should see 3 policies)

## Test Login

1. Open: http://localhost:3000

2. Try logging in with:
   - Email: `user@ousl.lk`
   - Password: `User@123`

3. If successful, you should see the dashboard!

## Troubleshooting

### Error: "User not found"
- Run: `python setup_firebase_users.py` again

### Error: "Permission denied"
- Deploy Firestore rules from Firebase Console
- OR use temporary open rules for testing

### Error: "Invalid credentials"
- Double-check email and password (case-sensitive)
- Password requirements: At least 6 characters

## Re-run Setup (if needed)

```powershell
cd "C:\Users\user\Desktop\OCT Project\ouslpms-monorepo\backend"
python setup_firebase_users.py
```

This will:
- Create missing users
- Update existing users (merge)
- Create default policies

## Print Test Flow

Once logged in:

1. **As user@ousl.lk** (Regular User):
   - Can print "official" documents (max 3 copies, 30 pages, 50/day)
   - Cannot print "personal" documents (blocked)
   - Cannot print "confidential" documents (requires approval)

2. **As admin@ousl.lk** (Administrator):
   - Can print any document type
   - No restrictions (999 copies, pages, daily limit)

3. **As dean@ousl.lk** (Dean):
   - Similar to admin but for faculty management
   - Can create/modify policies

4. **As lecturer@ousl.lk** (Lecturer):
   - Standard user permissions
   - Department-specific access

## Next Steps

1. ✅ Users created
2. ✅ Policies created
3. 🔄 Deploy Firestore rules (see Option 1 above)
4. ✅ Backend running (localhost:8000)
5. ✅ File watcher running
6. 🔄 Frontend running (localhost:3000)
7. 🎯 **TRY LOGGING IN NOW!**
