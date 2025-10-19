# Dean Dashboard Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        DEAN DASHBOARD ARCHITECTURE                       │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                             FRONTEND LAYER                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                  DeanDashboardUI.jsx                              │  │
│  │  ┌────────────────────────────────────────────────────────────┐  │  │
│  │  │ Sidebar                Main Content Area                    │  │  │
│  │  │ ┌──────────┐          ┌─────────────────────────────────┐  │  │  │
│  │  │ │ Overview │────────> │ OverviewTab                     │  │  │  │
│  │  │ │          │          │ • 4 Stats Cards                 │  │  │  │
│  │  │ │          │          │ • 1 Quick Action (Review)       │  │  │  │
│  │  │ └──────────┘          └─────────────────────────────────┘  │  │  │
│  │  │                                                              │  │  │
│  │  │ ┌──────────┐          ┌─────────────────────────────────┐  │  │  │
│  │  │ │Notificat.│────────> │ Notifications List              │  │  │  │
│  │  │ │  [🔴2]   │          │ • Proposal Alerts (High)        │  │  │  │
│  │  │ └──────────┘          │ • Security Alerts (Medium)      │  │  │  │
│  │  │                       └─────────────────────────────────┘  │  │  │
│  │  │                                                              │  │  │
│  │  │ ┌──────────┐          ┌─────────────────────────────────┐  │  │  │
│  │  │ │ Reports  │────────> │ Report Generation               │  │  │  │
│  │  │ │          │          │ • Summary Stats                 │  │  │  │
│  │  │ └──────────┘          │ • Top Users Table               │  │  │  │
│  │  │                       │ • Blocked Attempts Chart        │  │  │  │
│  │  │                       │ • [Export CSV] Button           │  │  │  │
│  │  │ ┌──────────┐          └─────────────────────────────────┘  │  │  │
│  │  │ │ Change   │────────> ┌─────────────────────────────────┐  │  │  │
│  │  │ │ Password │          │ ChangePassword Component        │  │  │  │
│  │  │ └──────────┘          └─────────────────────────────────┘  │  │  │
│  │  │                                                              │  │  │
│  │  │ ┌──────────┐          ┌─────────────────────────────────┐  │  │  │
│  │  │ │(Quick    │────────> │ Settings Review Tab             │  │  │  │
│  │  │ │ Action)  │          │ ┌─────────────────────────────┐ │  │  │  │
│  │  │ │Review    │          │ │ Proposal Card #1            │ │  │  │  │
│  │  │ │Proposals │          │ │ Admin: John Smith           │ │  │  │  │
│  │  │ └──────────┘          │ │ ┌──────────────────────────┐│ │  │  │  │
│  │  └─────────────────────  │ │ │Setting│Current│Proposed ││ │  │  │  │
│  │                           │ │ ├───────┼───────┼─────────┤│ │  │  │  │
│  └───────────────────────────│ │ │MaxCopy│  5    │   10    ││ │  │  │  │
│                               │ │ └──────────────────────────┘│ │  │  │  │
│                               │ │ [✅ Approve] [❌ Reject]     │ │  │  │  │
│                               │ └─────────────────────────────┘ │  │  │  │
│                               └─────────────────────────────────┘  │  │  │
│                                                                      │  │  │
└──────────────────────────────────────────────────────────────────────┘  │
                                                                            │
                                     ↕                                      │
                            API Calls (api.js)                             │
                                     ↕                                      │
