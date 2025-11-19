# 🎯 Admin Dashboard - What to Do Next

## ✅ Deployment Complete!

**Status:**
- ✅ Firestore rules deployed successfully
- ✅ Firestore indexes deployed (old print_jobs index removed)
- ✅ Firebase authentication: lahirujee123@gmail.com
- ✅ All policy proposal components integrated

---

## 🚀 Next Steps: Test the Admin Dashboard

### Step 1: Start the Frontend (5 seconds)

```powershell
cd "c:\Users\user\Desktop\OCT project\ouslpms-monorepo\frontend"
npm run dev
```

**Expected output:**
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

---

### Step 2: Login as Admin

1. **Open browser:** http://localhost:5173/
2. **Login with:**
   - Email: `admin@ousl.lk` (or `99999@ousl.edu.lk`)
   - Password: `admin123` (or your configured admin password)

3. **Navigate to Admin Dashboard**

---

### Step 3: Test New Features (Policy Proposals Tab)

#### 3A. Test Policy Proposal Tab

1. **Click "📝 Policy Proposals" button** in admin navigation
2. **You should see 3 sections:**

   **Section 1: Current Global Policies**
   ```
   Maximum Attempts Per Day: 5
   Maximum Copies Per Document: 5
   ```

   **Section 2: Submit New Proposal**
   - Field 1: `Max Attempts Per Day` (number input)
   - Field 2: `Max Copies Per Document` (number input)
   - Button: "Submit Proposal"

   **Section 3: Pending Proposals**
   - Should show 2 sample proposals created during initialization
   - Status: "Pending" (yellow badge)

3. **Try creating a proposal:**
   - Enter: Max Attempts = 10
   - Enter: Max Copies = 15
   - Click "Submit Proposal"
   - ✅ Should appear in "Pending Proposals" section

4. **Check Firestore Console:**
   - Go to: https://console.firebase.google.com/project/oct-project-25fad/firestore/databases/-default-/data/~2Fpolicy_proposals
   - ✅ Should see your new proposal document

---

#### 3B. Test Special Users Tab

1. **Click "⭐ Special Users" button** in admin navigation
2. **You should see:**

   **Section 1: Add Special User**
   - EPF Number input field
   - "Search User" button

   **Section 2: Active Special Users**
   - Should show sample special user from initialization
   - Each user shows: EPF, Name, Max Attempts, Max Copies, "Remove" button

3. **Try adding a special user:**
   - Enter EPF: `60001` (or any existing user EPF)
   - Click "Search User"
   - Set custom limits (e.g., 20 attempts, 30 copies)
   - Click "Save"
   - ✅ Should appear in "Active Special Users" section

4. **Try removing a user:**
   - Click "Remove" button on any special user
   - ✅ Should be removed from the list

---

### Step 4: Test Other Tabs (Verify No Errors)

Click through each navigation button to ensure no errors:

1. **🏠 Overview**
   - ✅ Should show system stats
   
2. **👥 User Management**
   - ✅ Should show user list
   - ✅ Add/Remove user buttons work

3. **📊 System Analytics**
   - ✅ Should show analytics dashboard

4. **🖨️ Print Document**
   - ✅ Should show print upload form

5. **🔒 Change Password**
   - ✅ Should show password change form

---

### Step 5: Check Browser Console (F12)

1. **Press F12** to open DevTools
2. **Go to Console tab**
3. **Look for errors:**
   - ❌ Red errors = something broken
   - ⚠️ Yellow warnings = OK (may be deprecation warnings)
   - 🔵 Blue/Gray info = normal

**Common issues:**
- "Failed to fetch" → Backend not running
- "Firebase auth error" → Not logged in
- "Firestore permission denied" → Rules not deployed (but we just deployed them!)

---

### Step 6: Verify Firestore Data

**Check collections in Firebase Console:**

1. **global_policies**
   - Go to: https://console.firebase.google.com/project/oct-project-25fad/firestore/databases/-default-/data/~2Fglobal_policies
   - ✅ Should see 1 document with maxAttemptsPerDay: 5, maxCopiesPerDoc: 5

2. **policy_proposals**
   - Go to: https://console.firebase.google.com/project/oct-project-25fad/firestore/databases/-default-/data/~2Fpolicy_proposals
   - ✅ Should see 2-3 proposals (2 samples + your new one)

3. **user_special_policies**
   - Go to: https://console.firebase.google.com/project/oct-project-25fad/firestore/databases/-default-/data/~2Fuser_special_policies
   - ✅ Should see 1 document for sample special user

---

## 🐛 Troubleshooting

### Issue 1: "Policy Proposals" tab is empty

**Possible causes:**
- Firestore collections not initialized
- Firestore rules blocking read access

**Solution:**
```powershell
cd "c:\Users\user\Desktop\OCT project\ouslpms-monorepo\backend"
python init_policy_collections.py init
```

---

### Issue 2: "Permission denied" errors

**Possible causes:**
- Not logged in as admin
- Firestore rules not deployed

