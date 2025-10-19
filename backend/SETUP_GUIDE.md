# Backend Setup Guide - Admin Dashboard Upgrade

This guide will help you set up the backend API endpoints for the Admin Dashboard upgrade.

## 📋 What's Been Added

### New Files
- `backend/app/routers/admin.py` - Admin dashboard API endpoints
- `backend/init_firestore.py` - Script to initialize Firestore collections

### Updated Files
- `backend/app/main.py` - Added admin router

### API Endpoints Created

1. **GET /admin/overview** - Get dashboard statistics
2. **GET /system-settings** - Get current system settings
3. **GET /settings-requests** - Get proposal history
4. **POST /admin/propose-settings** - Submit new settings proposal
5. **POST /dean/review-proposal/{proposal_id}** - Dean approves/rejects proposal

---

## 🚀 Setup Instructions

### Step 1: Initialize Firestore Collections

Run the initialization script to create necessary Firestore collections:

```powershell
cd backend
.\.venv\Scripts\python.exe init_firestore.py
```

This will:
- Create `system_settings` collection with default values
- Create empty `settings_requests` collection
- Optionally create a sample proposal for testing

**Default Settings Created:**
- Max Copies per Document: 10
- Max Print Attempts per Day: 50
- Max Pages per Job: 100
- Daily Quota: 500 pages
- Color Printing: Enabled

### Step 2: Verify Backend Server

Make sure your backend server is running:

```powershell
cd backend
$env:GOOGLE_APPLICATION_CREDENTIALS = 'C:\Users\user\Desktop\OUspms\backend\firebase-adminsdk.json'
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

You should see:
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Step 3: Test API Endpoints

#### Test 1: Get System Settings
```powershell
# Get your Firebase token from browser console after logging in
# Then test the endpoint:
curl http://localhost:8000/system-settings `
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

Expected response:
```json
{
  "maxCopiesPerDocument": 10,
  "maxPrintAttemptsPerDay": 50,
  "maxPagesPerJob": 100,
  "dailyQuota": 500,
  "allowColorPrinting": true,
  "lastModified": "2025-10-18T...",
  "modifiedBy": "system"
}
```

#### Test 2: Get Overview Stats
```powershell
curl http://localhost:8000/admin/overview `
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

Expected response:
```json
{
  "todayPrintJobs": 0,
  "pendingProposals": 0,
  "blockedAttempts": 0,
  "activeUsers": 3,
  "recentActivity": [...]
}
```

#### Test 3: Submit Settings Proposal (via Frontend)
1. Login to admin dashboard at http://localhost:5173
2. Navigate to "Settings Proposal" tab
3. Change some values in the form
4. Click "Submit Proposal"
5. Should see success message

---

## 🗂️ Firestore Collections Structure

### Collection: `system_settings`
**Document ID:** `current`

```javascript
{
  maxCopiesPerDocument: 10,
  maxPrintAttemptsPerDay: 50,
  maxPagesPerJob: 100,
  dailyQuota: 500,
  allowColorPrinting: true,
  lastModified: "2025-10-18T10:30:00Z",
  modifiedBy: "dean_epf",
  modifiedByName: "Dean Name"
}
```

### Collection: `settings_requests`
**Documents:** Auto-generated IDs

```javascript
{
  adminId: "50005",
  adminEmail: "50005@ousl.edu.lk",
  adminName: "Admin User",
  proposedSettings: {
    maxCopiesPerDocument: 15,
    maxPrintAttemptsPerDay: 60,
    maxPagesPerJob: 120,
    dailyQuota: 600,
    allowColorPrinting: false
  },
  status: "pending",  // or "approved" or "rejected"
  submittedAt: "2025-10-18T09:30:00Z",
  reviewedAt: null,
  reviewedBy: null,
  reviewedByName: null,
  deanNotes: null
}
```

---

## 🔍 API Endpoint Details

### 1. GET /admin/overview
**Purpose:** Fetch admin dashboard statistics  
**Auth:** Requires JWT token, admin role  
**Returns:**
- `todayPrintJobs` - Count of print jobs today
- `pendingProposals` - Count of pending settings proposals
- `blockedAttempts` - Count of blocked login attempts today
- `activeUsers` - Total count of active users
- `recentActivity` - Array of last 10 admin actions

### 2. GET /system-settings
**Purpose:** Get current approved system settings  
**Auth:** Requires JWT token, admin role  
**Returns:** Current settings with metadata (lastModified, modifiedBy)

### 3. GET /settings-requests
**Purpose:** Get proposal history  
**Auth:** Requires JWT token, admin role  
**Query Params:** `adminId` (optional) - filter by specific admin  
**Returns:** Array of proposals ordered by submission date (newest first)

### 4. POST /admin/propose-settings
**Purpose:** Submit new settings proposal  
**Auth:** Requires JWT token, admin role  
**Body:**
```json
{
  "adminId": "50005",
  "proposedSettings": {
    "maxCopiesPerDocument": 15,
    "maxPrintAttemptsPerDay": 60,
    "maxPagesPerJob": 120,
    "dailyQuota": 600,
    "allowColorPrinting": false
  }
}
```
**Validation:**
- Max Copies: 1-100
- Max Attempts: 1-200
- Max Pages: 1-500
- Daily Quota: 1-2000
- Checks for existing pending proposal (only one allowed at a time)

