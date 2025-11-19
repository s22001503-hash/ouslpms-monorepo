# Dashboard Navigation & Features Map

## 🎯 VC Dashboard (Vice Chancellor)

```
┌─────────────────────────────────────────────────────────────┐
│                    VC DASHBOARD - EcoPrint                   │
│                  dean@ousl.lk / Dean123456                   │
└─────────────────────────────────────────────────────────────┘

├─ 🏠 Overview
│  ├─ Metrics Cards:
│  │  ├─ 🖨️ Print Jobs Today (247)
│  │  ├─ ⏳ Pending Approvals (12) ← CLICKABLE
│  │  ├─ 🌳 Paper Saved (1,235 sheets) ← NEW
│  │  ├─ 🚫 Blocked Attempts (45)
│  │  └─ 👥 Active Users (156)
│  └─ Quick Actions:
│     ├─ 📋 Review Print Requests → ApprovalRequests
│     └─ ⚙️ Review Policy Changes → PolicyManagement
│
├─ 📋 Approval Requests ← NEW TAB
│  ├─ Filter Tabs: Pending | Approved | Rejected | All
│  ├─ Request Cards:
│  │  ├─ User: John Doe (EPF: 10234)
│  │  ├─ Document: Research_Paper.pdf
│  │  ├─ Classification: 🟢 Official / 🔴 Personal / 🟡 Confidential
│  │  ├─ Block Reason: Daily limit exceeded / Copy limit exceeded
│  │  ├─ Justification: (user's reason)
│  │  └─ Actions: ✅ Approve | ❌ Reject
│  └─ Decision History:
│     └─ Shows your past approvals/rejections
│
├─ ⚙️ Policy Management ← NEW TAB
│  ├─ Filter Tabs: Pending | Approved | Rejected | All
│  ├─ Proposal Cards:
│  │  ├─ Admin: Admin User (EPF: 50001)
│  │  ├─ Proposed Changes:
│  │  │  └─ User Daily Limit: 10 → 12
│  │  ├─ Justification: (admin's reason)
│  │  └─ Actions: ✅ Approve Changes | ❌ Reject Changes
│  └─ Review Interface:
│     └─ Add notes for decision
│
├─ 🖨️ Print Document
│  ├─ File Upload (drag & drop)
│  ├─ AI Classification Preview
│  ├─ VC Policy Check (20 pages/day, 20 copies, NO personal)
│  └─ Confirm & Print
│
├─ 🔔 Notifications
│  └─ (Placeholder)
│
├─ 📊 Generate Report
│  └─ (Placeholder)
│
└─ 🔒 Change Password
   └─ Secure password update

```

---

## 🛠️ Admin Dashboard (Administrator)

```
┌─────────────────────────────────────────────────────────────┐
│                  ADMIN DASHBOARD - EcoPrint                  │
└─────────────────────────────────────────────────────────────┘

├─ 🏠 Overview
│  ├─ Metrics Cards:
│  │  ├─ 🖨️ Print Jobs Today (247)
│  │  ├─ ⏳ Pending Proposals (3)
│  │  ├─ 🚫 Blocked Attempts (45)
│  │  └─ 👥 Active Users (156)
│  └─ Quick Actions:
│     ├─ 👤➕ Add User
│     ├─ 👤➖ Remove User
│     └─ ⚙️ Propose Settings
│
├─ 📝 Policy Proposals ← NEW TAB
│  ├─ Current Policies:
│  │  ├─ User Daily Limit: 10 pages
│  │  ├─ User Max Copies: 5
│  │  ├─ Staff Daily Limit: 15 pages
│  │  ├─ VC Daily Limit: 20 pages
│  │  ├─ Allow Personal Docs: No
│  │  ├─ Max File Size: 10 MB
│  │  └─ Auto-block Threshold: 3 violations
│  ├─ Proposal Form:
│  │  ├─ Select Policy to Change
│  │  ├─ Current Value → Proposed Value
│  │  ├─ Justification (required)
│  │  └─ Submit to VC
│  └─ Pending Proposals:
│     ├─ Proposal #1: Pending VC approval
│     ├─ Proposal #2: ✅ Approved by VC
│     └─ Proposal #3: ❌ Rejected by VC
│
├─ 📊 System Analytics ← NEW TAB
│  ├─ Key Metrics:
│  │  ├─ Today's Prints: 247
│  │  ├─ Paper Saved: 1,235 sheets
│  │  ├─ Blocked Attempts: 45
│  │  └─ Active Users: 156
│  ├─ System Health:
│  │  ├─ Overall Status: 🟢 Healthy
│  │  ├─ AI Service: 🟢 Online
│  │  └─ Printers: 8/10 online
│  ├─ Block Reasons Chart:
│  │  ├─ Personal Documents: 45% ██████████
│  │  ├─ Daily Limit: 35% ████████
│  │  └─ Copy Limit: 20% █████
│  ├─ Top 5 Users:
│  │  ├─ 1. John Doe - 89 prints (CS Dept)
│  │  ├─ 2. Jane Smith - 76 prints (Eng Dept)
│  │  └─ ...
│  ├─ Recent Activity Feed:
│  │  ├─ John Doe printed Lecture_Notes.pdf (✅ Success)
│  │  ├─ Alice Brown blocked - Personal document (🚫 Blocked)
│  │  └─ ...
│  ├─ Auto-refresh Toggle (30s)
│  └─ Export Buttons:
│     ├─ 📥 Export Daily Report
│     ├─ 📥 Export Weekly Report
│     └─ 📥 Export by Department
│
├─ 🖨️ Print Document
│  └─ (Same as VC)
│
├─ 🔔 Notifications
│  └─ (Placeholder)
│
├─ 📊 Generate Report
│  └─ (Placeholder)
│
└─ 🔒 Change Password
   └─ Secure password update

```

