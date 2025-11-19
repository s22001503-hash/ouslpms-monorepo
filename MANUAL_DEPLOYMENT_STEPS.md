# 📋 Manual Deployment Steps - Complete Guide

## 🎯 What You Need to Do

You need to complete **2 manual steps** in the Firebase Console because the Firebase CLI requires authentication that can't be done programmatically.

---

## 🔥 Step 2: Deploy Firestore Rules (5 minutes)

### Method 1: Firebase Console (EASIEST) ⭐

1. **Open Firebase Console:**
   - Go to: https://console.firebase.google.com/
   - Select project: **oct-project-25fad**

2. **Navigate to Firestore Rules:**
   - Click "Firestore Database" in left sidebar
   - Click "Rules" tab at the top
   
3. **Copy the Rules:**
   - Open file: `c:\Users\user\Desktop\OCT project\ouslpms-monorepo\backend\firestore.rules`
   - Select ALL text (Ctrl+A)
   - Copy (Ctrl+C)

4. **Paste and Publish:**
   - In Firebase Console, select all existing rules text
   - Paste the new rules (Ctrl+V)
   - Click **"Publish"** button (top right)
   - Wait for confirmation message

### Method 2: Firebase CLI (if you prefer terminal)

```powershell
# Step 1: Login to Firebase
firebase login

# Step 2: Navigate to project
cd "c:\Users\user\Desktop\OCT project\ouslpms-monorepo"

# Step 3: Deploy rules
firebase deploy --only firestore:rules
```

### ✅ Verification
- You should see "Rules published successfully"
- No errors in the Rules editor

---

## 📊 Step 3: Create Firestore Indexes (10 minutes)

### Method 1: Firebase Console (RECOMMENDED) ⭐

1. **Open Firebase Console:**
   - Go to: https://console.firebase.google.com/
   - Select project: **oct-project-25fad**

2. **Navigate to Indexes:**
   - Click "Firestore Database" in left sidebar
   - Click "Indexes" tab at the top
   - Click "Composite" sub-tab

3. **Create Index 1:**
   - Click **"Create Index"** button
   - Fill in:
     - **Collection ID:** `policy_proposals`
     - **Fields to index:**
       1. Field: `type`, Order: **Ascending**
       2. Click "+ Add field"
       3. Field: `status`, Order: **Ascending**
       4. Click "+ Add field"
       5. Field: `submittedAt`, Order: **Descending**
     - **Query scopes:** Collection
   - Click **"Create"**
   - Status will show "Building..." (this takes 5-10 minutes)

4. **Create Index 2:**
   - Click **"Create Index"** button again
   - Fill in:
     - **Collection ID:** `policy_proposals`
     - **Fields to index:**
       1. Field: `status`, Order: **Ascending**
       2. Click "+ Add field"
       3. Field: `submittedAt`, Order: **Descending**
     - **Query scopes:** Collection
   - Click **"Create"**
   - Status will show "Building..."

5. **Wait for Completion:**
   - Both indexes will show "Building..." for 5-10 minutes
   - You'll receive an email when they're ready
   - Refresh the page to see status change to "Enabled"

### Method 2: Firebase CLI

```powershell
# Step 1: Login (if not already)
firebase login

# Step 2: Navigate to project
cd "c:\Users\user\Desktop\OCT project\ouslpms-monorepo"

# Step 3: Deploy indexes
firebase deploy --only firestore:indexes
```

### Method 3: Click Error Link (EASIEST!) ⭐⭐⭐

When you try to query without indexes, Firestore will show an error with a **direct link** to create the index. This is the fastest method!

1. Start your app and try to view policy proposals
2. Open browser console (F12)
3. Look for Firestore error with a link like:
   ```
   https://console.firebase.google.com/project/oct-project-25fad/firestore/indexes?create_composite=...
   ```
4. Click the link - it will auto-fill all index fields!
5. Just click "Create" - done!

### ✅ Verification
- Both indexes show status "Enabled" (not "Building")
- No error emails from Firebase
- Queries work without errors

---

## 🖼️ Visual Guide - Screenshots Reference

### Firebase Console Navigation:
```
Firebase Console Homepage
  └─ Select "oct-project-25fad" project
      └─ Left Sidebar: "Firestore Database"
          ├─ Tab: "Data" (view collections)
          ├─ Tab: "Rules" ← Deploy rules here
          └─ Tab: "Indexes"
              ├─ Single field (auto-created)
              └─ Composite ← Create indexes here
```

### Firestore Rules Editor:
```
┌─────────────────────────────────────────────────┐
│ Firestore Database > Rules                      │
├─────────────────────────────────────────────────┤
│ [Edit rules]  [Simulator]               Publish │
├─────────────────────────────────────────────────┤
│ rules_version = '2';                             │
│ service cloud.firestore {                        │
│   match /databases/{database}/documents {        │
│     // Paste your rules here                     │
│   }                                               │
│ }                                                 │
└─────────────────────────────────────────────────┘
```

