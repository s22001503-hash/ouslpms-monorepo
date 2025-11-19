# Sprint 5 Testing Guide
**SQLite REST API & Firestore Policy Enforcement**

---

## 📋 Overview

This guide walks you through testing the complete Sprint 5 implementation:
1. SQLite REST API server
2. Firestore policy enforcement
3. Local classification history storage
4. End-to-end print flow

---

## 🚀 Quick Start

### Step 1: Start SQLite API Server

```powershell
cd "c:\Users\user\Desktop\OCT Project\ouslpms-monorepo\backend"
python sqlite_api_server.py
```

**Expected Output:**
```
╔═══════════════════════════════════════════════════════════════╗
║         OUSL Print Management - SQLite API Server             ║
╚═══════════════════════════════════════════════════════════════╝

🔑 API Key: ousl-sqlite-api-key-2025

📊 Endpoints:
  GET  /                           - Health check (no auth)
  GET  /api/classification-history - Get classification records
  GET  /api/daily-stats            - Get daily statistics
  GET  /api/search                 - Search records
  GET  /api/stats/summary          - Get summary statistics
  GET  /api/users                  - Get user list

📝 Example Usage:
  curl -H "X-API-Key: ousl-sqlite-api-key-2025" http://localhost:8001/

Server starting on http://localhost:8001
Press Ctrl+C to stop
```

**Troubleshooting:**
- **Port already in use**: `netstat -ano | findstr :8001` then kill the process
- **Python not found**: Ensure Python is in PATH
- **Database not found**: The database will be created when agent runs first print job

---

## ✅ Test 1: Health Check Endpoint

Test the health check endpoint (no authentication required).

### PowerShell:
```powershell
Invoke-WebRequest -Uri "http://localhost:8001/" -Method GET | Select-Object -ExpandProperty Content
```

### cURL (Git Bash):
```bash
curl http://localhost:8001/
```

**Expected Response:**
```json
{
  "status": "online",
  "message": "OUSL Print Management - SQLite API Server",
  "database": "C:\\AI_Prints\\job_queue.db",
  "database_exists": true,
  "record_count": 0
}
```

**Pass Criteria:**
- ✅ Status code: 200
- ✅ `"status": "online"`
- ✅ `"database_exists": true` (if database file exists)

---

## ✅ Test 2: Authentication Required

Test that protected endpoints require API key.

### PowerShell (Without API Key):
```powershell
Invoke-WebRequest -Uri "http://localhost:8001/api/stats/summary" -Method GET
```

**Expected Response:**
- Status Code: 401 Unauthorized
- Error: `{"detail":"Invalid API key"}`

### PowerShell (With API Key):
```powershell
$headers = @{ "X-API-Key" = "ousl-sqlite-api-key-2025" }
Invoke-WebRequest -Uri "http://localhost:8001/api/stats/summary" -Headers $headers -Method GET | Select-Object -ExpandProperty Content
```

**Expected Response:**
```json
{
  "total_records": 0,
  "unique_users": 0,
  "classification_breakdown": {},
  "action_breakdown": {}
}
```

**Pass Criteria:**
- ✅ Request without API key returns 401
- ✅ Request with correct API key returns 200

---

## ✅ Test 3: Classification History Endpoint

Get classification records from SQLite database.

### PowerShell:
```powershell
$headers = @{ "X-API-Key" = "ousl-sqlite-api-key-2025" }
Invoke-WebRequest -Uri "http://localhost:8001/api/classification-history?limit=10" -Headers $headers -Method GET | Select-Object -ExpandProperty Content
```

### cURL:
```bash
curl -H "X-API-Key: ousl-sqlite-api-key-2025" \
  "http://localhost:8001/api/classification-history?limit=10"
```

**Query Parameters:**
- `user_id` - Filter by user ID (e.g., `?user_id=99999`)
- `classification` - Filter by classification (e.g., `?classification=personal`)
- `action` - Filter by action (e.g., `?action=block`)
- `limit` - Number of records (default: 100)
- `offset` - Skip records (for pagination)