---

## 🔄 Workflow Diagrams

### **User Print Request → VC Approval Flow**

```
┌──────────┐
│   USER   │
└────┬─────┘
     │
     │ 1. Upload document
     ▼
┌─────────────────┐
│  AI Classifier  │
│  (Pinecone+Groq)│
└────┬────────────┘
     │
     │ 2. Classify as Personal/Official/Confidential
     ▼
┌─────────────────┐
│ Policy Engine   │
│ Check Limits    │
└────┬────────────┘
     │
     ├─ ✅ Within limits → Print immediately
     │
     ├─ ⚠️ Daily limit exceeded → Request VC approval
     │
     ├─ ⚠️ Copy limit exceeded → Request VC approval
     │
     └─ 🚫 Personal document → HARD BLOCK
          │
          ▼
     ┌─────────────────┐
     │  VC Dashboard   │
     │ Approval Queue  │
     └────┬────────────┘
          │
          │ 3. VC reviews request
          ▼
     ┌──────┬──────┐
     │ ✅   │  ❌  │
     │Approve│Reject│
     └──┬───┴───┬──┘
        │       │
        │       │ 4. Notify user
        ▼       ▼
    ┌─────┐ ┌──────┐
    │Print│ │Cancel│
    └─────┘ └──────┘
```

### **Admin Policy Proposal → VC Approval Flow**

```
┌──────────┐
│  ADMIN   │
└────┬─────┘
     │
     │ 1. Propose policy change
     ▼
┌─────────────────────┐
│ Policy Proposal Tab │
│ - Current: 10 pages │
│ - Proposed: 12 pages│
│ - Justification     │
└────┬────────────────┘
     │
     │ 2. Submit to VC
     ▼
┌─────────────────────┐
│   VC Dashboard      │
│ Policy Management   │
└────┬────────────────┘
     │
     │ 3. VC reviews proposal
     ▼
┌──────┬──────┐
│ ✅   │  ❌  │
│Approve│Reject│
└──┬───┴───┬──┘
   │       │
   │       │ 4. Update system / Notify admin
   ▼       ▼
┌──────┐ ┌──────┐
│Update│ │Deny  │
│Policy│ │Change│
└──────┘ └──────┘
```

---

## 📊 Data Flow Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  VC Dashboard              Admin Dashboard              │
│  ├─ OverviewTab            ├─ OverviewTab               │
│  ├─ ApprovalRequestsTab    ├─ PolicyProposalTab         │
│  ├─ PolicyManagementTab    ├─ SystemAnalyticsTab        │
│  └─ PrintDocument          └─ PrintDocument             │
│                                                          │
└─────────────┬───────────────────────────────────────────┘
              │
              │ API Calls (api.js)
              ▼