**Returns:**
```json
{
  "success": true,
  "message": "Settings proposal submitted successfully",
  "requestId": "abc123xyz"
}
```

### 5. POST /dean/review-proposal/{proposal_id}
**Purpose:** Dean approves or rejects a proposal  
**Auth:** Requires JWT token, dean role (currently uses admin role)  
**Path Param:** `proposal_id` - ID of proposal to review  
**Body:**
```json
{
  "approve": true,
  "dean_notes": "Approved for increased capacity"
}
```
**Actions:**
- Updates proposal status to "approved" or "rejected"
- If approved, updates `system_settings/current` document
- Logs action to `admin_actions` collection

---

## 🐛 Troubleshooting

### Error: "Firebase Admin not configured"
**Solution:** Make sure you set the environment variable:
```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS = 'C:\Users\user\Desktop\OUspms\backend\firebase-adminsdk.json'
```

### Error: "Missing or invalid authorization header"
**Solution:** Make sure you're sending the JWT token:
```javascript
headers: {
  'Authorization': `Bearer ${token}`
}
```

### Error: "You already have a pending proposal"
**Solution:** This is intentional. You can only have one pending proposal at a time. Wait for Dean to approve/reject the existing one, or manually update the status in Firestore.

### Frontend shows "Network error: Cannot connect to server"
**Solutions:**
1. Check backend is running on port 8000
2. Check CORS settings in `main.py` include port 5173
3. Check firewall/antivirus isn't blocking connections

### Firestore permission denied errors
**Solutions:**
1. Verify service account key path is correct
2. Check service account has Firestore permissions
3. Verify Firebase project ID matches

---

## 📊 Testing Workflow

### Complete End-to-End Test

1. **Initialize Firestore:**
   ```powershell
   cd backend
   .\.venv\Scripts\python.exe init_firestore.py
   ```
   Choose "y" to create sample proposal

2. **Start Backend:**
   ```powershell
   $env:GOOGLE_APPLICATION_CREDENTIALS = 'C:\Users\user\Desktop\OUspms\backend\firebase-adminsdk.json'
   .\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
   ```

3. **Start Frontend:**
   ```powershell
   cd ..\frontend
   npm run dev
   ```

4. **Login as Admin:**
   - Navigate to http://localhost:5173
   - Login with EPF: 50005, Password: 5000555

5. **Test Overview Tab:**
   - Should see dashboard with real stats
   - Active Users should show actual count from Firestore
   - Pending Proposals should show 1 (if you created sample)
   - Recent activity should show recent admin actions

6. **Test Settings Proposal:**
   - Click "⚙️ Settings Proposal" in sidebar
   - Current settings should show: max copies=10, max attempts=50, etc.
   - Change max copies to 15, max attempts to 60
   - Click "Submit Proposal"
   - Should see success message
   - Form should disable with "Pending Proposal" badge
   - New proposal should appear in history table with "Pending" status

7. **Test Dean Review (TODO):**
   - Login as Dean (when implemented)
   - View pending proposals
   - Approve or reject
   - Verify settings update if approved

---

## 🔒 Security Notes

1. **Token Verification:** All endpoints use `verify_admin` dependency to ensure only authenticated admins can access

2. **Input Validation:** All settings values are validated on backend (ranges, types)

3. **Rate Limiting:** Consider adding rate limiting to prevent spam proposals

4. **Audit Logging:** All actions are logged to `admin_actions` collection

5. **Role-Based Access:** TODO - Create separate `verify_dean` dependency for dean-only endpoints

---

## 🚧 TODO / Future Improvements

- [ ] Create `verify_dean` dependency for dean-specific endpoints
- [ ] Add email notifications when proposal is submitted/reviewed
- [ ] Add rate limiting middleware (e.g., 5 proposals per hour)
- [ ] Add WebSocket support for real-time updates
- [ ] Add print jobs tracking (currently returns 0)
- [ ] Add blocked attempts tracking (currently returns 0)
- [ ] Add proposal comments/discussion feature
- [ ] Add proposal versioning/history comparison
- [ ] Add scheduled reports generation

---

## 📞 Need Help?

If you encounter issues:
1. Check the error message in terminal
2. Check browser console for frontend errors
3. Verify Firestore collections exist in Firebase Console
4. Test API endpoints directly with curl/Postman
5. Check logs in `admin_actions` collection

---

## ✅ Success Checklist

- [ ] `init_firestore.py` ran successfully
- [ ] Backend server starts without errors
- [ ] Frontend shows Overview tab as default
- [ ] Overview tab shows real stats from Firestore
- [ ] Settings Proposal tab loads current settings
- [ ] Can submit a settings proposal successfully
- [ ] Proposal appears in history table
- [ ] Form disables when proposal is pending
- [ ] No errors in browser console
- [ ] No errors in backend terminal

**When all boxes are checked, your backend is fully operational!** 🎉