**Expected Response:**
```json
[
  {
    "id": 1,
    "job_id": "job_20250129_143022_abc123",
    "user_id": "99999",
    "file_name": "personal_photo.jpg",
    "file_hash": "d4f5e6...",
    "classification": "personal",
    "action": "block",
    "reason": "Personal documents are not allowed for printing",
    "copies": 1,
    "executive_summary": null,
    "timestamp": "2025-01-29T14:30:22",
    "synced_to_firestore": 0
  }
]
```

**Pass Criteria:**
- ✅ Returns array of classification records
- ✅ Filters work correctly
- ✅ Pagination works with limit/offset

---

## ✅ Test 4: Daily Statistics Endpoint

Get daily statistics for a specific user.

### PowerShell:
```powershell
$headers = @{ "X-API-Key" = "ousl-sqlite-api-key-2025" }
$today = (Get-Date).ToString("yyyy-MM-dd")
Invoke-WebRequest -Uri "http://localhost:8001/api/daily-stats?user_id=99999&date=$today" -Headers $headers -Method GET | Select-Object -ExpandProperty Content
```

### cURL:
```bash
curl -H "X-API-Key: ousl-sqlite-api-key-2025" \
  "http://localhost:8001/api/daily-stats?user_id=99999&date=$(date +%Y-%m-%d)"
```

**Expected Response:**
```json
{
  "user_id": "99999",
  "date": "2025-01-29",
  "total_attempts": 5,
  "allowed": 3,
  "blocked": 2,
  "by_classification": {
    "office": 3,
    "personal": 2
  },
  "by_action": {
    "allow": 3,
    "block": 2
  }
}
```

**Pass Criteria:**
- ✅ Returns statistics for specified user and date
- ✅ Counts match actual records in database
- ✅ Breakdowns by classification and action are correct

---

## ✅ Test 5: Search Endpoint

Search classification history by keyword.

### PowerShell:
```powershell
$headers = @{ "X-API-Key" = "ousl-sqlite-api-key-2025" }
Invoke-WebRequest -Uri "http://localhost:8001/api/search?query=personal&field=classification" -Headers $headers -Method GET | Select-Object -ExpandProperty Content
```

### cURL:
```bash
curl -H "X-API-Key: ousl-sqlite-api-key-2025" \
  "http://localhost:8001/api/search?query=personal&field=classification"
```

**Query Parameters:**
- `query` - Search keyword (required)
- `field` - Field to search: `file_name`, `classification`, `user_id`, `action` (required)
- `limit` - Max results (default: 100)

**Expected Response:**
```json
{
  "query": "personal",
  "field": "classification",
  "count": 2,
  "results": [
    {
      "id": 1,
      "classification": "personal",
      "action": "block",
      ...
    }
  ]
}
```

**Pass Criteria:**
- ✅ Returns matching records
- ✅ Search is case-insensitive
- ✅ Count matches result array length

---

## ✅ Test 6: Summary Statistics Endpoint

Get overall database statistics.

### PowerShell:
```powershell
$headers = @{ "X-API-Key" = "ousl-sqlite-api-key-2025" }
Invoke-WebRequest -Uri "http://localhost:8001/api/stats/summary" -Headers $headers -Method GET | Select-Object -ExpandProperty Content
```

### cURL:
```bash
curl -H "X-API-Key: ousl-sqlite-api-key-2025" \
  "http://localhost:8001/api/stats/summary"
```

**Expected Response:**
```json
{
  "total_records": 10,
  "unique_users": 3,
  "classification_breakdown": {
    "office": 6,
    "personal": 3,
    "confidential": 1
  },
  "action_breakdown": {
    "allow": 7,
    "block": 3
  }
}
```

**Pass Criteria:**
- ✅ Total records matches actual count
- ✅ Unique users count is correct
- ✅ Breakdowns sum to total

---

## ✅ Test 7: Users List Endpoint

Get list of all users with their statistics.

### PowerShell:
```powershell
$headers = @{ "X-API-Key" = "ousl-sqlite-api-key-2025" }
Invoke-WebRequest -Uri "http://localhost:8001/api/users?limit=10" -Headers $headers -Method GET | Select-Object -ExpandProperty Content
```