**Solution:**
1. Check you're logged in as admin (role = 'admin')
2. Re-deploy rules:
   ```powershell
   cd "c:\Users\user\Desktop\OCT project\ouslpms-monorepo"
   firebase deploy --only firestore:rules
   ```

---

### Issue 3: Components not rendering

**Possible causes:**
- Import errors in AdminDashboardUI.jsx
- Component files missing

**Solution:**
1. Check browser console (F12) for import errors
2. Verify files exist:
   - `frontend/src/components/PolicyProposalTab.jsx`
   - `frontend/src/components/SpecialUsersManagementTab.jsx`

---

### Issue 4: API calls failing

**Possible causes:**
- Backend not running
- API endpoints not integrated

**Solution:**
1. Start backend (if needed):
   ```powershell
   cd "c:\Users\user\Desktop\OCT project\ouslpms-monorepo\backend"
   python -m uvicorn app.main:app --reload
   ```

2. Check if API endpoints are in `backend/app/main.py`:
   ```python
   from app.routers import policy_proposals
   app.include_router(policy_proposals.router, prefix="/api", tags=["policies"])
   ```

---

## 📋 Testing Checklist

Use this checklist to verify everything works:

### Frontend Components
- [ ] Policy Proposals tab loads without errors
- [ ] Special Users tab loads without errors
- [ ] Current policies display correctly
- [ ] Can submit new policy proposal
- [ ] Can add special user
- [ ] Can remove special user
- [ ] All 7 navigation buttons work

### Firestore Integration
- [ ] global_policies collection exists
- [ ] policy_proposals collection exists
- [ ] user_special_policies collection exists
- [ ] Can read data from Firestore
- [ ] Can write data to Firestore
- [ ] Rules allow admin access
- [ ] Rules block unauthorized access

### UI/UX
- [ ] Forms validate input
- [ ] Buttons have hover effects
- [ ] Colors match design (blue theme)
- [ ] No layout issues
- [ ] Mobile responsive (test with F12 → Device Toolbar)

---

## 🎉 Success Criteria

**You'll know it's working when:**

1. ✅ Policy Proposals tab shows 3 sections with data
2. ✅ Can create new proposal and see it appear immediately
3. ✅ Special Users tab shows existing users
4. ✅ Can add/remove special users without errors
5. ✅ Browser console shows no red errors
6. ✅ Firestore console shows new documents when you create proposals

---

## 🚀 What's Next? (Optional Enhancements)

### Backend Integration (if not done yet)

1. **Add policy endpoints to main app:**
   ```powershell
   cd "c:\Users\user\Desktop\OCT project\ouslpms-monorepo\backend"
   # Edit app/main.py to include policy router
   ```

2. **Test API endpoints:**
   - GET http://localhost:8000/api/admin/current-policies
   - POST http://localhost:8000/api/admin/propose-policy
   - GET http://localhost:8000/api/admin/special-policy-users

### VC Dashboard (for Vice Chancellor approval)

1. **Create VC role user:**
   ```powershell
   cd backend
   python create_vc_user.py
   ```

2. **Login as VC and approve proposals:**
   - VC sees "Pending Proposals" tab
   - Can approve/reject proposals
   - Approved proposals update global_policies

### Email Notifications

1. **Add email service:**
   - Install: `pip install sendgrid`
   - Configure email templates
   - Send notifications when:
     - New proposal submitted (notify VC)
     - Proposal approved (notify admin)
     - Proposal rejected (notify admin)

---

## 📚 Documentation

- **Full Setup:** `POLICY_BACKEND_SETUP.md`
- **Implementation Summary:** `POLICY_SYSTEM_COMPLETE.md`
- **Manual Deployment:** `FIREBASE_MANUAL_DEPLOYMENT.md`
- **Steps 1-5 Status:** `STEPS_1_TO_5_STATUS.md`

---

## 🆘 Need Help?

**Check logs:**
- Browser Console (F12 → Console)
- Backend logs (terminal running uvicorn)
- Firebase logs (Console → Functions → Logs)

**Common commands:**
```powershell
# Reinitialize Firestore collections
cd backend
python init_policy_collections.py init

# Verify collections
python init_policy_collections.py verify

# Re-deploy rules
cd ..
firebase deploy --only firestore:rules

# Re-deploy indexes
firebase deploy --only firestore:indexes

# Start frontend
cd frontend
npm run dev

# Start backend (if needed)
cd ../backend
python -m uvicorn app.main:app --reload
```

---

## 🎯 Your Immediate Action Plan

**RIGHT NOW (2 minutes):**

1. Start frontend:
   ```powershell
   cd "c:\Users\user\Desktop\OCT project\ouslpms-monorepo\frontend"
   npm run dev
   ```

2. Open browser: http://localhost:5173/

3. Login as admin

4. Click "📝 Policy Proposals" button

5. **If you see 3 sections with data** → ✅ SUCCESS! Everything works!

6. **If you see errors** → Check browser console (F12) and tell me the error message

---

**Let me know what you see!** 🚀