┌─────────────────────────────────────────────────────────┐
│                  API SERVICE LAYER                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Policy Management:                                      │
│  ├─ proposePolicyChange()                               │
│  ├─ getPolicyProposals()                                │
│  ├─ approvePolicyProposal()                             │
│  └─ rejectPolicyProposal()                              │
│                                                          │
│  Approval Requests:                                      │
│  ├─ getApprovalRequests()                               │
│  ├─ approveUserRequest()                                │
│  └─ rejectUserRequest()                                 │
│                                                          │
│  System Analytics:                                       │
│  ├─ getSystemMetrics()                                  │
│  └─ exportReport()                                      │
│                                                          │
└─────────────┬───────────────────────────────────────────┘
              │
              │ HTTP Requests
              ▼
┌─────────────────────────────────────────────────────────┐
│              BACKEND (FastAPI - To be implemented)       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Endpoints:                                              │
│  ├─ POST /admin/propose-policy                          │
│  ├─ GET  /vc/policy-proposals                           │
│  ├─ POST /vc/policy-proposals/approve                   │
│  ├─ POST /vc/policy-proposals/reject                    │
│  ├─ GET  /vc/approval-requests                          │
│  ├─ POST /vc/approval-requests/approve                  │
│  ├─ POST /vc/approval-requests/reject                   │
│  ├─ GET  /admin/system-metrics                          │
│  └─ POST /admin/export-report                           │
│                                                          │
└─────────────┬───────────────────────────────────────────┘
              │
              │ Database Operations
              ▼
┌─────────────────────────────────────────────────────────┐
│                 FIREBASE FIRESTORE                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Collections:                                            │
│  ├─ policyProposals/                                    │
│  │  └─ {proposalId}                                     │
│  │     ├─ adminId                                       │
│  │     ├─ changes[]                                     │
│  │     ├─ justification                                 │
│  │     ├─ status (pending/approved/rejected)            │
│  │     └─ vcDecision{notes, decidedAt}                 │
│  │                                                       │
│  ├─ approvalRequests/                                   │
│  │  └─ {requestId}                                      │
│  │     ├─ userId                                        │
│  │     ├─ document{name, size, classification}          │
│  │     ├─ blockReason                                   │
│  │     ├─ justification                                 │
│  │     ├─ status (pending/approved/rejected)            │
│  │     └─ vcDecision{notes, decidedAt}                 │
│  │                                                       │
│  └─ systemMetrics/                                      │
│     └─ daily/{date}                                     │
│        ├─ todayPrints                                   │
│        ├─ paperSaved                                    │
│        ├─ blockedAttempts                               │
│        ├─ activeUsers                                   │
│        └─ blockReasons{}                                │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🎨 Component Hierarchy

```
App
│
├─ Login
│
├─ UserDashboard
│  ├─ PrintWorkflow ← NEW COMPONENT
│  │  ├─ ClassificationBadge
│  │  └─ File Upload UI
│  └─ Notifications (enhanced with VC decisions)
│
├─ VCDashboard (DeanDashboardUI)
│  ├─ OverviewTab (role="vc")
│  ├─ ApprovalRequestsTab ← NEW
│  │  └─ ClassificationBadge
│  ├─ PolicyManagementTab ← NEW
│  ├─ PrintDocument
│  └─ ChangePassword
│
└─ AdminDashboard
   ├─ OverviewTab (role="admin")
   ├─ PolicyProposalTab ← NEW
   ├─ SystemAnalyticsTab ← NEW
   ├─ SettingsProposalTab (legacy)
   ├─ AddUser
   ├─ RemoveUser
   ├─ PrintDocument
   └─ ChangePassword
```

---

## 🔑 Key Features by Role

### **User Role:**
- Upload documents
- AI-powered classification
- Automatic policy checks
- Request VC approval when needed
- View VC decisions on requests

### **VC Role:**
- Review user print requests
- Approve/reject with notes
- Review admin policy proposals
- Approve/reject policy changes
- Monitor paper savings
- Higher print privileges (20 pages/day, 20 copies)

### **Admin Role:**
- Propose policy changes
- View system analytics in real-time
- Monitor top users
- Track block reasons
- Export reports
- Add/remove users
- Manage system settings

---

## 📈 Metrics Tracked

### **Real-time Metrics:**
- Today's Prints
- Paper Saved (sheets)
- Blocked Attempts
- Active Users
- System Health Status
- AI Service Status
- Printers Online/Offline

### **Analytics:**
- Block Reasons Distribution
- Top 5 Users by Prints
- Recent Activity Feed
- Department-wise Usage
- Daily/Weekly Trends

### **Exportable Reports:**
- Daily Print Report
- Weekly Summary
- Department Breakdown
- User Activity Logs
- Policy Change History

---

This visualization shows the complete structure and data flow of the enhanced EcoPrint system! 🚀
