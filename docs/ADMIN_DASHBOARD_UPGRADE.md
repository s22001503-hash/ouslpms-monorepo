# Admin Dashboard - Full Upgrade Documentation

## Overview
The Admin Dashboard has been enhanced with two new major features:
1. **Overview Tab** - Real-time system metrics and activity monitoring
2. **Settings Proposal Tab** - Propose system setting changes for Dean approval

---

## 1. Overview Tab

### Features
- **Stat Cards Grid**: Displays 4 key system metrics
  - Print Jobs Today (green gradient)
  - Pending Proposals (orange gradient, clickable)
  - Blocked Attempts (red gradient)
  - Active Users (blue gradient)
  
- **Quick Actions**: Shortcut buttons for common admin tasks
  - Add User
  - Propose Settings
  - Change Password

- **Recent Activity Feed**: Shows last 10 system activities with:
  - Activity type icon
  - Description text
  - Timestamp
  - Status badge (success/warning/error)

- **System Status**: Real-time health indicators
  - Backend API (operational/down)
  - Firebase Auth (operational/down)
  - Firestore (operational/down)

### Navigation
- Clicking the "Pending Proposals" card navigates to Settings Proposal tab
- Quick action buttons navigate to respective admin functions

### Implementation
```jsx
// Component: frontend/src/components/OverviewTab.jsx
<OverviewTab 
  stats={{
    todayPrintJobs: 127,
    pendingProposals: 2,
    blockedAttempts: 5,
    activeUsers: 342,
    recentActivity: [...]
  }}
  onNavigate={(view) => setActiveView(view)}
/>
```

---

## 2. Settings Proposal Tab

### Features

#### Current Settings Display (Read-Only)
Shows currently approved system configuration:
- Max Copies per Document
- Max Print Attempts per Day
- Max Pages per Job
- Daily Quota (pages)
- Allow Color Printing (toggle)

#### Proposal Form
Admin can propose new values with:
- Input validation (positive integers, reasonable ranges)
- Visual comparison (shows current vs proposed)
- Form disables when proposal is pending
- Success/error messaging
- Automatic Dean notification (backend integration)

#### Validation Rules
- Max Copies per Document: 1-100
- Max Print Attempts per Day: 1-200
- Max Pages per Job: 1-500
- Daily Quota: 1-2000 pages
- At least one setting must change from current value

#### Proposal History Table
Shows all previous proposals with:
- Submission timestamp
- Proposed changes (detailed breakdown)
- Status badge (pending/approved/rejected)
- Review timestamp
- Reviewer name

### Workflow
1. Admin reviews current settings
2. Admin proposes new values via form
3. Backend creates document in `settings_requests` collection
4. Dean receives notification (in Dean Dashboard pending approvals)
5. Dean approves/rejects proposal
6. If approved, `system_settings` collection is updated
7. Admin receives notification of decision
8. Form re-enables for new proposals

### Implementation
```jsx
// Component: frontend/src/components/SettingsProposalTab.jsx
<SettingsProposalTab adminId={user.epf} />
```

---

## 3. Integration Changes

### AdminDashboardUI.jsx Updates
```jsx
// Added new state
const [activeView, setActiveView] = useState('overview') // default to overview
const [overviewStats, setOverviewStats] = useState({...})

// Added navigation handler
const handleNavigate = (view) => {
  setActiveView(view)
}

// Added sidebar buttons
<button onClick={() => setActiveView('overview')}>🏠 Overview</button>
<button onClick={() => setActiveView('settingsProposal')}>⚙️ Settings Proposal</button>

// Added conditional rendering
{activeView === 'overview' && <OverviewTab stats={overviewStats} onNavigate={handleNavigate} />}
{activeView === 'settingsProposal' && <SettingsProposalTab adminId={user.epf} />}
```

---

## 4. API Service Functions

### New Functions in `frontend/src/services/api.js`

#### fetchOverviewStats()
```javascript
export async function fetchOverviewStats()
// GET /admin/overview
// Returns: { todayPrintJobs, pendingProposals, blockedAttempts, activeUsers, recentActivity }
```

