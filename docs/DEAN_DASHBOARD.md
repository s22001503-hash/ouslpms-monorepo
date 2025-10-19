# Dean Dashboard - EcoPrint System

## Overview

The Dean Dashboard is the highest-level administrative interface for the EcoPrint Smart Print Management System. It provides comprehensive oversight, system configuration, approval management, and analytics capabilities for organizational leadership.

## Features

### 1. **Overview Dashboard**
- **System Statistics**: Real-time metrics for users, admins, print jobs, and pending approvals
- **System Status**: Visual indicator of system health (Operational/Maintenance/Down)
- **Recent Activity Feed**: Live stream of system actions and events
- **Quick Stats Cards**: 
  - Total Users
  - Total Administrators
  - Pending Approvals (highlighted)
  - Today's Print Jobs
  - System Status

### 2. **System Configuration**
- **Print Limits**: Configure maximum page limits per job
- **Daily Quotas**: Set organization-wide daily print quotas
- **Color Printing**: Toggle color printing permissions
- **Auto-Approval**: Set threshold for automatic job approval
- **Maintenance Mode**: Enable/disable system maintenance mode
- **Save Configuration**: Persist changes to backend

### 3. **Pending Approvals**
- **Approval Queue**: View all items requiring dean approval
- **Approval Types**:
  - Print Jobs (exceeding limits)
  - User Creation Requests
  - Budget Overages
  - Policy Exceptions
- **Actions**: Approve or Reject with one click
- **Real-time Updates**: Badge shows count of pending items

### 4. **User Oversight**
- **User Statistics**: Total users, admins, active users
- **High-Level Monitoring**: Overview of user base
- **Quick Actions**:
  - View All Users
  - Export User Report
- **Info Note**: Detailed user management delegated to Administrators

### 5. **Reports & Analytics**
- **Print Usage Report**: Weekly print job statistics and trends
- **Cost Analysis**: Department-wise cost breakdown
- **User Activity**: Login and print activity logs
- **System Performance**: Uptime and performance metrics
- **Export Options**: Generate and download reports

### 6. **Audit Logs**
- **Complete Activity Log**: All system actions with timestamps
- **Filtering**: By date, action type (login, user management, print jobs, config)
- **User Tracking**: Who performed each action
- **Status Indicators**: Success/Failed badges
- **Searchable Table**: Easy navigation and analysis

### 7. **Change Password**
- Reuses the shared `ChangePassword` component
- Secure password update with current password verification
- Returns to Overview after successful change

## File Structure

```
frontend/src/pages/
├── DeanDashboard.jsx          # Route protection wrapper
├── DeanDashboardUI.jsx        # Main UI component
└── DeanDashboardUI.css        # Styling
```

## Components

### DeanDashboard.jsx
- Route protection component
- Verifies user has 'dean' role
- Redirects non-dean users to appropriate dashboards
- Shows loading state during authentication

### DeanDashboardUI.jsx
- Main dashboard interface
- Multiple view states managed by `activeView`
- Mock data for demonstration (TODO: Connect to backend APIs)
- Integrates with `ChangePassword` component

### DeanDashboardUI.css
- Blue theme (distinguishes from Admin green/User green)
- Responsive grid layouts
- Card-based design system
- Interactive elements (toggle switches, badges, status indicators)

## Routing

```javascript
// App.jsx
<Route path="/dean" element={
  <ProtectedRoute role="dean">
    <DeanDashboardUI />
  </ProtectedRoute>
} />
```

### Login Redirection
After successful login, users with 'dean' role are automatically redirected to `/dean`.

## State Management

### Active View States
- `overview` (default)
- `systemConfig`
- `approvals`
- `userOversight`
- `reports`
- `auditLogs`
- `changePassword`

### Data States
- `stats`: System-wide statistics
- `pendingApprovals`: Items awaiting dean approval
- `systemConfig`: Configuration values
- `recentActivity`: Activity log entries

## API Integration (TODO)