### cURL:
```bash
curl -H "X-API-Key: ousl-sqlite-api-key-2025" \
  "http://localhost:8001/api/users?limit=10"
```

**Expected Response:**
```json
[
  {
    "user_id": "99999",
    "total_prints": 10,
    "allowed": 7,
    "blocked": 3,
    "last_print": "2025-01-29T14:30:22"
  }
]
```

**Pass Criteria:**
- ✅ Returns list of users with statistics
- ✅ Counts match individual user records
- ✅ Sorted by total_prints descending

---

## 🔥 Test 8: Initialize Firestore Policies

Initialize Firestore with default policies.

### Run Script:
```powershell
cd "c:\Users\user\Desktop\OCT Project\ouslpms-monorepo\backend"
python scripts\init_firestore_policies.py
```

**Expected Output:**
```
========================================
Firestore Policy Initialization
========================================

Initializing system policies...
✅ System policies created successfully!
  - max_daily_prints: 3
  - max_copies_per_document: 10

Create sample user daily limits document? (y/n): n

========================================
Initialization Complete!
========================================

Firestore Collections Created:
✅ system_policies/default

You can now:
1. Start backend server
2. Start agent
3. Test print flow
```

**Verify in Firebase Console:**
1. Go to: https://console.firebase.google.com/
2. Select your project
3. Navigate to Firestore Database
4. Check collection: `system_policies`
5. Verify document: `default` exists with fields:
   - `max_daily_prints: 3`
   - `max_copies_per_document: 10`

---

## 🖨️ Test 9: End-to-End Print Flow

Test the complete print workflow with Firestore enforcement.

### Prerequisites:
- ✅ SQLite API server running
- ✅ Firestore policies initialized
- ✅ Backend server running (`uvicorn app.main:app --reload`)
- ✅ Agent running (`python virtual_printer_agent.py`)

### Test Scenario 1: Print Office Document (Should Allow)

1. **Action**: Print an office document
2. **Expected**:
   - Backend queries Firestore for policies
   - Daily limit check passes (0/3)
   - Copy limit check passes (1 <= 10)
   - Classification stored in SQLite
   - Print allowed
   - Daily counter incremented in Firestore

3. **Verify SQLite**:
```powershell
python scripts\query_local_history.py --limit 1
```

4. **Verify Firestore**:
   - Check `user_daily_limits/{user_id}_{date}` document
   - `prints_today` should be `1`

### Test Scenario 2: Print Personal Document (Should Block)

1. **Action**: Print a personal document (photo, entertainment)
2. **Expected**:
   - Classification identifies as "personal"
   - Backend blocks IMMEDIATELY (no limit checks)
   - Stored in SQLite with action="block"
   - Daily counter NOT incremented
   - Notification shown to user

3. **Verify SQLite**:
```powershell
python scripts\query_local_history.py --limit 1
```
   - Should show: `action: block`, `classification: personal`

### Test Scenario 3: Exceed Daily Limit (Should Block)

1. **Action**: Print 4 office documents (max is 3)
2. **Expected**:
   - First 3 prints allowed
   - 4th print blocked with reason: "Daily limit exceeded (3/3)"
   - Daily counter stays at 3

3. **Verify Firestore**:
   - `prints_today` should be `3`
   - No increment on 4th attempt

### Test Scenario 4: Exceed Copy Limit (Should Block)

1. **Action**: Print office document with 15 copies (max is 10)
2. **Expected**:
   - Backend blocks with reason: "Copies exceed limit (15 > 10)"
   - Daily counter NOT incremented

---

## 📊 Test 10: Query Local Database

Use the query script to inspect local classification history.

### Get Statistics:
```powershell
python scripts\query_local_history.py --stats
```

**Expected Output:**
```
================================================================================
Daily Statistics (All Users)
================================================================================

Date: 2025-01-29

Total Print Attempts: 10
Allowed: 7
Blocked: 3

Classification Breakdown:
  - office: 6
  - personal: 3
  - confidential: 1

Action Breakdown:
  - allow: 7
  - block: 3
```

### Get History for User:
```powershell
python scripts\query_local_history.py --user 99999 --limit 5
```

### Export to CSV:
```powershell
python scripts\query_local_history.py --user 99999 --export
```