#### fetchSystemSettings()
```javascript
export async function fetchSystemSettings()
// GET /system-settings
// Returns: { maxCopiesPerDocument, maxPrintAttemptsPerDay, maxPagesPerJob, dailyQuota, allowColorPrinting }
```

#### fetchSettingsRequests(adminId)
```javascript
export async function fetchSettingsRequests(adminId)
// GET /settings-requests?adminId={adminId}
// Returns: [{ id, proposedSettings, status, submittedAt, reviewedAt, reviewedBy }]
```

#### proposeSettings(proposal)
```javascript
export async function proposeSettings(proposal)
// POST /admin/propose-settings
// Body: { adminId, proposedSettings: {...} }
// Returns: { success, message, requestId }
```

---

## 5. Backend API Endpoints (To Be Implemented)

### GET /admin/overview
**Purpose**: Fetch admin dashboard statistics  
**Auth**: Requires valid JWT token, admin role  
**Response**:
```json
{
  "todayPrintJobs": 127,
  "pendingProposals": 2,
  "blockedAttempts": 5,
  "activeUsers": 342,
  "recentActivity": [
    {
      "id": 1,
      "type": "user_added",
      "description": "New user EPF 60001 added",
      "timestamp": "2025-10-18T09:30:00Z",
      "status": "success"
    }
  ]
}
```

### GET /system-settings
**Purpose**: Fetch current approved system settings  
**Auth**: Requires valid JWT token  
**Response**:
```json
{
  "maxCopiesPerDocument": 10,
  "maxPrintAttemptsPerDay": 50,
  "maxPagesPerJob": 100,
  "dailyQuota": 500,
  "allowColorPrinting": true,
  "lastModified": "2025-10-15T10:00:00Z",
  "modifiedBy": "Dean Smith"
}
```

### GET /settings-requests
**Purpose**: Fetch proposal history for an admin  
**Auth**: Requires valid JWT token, admin role  
**Query Params**: `adminId` (optional, filters by admin)  
**Response**:
```json
[
  {
    "id": "req_12345",
    "adminId": "50005",
    "adminEmail": "admin@ousl.edu.lk",
    "proposedSettings": {
      "maxCopiesPerDocument": 15,
      "maxPrintAttemptsPerDay": 60
    },
    "status": "pending",
    "submittedAt": "2025-10-18T09:30:00Z",
    "reviewedAt": null,
    "reviewedBy": null,
    "deanNotes": null
  }
]
```

### POST /admin/propose-settings
**Purpose**: Submit new settings proposal for Dean approval  
**Auth**: Requires valid JWT token, admin role  
**Request Body**:
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
**Response**:
```json
{
  "success": true,
  "message": "Settings proposal submitted successfully",
  "requestId": "req_12345"
}
```

---

## 6. Firestore Schema

### Collection: `system_settings`
Single document with ID `current`:
```json
{
  "maxCopiesPerDocument": 10,
  "maxPrintAttemptsPerDay": 50,
  "maxPagesPerJob": 100,
  "dailyQuota": 500,
  "allowColorPrinting": true,
  "lastModified": "2025-10-15T10:00:00Z",
  "modifiedBy": "dean_epf",
  "modifiedByName": "Dean Smith"
}
```

### Collection: `settings_requests`
Documents with auto-generated IDs:
```json
{
  "adminId": "50005",
  "adminEmail": "admin@ousl.edu.lk",
  "adminName": "Admin User",
  "proposedSettings": {
    "maxCopiesPerDocument": 15,
    "maxPrintAttemptsPerDay": 60,
    "maxPagesPerJob": 120,
    "dailyQuota": 600,
    "allowColorPrinting": false
  },
  "status": "pending",
  "submittedAt": "2025-10-18T09:30:00Z",
  "reviewedAt": null,
  "reviewedBy": null,
  "reviewedByName": null,
  "deanNotes": null
}
```

---

## 7. Testing Checklist

### Overview Tab
- [ ] Verify stats display correctly
- [ ] Test "Pending Proposals" card click navigation
- [ ] Verify quick action buttons work
- [ ] Check recent activity updates in real-time
- [ ] Verify system status indicators reflect actual status