Currently uses mock data. Replace with actual API calls:

```javascript
// TODO: Fetch stats from backend
useEffect(() => {
  // fetchDeanStats().then(data => setStats(data))
}, [])

// TODO: Fetch pending approvals
useEffect(() => {
  // fetchPendingApprovals().then(data => setPendingApprovals(data))
}, [])

// TODO: Handle approval actions
const handleApproval = async (id, action) => {
  // await approveItem(id, action)
  // Update UI
}

// TODO: Save configuration
const handleSaveConfig = async () => {
  // await saveSystemConfig(systemConfig)
}
```

## Creating a Dean Account

### Using the Backend Script

```powershell
# Navigate to backend
cd backend

# Run the create admin user script (modify for dean role)
python scripts/create_admin_user.py
```

### Manually in Firebase Console

1. Go to Firebase Console → Authentication
2. Add user with email format: `[EPF]@ousl.edu.lk`
3. Set password
4. Go to Firestore → `users` collection
5. Create document with ID = EPF:
   ```json
   {
     "uid": "[Firebase UID]",
     "epf": "[EPF Number]",
     "email": "[EPF]@ousl.edu.lk",
     "role": "dean",
     "department": "Administration",
     "name": "Dean Name",
     "status": "active"
   }
   ```

## Testing

### Login as Dean
1. Use dean EPF (e.g., `60001`)
2. Use password set during account creation
3. Should redirect to `/dean` dashboard
4. Verify all navigation tabs work
5. Test approval actions
6. Test configuration changes
7. Test password change functionality

### Role-Based Access
- Admin users redirected to `/admin`
- Regular users redirected to `/user`
- Unauthenticated users redirected to `/login`

## Styling Theme

### Color Scheme
- **Primary Blue**: `#1e3a8a` to `#2563eb`
- **Background**: Light blue gradient (`#f0f4ff` to `#e6efff`)
- **Cards**: White with subtle shadows
- **Accent**: Blue (`#3b82f6`)
- **Success**: Green (`#10b981`)
- **Danger**: Red (`#ef4444`)

### Design Principles
- Consistent with Admin/User dashboards
- Blue theme for dean-specific identity
- Card-based layout
- Responsive grid system
- Clear visual hierarchy

## Future Enhancements

### Backend Integration
- [ ] Connect to real-time stats API
- [ ] Implement approval workflow endpoints
- [ ] Add system configuration persistence
- [ ] Create report generation APIs
- [ ] Implement audit log queries

### Features
- [ ] Real-time notifications for pending approvals
- [ ] Advanced filtering and search
- [ ] Dashboard customization
- [ ] Data visualization (charts/graphs)
- [ ] Bulk approval actions
- [ ] Scheduled reports
- [ ] Export to PDF/Excel
- [ ] Email notifications

### UI Improvements
- [ ] Loading skeletons
- [ ] Animated transitions
- [ ] Toast notifications
- [ ] Modal confirmations
- [ ] Drag-and-drop customization
- [ ] Dark mode support

## Security Considerations

- ✅ Role-based access control (dean role required)
- ✅ Route protection with authentication check
- ✅ Secure password change with current password verification
- ✅ Firebase authentication integration
- 🔄 TODO: API rate limiting
- 🔄 TODO: Activity logging for all dean actions
- 🔄 TODO: Multi-factor authentication option

## Responsive Design

- Desktop: Full sidebar navigation
- Tablet: Horizontal scrollable nav
- Mobile: Stacked layout, simplified stats grid

## Dependencies

- React 18+
- React Router 6+
- Firebase Auth & Firestore
- Custom `useAuth` hook
- Shared `ChangePassword` component

## Support

For issues or questions:
1. Check console for errors
2. Verify Firebase configuration
3. Ensure dean role is properly set in Firestore
4. Test authentication flow step-by-step

---

**Status**: ✅ UI Complete | 🔄 Backend Integration Pending
**Created**: October 2025
**Last Updated**: October 2025