┌───────────────────────────────────────────────────────────────────────┐ │
│                           BACKEND LAYER                                │ │
├───────────────────────────────────────────────────────────────────────┤ │
│                                                                         │ │
│  FastAPI (port 8000)                                                   │ │
│  ┌─────────────────────────────────────────────────────────────────┐  │ │
│  │  dean.py Router (/dean prefix)                                   │  │ │
│  │  ┌────────────────────────────────────────────────────────────┐ │  │ │
│  │  │ GET  /dean/overview           → Overview Stats             │ │  │ │
│  │  │ GET  /dean/settings-requests   → List Proposals            │ │  │ │
│  │  │ POST /dean/settings/approve    → Approve Proposal          │ │  │ │
│  │  │ POST /dean/settings/reject     → Reject Proposal           │ │  │ │
│  │  │ GET  /dean/notifications       → Get Notifications         │ │  │ │
│  │  │ GET  /dean/reports             → Generate Reports          │ │  │ │
│  │  └────────────────────────────────────────────────────────────┘ │  │ │
│  │                                                                   │  │ │
│  │  Authentication: verify_dean() dependency                        │  │ │
│  │  ↓ Checks Firebase Auth token                                    │  │ │
│  │  ↓ Verifies role == 'dean' in Firestore                          │  │ │
│  └─────────────────────────────────────────────────────────────────┘  │ │
│                                                                         │ │
└─────────────────────────────────────────────────────────────────────────┘
                                     ↕
                              Firebase Admin SDK
                                     ↕