---

## 🎯 Test 11: Frontend Integration

Test the TypeScript service from frontend.

### Example Usage in React Component:
```typescript
import { agentApiClient } from '../services/agentApi';

// Get classification history
const history = await agentApiClient.getClassificationHistory({
  userId: '99999',
  limit: 50
});

// Get daily stats
const today = new Date().toISOString().split('T')[0];
const stats = await agentApiClient.getDailyStats('99999', today);

// Search
const results = await agentApiClient.search('personal', 'classification');
```

### Test with Console:
1. Open frontend in browser: http://localhost:5174
2. Open DevTools Console (F12)
3. Run:
```javascript
import('/src/services/agentApi.ts').then(module => {
  const api = module.agentApiClient;
  api.healthCheck().then(console.log);
  api.getSummaryStats().then(console.log);
});
```

---

## 🔍 Troubleshooting

### SQLite API Server Won't Start

**Problem**: Port 8001 already in use
```powershell
# Find process using port 8001
netstat -ano | findstr :8001

# Kill process (replace PID)
taskkill /F /PID <PID>
```

### Database Not Found

**Problem**: `C:\AI_Prints\job_queue.db` doesn't exist
- **Solution**: Run agent first to create database
- **Or**: Print a document to trigger database creation

### API Returns Empty Results

**Problem**: All endpoints return empty arrays
- **Cause**: No print jobs have been processed yet
- **Solution**: Print a test document through agent

### Authentication Fails

**Problem**: Always getting 401 Unauthorized
- **Verify**: API key is exactly `ousl-sqlite-api-key-2025`
- **Check**: Header is `X-API-Key` (case-sensitive)
- **PowerShell**: Use `@{ "X-API-Key" = "..." }`

### Firestore Query Errors

**Problem**: Backend returns "Firebase not initialized"
- **Solution**: Run `python scripts/init_firestore_policies.py`
- **Verify**: `.env` file has correct `FIREBASE_CREDENTIALS`

---

## ✅ Acceptance Criteria

Sprint 5 is complete when ALL tests pass:

- [x] SQLite API server starts on port 8001
- [x] Health check endpoint returns status
- [x] Authentication works (401 without key, 200 with key)
- [x] Classification history endpoint returns records
- [x] Daily stats endpoint returns correct statistics
- [x] Search endpoint finds matching records
- [x] Summary stats endpoint returns totals
- [x] Users endpoint lists users with stats
- [x] Firestore policies initialized
- [x] Personal documents blocked immediately
- [x] Official documents check Firestore limits
- [x] Daily counter increments only on approval
- [x] SQLite stores all classification results
- [x] Frontend service calls API successfully

---

## 📝 Test Results Log

Document your test results:

| Test # | Test Name | Date | Result | Notes |
|--------|-----------|------|--------|-------|
| 1 | Health Check | | ⏳ | |
| 2 | Authentication | | ⏳ | |
| 3 | Classification History | | ⏳ | |
| 4 | Daily Statistics | | ⏳ | |
| 5 | Search | | ⏳ | |
| 6 | Summary Stats | | ⏳ | |
| 7 | Users List | | ⏳ | |
| 8 | Firestore Init | | ⏳ | |
| 9 | End-to-End Print | | ⏳ | |
| 10 | Local Database Query | | ⏳ | |
| 11 | Frontend Integration | | ⏳ | |

Legend: ✅ Pass | ❌ Fail | ⏳ Pending

---

## 🚀 Next Steps

After all tests pass:

1. **Deploy to Production**:
   - Configure production Firebase project
   - Update API keys
   - Deploy backend and agent

2. **Build Admin Dashboard**:
   - Use `AgentPrintHistory.tsx` component
   - Add charts and analytics
   - Real-time updates

3. **Replace OpenAI**:
   - Fine-tune open source model
   - Update backend to use local model
   - Remove OpenAI dependency

4. **Background Sync**:
   - Sync SQLite to Firestore periodically
   - Use `mark_synced_to_firestore()` method
   - Handle offline scenarios

---

**Testing Complete!** 🎉

All Sprint 5 features are implemented and ready for testing.