### Create Index Form:
```
┌─────────────────────────────────────────────────┐
│ Create a new index                               │
├─────────────────────────────────────────────────┤
│ Collection ID: [policy_proposals          ▼]    │
│                                                   │
│ Fields to index:                                 │
│   Field path     Index mode    Array config     │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│   │ type     │  │Ascending ▼│  │          │     │
│   └──────────┘  └──────────┘  └──────────┘     │
│                                    [+ Add field] │
│                                                   │
│ Query scope: ⦿ Collection  ○ Collection group   │
│                                                   │
│                          [Cancel]  [Create]      │
└─────────────────────────────────────────────────┘
```

---

## 🚨 Common Issues & Solutions

### Issue 1: "Firebase CLI not logged in"
**Error:** `Error: Not authenticated`

**Solution:**
```powershell
firebase login
```
This will open a browser window. Login with your Google account.

---

### Issue 2: "Index already exists"
**Error:** `Index already exists`

**Solution:**
- Go to Firestore Console > Indexes > Composite
- Check if index already exists
- If status is "Enabled", you're done!
- If status is "Error", delete and recreate

---

### Issue 3: "Index building stuck"
**Error:** Index shows "Building..." for more than 20 minutes

**Solution:**
- Refresh the Firebase Console page
- If still stuck, delete the index and recreate
- Check Firebase Status page: https://status.firebase.google.com/

---

### Issue 4: "Permission denied" when deploying rules
**Error:** `Permission denied`

**Solution:**
- Make sure you're logged in with the correct Google account
- Check you have "Owner" or "Editor" role on the project
- Go to Firebase Console > Project Settings > Users and Permissions

---

## 🎬 Quick Start (TL;DR)

**Fastest way to complete both steps:**

1. **Open:** https://console.firebase.google.com/project/oct-project-25fad
2. **Rules:** 
   - Click "Firestore Database" → "Rules" tab
   - Copy from `backend/firestore.rules` and paste
   - Click "Publish"
3. **Indexes:**
   - Click "Indexes" tab → "Create Index"
   - Add Index 1: `policy_proposals` → `type` (Asc) + `status` (Asc) + `submittedAt` (Desc)
   - Add Index 2: `policy_proposals` → `status` (Asc) + `submittedAt` (Desc)
   - Wait 5-10 minutes for "Enabled" status

**Done!** ✅

---

## 📝 What These Steps Do

### Firestore Rules (Step 2):
- **Controls who can read/write data**
- Rules we're deploying:
  - ✅ Admins can create policy proposals
  - ✅ VCs can approve/reject proposals
  - ✅ Deans can view special policies
  - ✅ Everyone can read global policies
  - ❌ Students cannot modify policies

### Firestore Indexes (Step 3):
- **Makes queries fast and efficient**
- Indexes we're creating:
  - Index 1: Filter proposals by type AND status, sorted by date
  - Index 2: Filter proposals by status, sorted by date
- Without these, queries will fail with "Index required" error

---

## ✅ Verification Checklist

After completing manual steps, verify:

- [ ] Firebase Console shows "Rules published successfully"
- [ ] Both indexes show status "Enabled" (not "Building")
- [ ] No error emails from Firebase
- [ ] Can view Firestore collections in console
- [ ] No permission errors when testing app

---

## 🆘 Need Help?

If you encounter issues:

1. **Check Firebase Console:**
   - https://console.firebase.google.com/project/oct-project-25fad

2. **View Firestore Data:**
   - Go to "Firestore Database" → "Data" tab
   - Should see: `global_policies`, `policy_proposals`, `user_special_policies`

3. **Test Connection:**
   ```powershell
   cd "c:\Users\user\Desktop\OCT project\ouslpms-monorepo\backend"
   python init_policy_collections.py verify
   ```

4. **Check Logs:**
   - Firebase Console → Functions → Logs (if using Cloud Functions)
   - Browser Console (F12) → Console tab

---

## 🎉 After Completion

Once both manual steps are done:

1. **Test Frontend:**
   ```powershell
   cd "c:\Users\user\Desktop\OCT project\ouslpms-monorepo\frontend"
   npm run dev
   ```

2. **Test Backend API:**
   ```powershell
   cd "c:\Users\user\Desktop\OCT project\ouslpms-monorepo\backend"
   python -m uvicorn app.main:app --reload
   ```

3. **Navigate to Admin Dashboard:**
   - Login as admin
   - Click "📝 Policy Proposals" tab
   - Try creating a proposal
   - Should work without errors!

---

## 📚 Related Files

- Rules source: `backend/firestore.rules`
- Indexes definition: `backend/firestore.indexes.json`
- Firebase config: `firebase.json`
- Project config: `.firebaserc`
- Initialization script: `backend/init_policy_collections.py`

---

**Total Time Required:** ~15 minutes (5 min rules + 10 min indexes)

**Difficulty:** 🟢 Easy (just copy/paste in Firebase Console)

**Required Access:** Firebase Console access to oct-project-25fad project