┌─────────────────────────────────────────────────────────────────────────┐
│                           DATABASE LAYER                                 │
├─────────────────────────────────────────────────────────────────────────┤
│  Firestore Collections:                                                  │
│                                                                           │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────┐ │
│  │ settings_requests   │  │ system_settings     │  │ print_logs      │ │
│  ├─────────────────────┤  ├─────────────────────┤  ├─────────────────┤ │
│  │ • proposalId        │  │ • maxCopies...      │  │ • userId        │ │
│  │ • adminId/Name      │  │ • maxPrintAttempts  │  │ • timestamp     │ │
│  │ • proposedSettings  │  │ • maxPages...       │  │ • status        │ │
│  │ • currentSettings   │  │ • dailyQuota        │  │ • blocked?      │ │
│  │ • status (pending)  │  │ • allowColor...     │  └─────────────────┘ │
│  │ • submittedAt       │  │ • lastUpdated       │                      │ │
│  │ • reviewedBy        │  │ • updatedBy         │  ┌─────────────────┐ │
│  │ • reviewedAt        │  └─────────────────────┘  │ admin_actions   │ │
│  │ • deanNotes         │                           ├─────────────────┤ │
│  └─────────────────────┘  ┌─────────────────────┐  │ • type          │ │
│                            │ users               │  │ • deanId/Name   │ │
│                            ├─────────────────────┤  │ • proposalId    │ │
│                            │ EPF: 60001          │  │ • settings      │ │
│                            │ • uid               │  │ • timestamp     │ │
│                            │ • email             │  │ • details       │ │
│                            │ • name              │  └─────────────────┘ │
│                            │ • role: "dean"      │                      │ │
│                            │ • status: "active"  │                      │ │
│                            └─────────────────────┘                      │ │
└─────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                      WORKFLOW SEQUENCE DIAGRAM                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  Admin                Dean                Backend              Firestore │
│    │                   │                     │                     │      │
│    │ 1. Propose        │                     │                     │      │
│    │    Settings       │                     │                     │      │
│    │──────────────────────────────────────> │                     │      │
│    │                   │                     │ 2. Save Proposal    │      │
│    │                   │                     │ ──────────────────> │      │
│    │                   │                     │                     │      │
│    │                   │ 3. See Notification │                     │      │
│    │                   │ <────────────────── │                     │      │
│    │                   │                     │ 4. Fetch Proposals  │      │
│    │                   │ ─────────────────> │ ──────────────────> │      │
│    │                   │                     │                     │      │
│    │                   │ 5. Review Proposal  │                     │      │
│    │                   │ (See current vs     │                     │      │
│    │                   │  proposed values)   │                     │      │
│    │                   │                     │                     │      │
│    │                   │ 6. Click Approve    │                     │      │
│    │                   │ ─────────────────> │                     │      │
│    │                   │                     │ 7. Update Status    │      │
│    │                   │                     │ ──────────────────> │      │
│    │                   │                     │ 8. Update Settings  │      │
│    │                   │                     │ ──────────────────> │      │
│    │                   │                     │ 9. Log Action       │      │
│    │                   │                     │ ──────────────────> │      │
│    │                   │                     │                     │      │
│    │                   │ 10. Success Message │                     │      │
│    │                   │ <────────────────── │                     │      │
│    │                   │                     │                     │      │
│    │ 11. Settings      │                     │                     │      │
│    │     Now Active    │                     │                     │      │
│    │                   │                     │                     │      │
└─────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                        COMPONENT HIERARCHY                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  DeanDashboardUI (Root Component)                                        │
│  │                                                                        │
│  ├── Sidebar                                                             │
│  │   ├── Brand (Logo + Text)                                             │
│  │   ├── Navigation (4 buttons)                                          │
│  │   └── Logout Button                                                   │
│  │                                                                        │
│  └── Main Content                                                        │
│      ├── Header                                                          │
│      ├── Banner                                                          │
│      ├── Message (Conditional: success/error)                            │
│      │                                                                    │
│      └── Active View (Conditional Rendering)                             │
│          │                                                                │
│          ├── Overview                                                    │
│          │   └── OverviewTab (imported component)                        │
│          │       ├── Stats Cards (×4)                                    │
│          │       └── Quick Actions (×1)                                  │
│          │                                                                │
│          ├── Settings Review                                             │
│          │   └── Proposals List                                          │
│          │       └── Proposal Item (map)                                 │
│          │           ├── Header (info + actions)                         │
│          │           └── Settings Table                                  │
│          │                                                                │
│          ├── Notifications                                               │
│          │   └── Notifications List                                      │
│          │       └── Notification Item (map)                             │
│          │           ├── Icon                                            │
│          │           ├── Content                                         │
│          │           └── Badge                                           │
│          │                                                                │
│          ├── Reports                                                     │
│          │   ├── Summary Stats Section                                   │
│          │   ├── Proposal Stats Section                                  │
│          │   ├── Top Users Section                                       │
│          │   ├── Blocked Attempts Section                                │
│          │   └── Export Button                                           │
│          │                                                                │
│          └── Change Password                                             │
│              └── ChangePassword (imported component)                     │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                         STATE MANAGEMENT                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  DeanDashboardUI State:                                                  │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │ • activeView: 'overview' | 'settingsProposal' | 'notifications'│    │
│  │                | 'reports' | 'changePassword'                   │    │
│  │                                                                  │    │
│  │ • overviewStats: { todayPrintJobs, pendingProposals,           │    │
│  │                    blockedAttempts, activeUsers }               │    │
│  │                                                                  │    │
│  │ • proposals: [ { id, adminName, proposedSettings, ... } ]      │    │
│  │                                                                  │    │
│  │ • notifications: [ { id, type, title, message, ... } ]         │    │
│  │                                                                  │    │
│  │ • reports: { topUsers, proposalStats, blockedAttemptsByDay }   │    │
│  │                                                                  │    │
│  │ • loading: boolean                                              │    │
│  │                                                                  │    │
│  │ • message: { type: 'success' | 'error', text: string }         │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                           │
│  User Context (from useAuth):                                            │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │ • user: { uid, email, displayName, role }                       │    │
│  │ • logout: function                                               │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘
```

## Key Interactions

### 1. **Approval Flow:**
```
User clicks "✅ Approve" 
  → Confirmation dialog
  → API call to /dean/settings/approve
  → Backend updates Firestore (proposal + system_settings)
  → Success message displayed
  → Proposals list refreshed
  → Overview stats updated
```

### 2. **Rejection Flow:**
```
User clicks "❌ Reject"
  → Prompt for reason
  → API call to /dean/settings/reject
  → Backend updates Firestore (proposal only)
  → Success message displayed
  → Proposals list refreshed
  → Overview stats updated
```

### 3. **Export Flow:**
```
User clicks "📥 Export CSV"
  → Generate CSV content from reports data
  → Create Blob object
  → Trigger download with timestamp filename
```

## Security

- **Authentication:** Firebase Auth tokens
- **Authorization:** `verify_dean()` middleware checks role
- **Token Refresh:** Automatic via `getFreshToken()`
- **Error Handling:** Network errors, auth failures, validation errors

## Performance

- **Lazy Loading:** Data fetched only when tab is active
- **Conditional Rendering:** Only active view is rendered
- **Optimistic Updates:** UI updates before API confirmation
- **Error Recovery:** Fallback to empty states on failures