### Settings Proposal Tab
- [ ] Verify current settings display correctly
- [ ] Test input validation (min/max ranges)
- [ ] Test form submission
- [ ] Verify form disables when proposal is pending
- [ ] Test "no changes detected" validation
- [ ] Verify proposal appears in Dean dashboard
- [ ] Test Dean approve/reject workflow
- [ ] Verify proposal history table displays correctly
- [ ] Test status badge colors (pending/approved/rejected)

### Integration
- [ ] Test navigation between all tabs
- [ ] Verify Overview is default view on login
- [ ] Test token refresh during long sessions
- [ ] Verify proper error messages on network failure
- [ ] Test responsive design on mobile/tablet

---

## 8. Future Enhancements

### Overview Tab
- [ ] Add charts for print job trends (daily/weekly)
- [ ] Add system health score meter
- [ ] Add notification bell with unread count
- [ ] Add export data button for reports

### Settings Proposal Tab
- [ ] Add email notifications to Dean when proposal submitted
- [ ] Add email notifications to Admin when proposal reviewed
- [ ] Add comments/notes field for admin to explain proposal
- [ ] Add side-by-side comparison view (current vs proposed)
- [ ] Add proposal templates for common scenarios
- [ ] Add bulk import/export for settings

### General
- [ ] Add real-time updates using WebSockets
- [ ] Add audit trail for all admin actions
- [ ] Add role-based permissions (super admin vs admin)
- [ ] Add scheduled reports generation

---

## 9. Files Modified/Created

### New Files
- `frontend/src/components/OverviewTab.jsx`
- `frontend/src/components/OverviewTab.css`
- `frontend/src/components/SettingsProposalTab.jsx`
- `frontend/src/components/SettingsProposalTab.css`
- `docs/ADMIN_DASHBOARD_UPGRADE.md` (this file)

### Modified Files
- `frontend/src/pages/AdminDashboardUI.jsx`
  - Added Overview and Settings Proposal views
  - Changed default view to 'overview'
  - Added navigation handler
  - Added overview stats state management
  
- `frontend/src/services/api.js`
  - Added `fetchOverviewStats()`
  - Added `fetchSystemSettings()`
  - Added `fetchSettingsRequests(adminId)`
  - Added `proposeSettings(proposal)`

---

## 10. Development Notes

### Current Status
✅ Frontend components complete with mock data  
✅ API service functions defined  
⏳ Backend API endpoints pending implementation  
⏳ Firestore schema pending setup  
⏳ Dean Dashboard integration pending  

### Mock Data
The components currently use mock data for development and testing. Replace mock data with actual API calls once backend endpoints are implemented.

### Styling
The components follow the existing design system:
- Green gradient theme matching admin dashboard
- 48px input heights for consistency
- Card-based layouts
- Responsive breakpoints at 768px and 480px

---

## 11. Security Considerations

### Access Control
- All admin endpoints must verify JWT token
- Role validation: Only admins can propose settings
- Only Dean can approve/reject proposals

### Input Validation
- Backend must re-validate all input ranges
- Sanitize all user input before Firestore storage
- Prevent SQL/NoSQL injection attempts

### Rate Limiting
- Implement rate limiting on proposal submission (e.g., 5 per hour)
- Prevent spam proposals

### Audit Logging
- Log all proposal submissions with timestamps
- Log all Dean approvals/rejections
- Log all settings changes to `admin_actions` collection

---

## 12. Deployment Steps

1. **Frontend Deployment**:
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. **Backend Implementation**:
   - Create `backend/app/routers/admin.py`
   - Implement all 4 endpoints
   - Add rate limiting middleware
   - Add admin role verification dependency

3. **Database Setup**:
   - Create `system_settings` collection with initial document
   - Set up Firestore indexes for `settings_requests` queries
   - Configure security rules

4. **Testing**:
   - Run frontend dev server
   - Run backend dev server
   - Test all features end-to-end
   - Test error scenarios (network failures, invalid input)

5. **Production**:
   - Update environment variables
   - Deploy frontend to hosting
   - Deploy backend to cloud (Cloud Run, AWS Lambda, etc.)
   - Monitor logs for errors

---

## Support & Contact

For questions or issues with this upgrade, contact the development team or refer to:
- Main project README: `README.md`
- Dean Dashboard docs: `docs/DEAN_DASHBOARD.md`
- Backend API docs: `backend/README.md`
