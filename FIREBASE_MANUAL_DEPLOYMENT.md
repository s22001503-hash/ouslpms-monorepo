# Firebase Deployment - Manual Steps

## Step 2: Deploy Firestore Rules (Manual)

Since we can't run interactive Firebase login in this environment, you need to deploy manually:

### Option A: Firebase Console (Recommended)

1. Go to [Firebase Console](https://console.firebase.google.com/project/oct-project-25fad/firestore/rules)

2. Copy and paste these rules:

```javascript
rules_version = '2';

service cloud.firestore {
  match /databases/{database}/documents {
    
    // Helper function to check if user is authenticated
    function isAuthenticated() {
      return request.auth != null;
    }
    
    // Helper function to check if user is admin
    function isAdmin() {
      return isAuthenticated() && 
             get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'admin';
    }
    
    // Helper function to check if user is dean
    function isDean() {
      return isAuthenticated() && 
             get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'dean';
    }
    
    // Helper function to check if user is VC
    function isVC() {
      return isAuthenticated() && 
             get(/databases/$(database)/documents/users/$(request.auth.uid)).data.role == 'vc';
    }
    
    // Helper function to check if accessing own data
    function isOwner(userId) {
      return isAuthenticated() && request.auth.uid == userId;
    }
    
    // Users collection
    match /users/{userId} {
      allow read: if isOwner(userId) || isAdmin() || isDean();
      allow update: if isOwner(userId) && !request.resource.data.diff(resource.data).affectedKeys().hasAny(['role', 'email']);
      allow create, delete: if isAdmin();
    }
    
    // Departments collection
    match /departments/{departmentId} {
      allow read: if isAuthenticated();
      allow write: if isAdmin();
    }
    
    // Roles collection
    match /roles/{roleId} {
      allow read: if isAuthenticated();
      allow write: if isAdmin();
    }
    
    // Policies collection
    match /policies/{policyId} {
      allow read: if isAuthenticated();
      allow write: if isAdmin() || isDean();
    }
    
    // Print jobs collection
    match /print_jobs/{jobId} {
      allow read: if isOwner(resource.data.user_id) || isAdmin() || isDean();
      allow create: if true;
      allow update, delete: if isAdmin();
    }
    
    // Blocked prints collection
    match /blocked_prints/{jobId} {
      allow read: if isOwner(resource.data.user_id) || isAdmin() || isDean();
      allow create: if true;
      allow update, delete: if isAdmin();
    }
    
    // System settings (admin only)
    match /system_settings/{setting} {
      allow read: if isAuthenticated();
      allow write: if isAdmin();
    }
    
    // Policy Proposals - Admin can create, VC can approve/reject
    match /policy_proposals/{proposalId} {
      allow read: if isAdmin() || isVC() || isDean();
      allow create: if isAdmin();
      allow update: if isVC();
      allow delete: if isAdmin();
    }
    
    // User Special Policies - Admin/VC read, system writes after VC approval
    match /user_special_policies/{epf} {
      allow read: if isAdmin() || isVC() || isDean() || isOwner(epf);
      allow write: if isAdmin() || isVC();
    }
    
    // Global Policies - Everyone can read, VC can write
    match /global_policies/{docId} {
      allow read: if isAuthenticated();
      allow write: if isVC() || isAdmin();
    }
    
    // Allow backend service account full access
    match /{document=**} {
      allow read, write: if request.auth == null;
    }
  }
}
```

3. Click "Publish"

### Option B: Firebase CLI (After Login)

Run these commands in PowerShell:

```powershell
# Login to Firebase
firebase login

# Deploy rules
cd "c:\Users\user\Desktop\OCT project\ouslpms-monorepo"
firebase deploy --only firestore:rules
```

## Step 3: Create Firestore Indexes (Manual)

1. Go to [Firebase Console - Indexes](https://console.firebase.google.com/project/oct-project-25fad/firestore/indexes)

2. Click "Add Index" and create these two indexes:

### Index 1:
- **Collection ID:** `policy_proposals`
- **Fields:**
  - `type` - Ascending
  - `status` - Ascending
  - `submittedAt` - Descending
- **Query scope:** Collection
- Click "Create Index"

### Index 2:
- **Collection ID:** `policy_proposals`
- **Fields:**
  - `status` - Ascending
  - `submittedAt` - Descending
- **Query scope:** Collection
- Click "Create Index"

**Note:** Index creation takes 5-10 minutes. You'll receive an email when complete.

### Option B: Deploy via CLI

```powershell
firebase deploy --only firestore:indexes
```

The indexes are already defined in `backend/firestore.indexes.json`.

---

## ✅ Verification

After deploying, verify in Firebase Console:
- Rules show the new policy_proposals, user_special_policies, and global_policies sections
- Indexes show "Enabled" status (may take a few minutes)

---

## Next Steps

Continue with Steps 4-5 which can be done without Firebase login.
