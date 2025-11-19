# SQLite REST API - Quick Reference
**OUSL Print Management System**

---

## 🔗 Base URL
```
http://localhost:8001
```

## 🔑 Authentication
All `/api/*` endpoints require API key in header:
```
X-API-Key: ousl-sqlite-api-key-2025
```

---

## 📡 Endpoints

### 1. Health Check
**No authentication required**

```http
GET /
```

**Response:**
```json
{
  "status": "online",
  "message": "OUSL Print Management - SQLite API Server",
  "database": "C:\\AI_Prints\\job_queue.db",
  "database_exists": true,
  "record_count": 42
}
```

---

### 2. Classification History
Get classification records with optional filters.

```http
GET /api/classification-history?user_id={user}&limit={limit}&offset={offset}
```

**Parameters:**
- `user_id` (optional): Filter by user ID
- `classification` (optional): Filter by classification (office, personal, confidential)
- `action` (optional): Filter by action (allow, block)
- `limit` (optional): Max records (default: 100)
- `offset` (optional): Skip records (for pagination)

**Response:**
```json
[
  {
    "id": 1,
    "job_id": "job_20250129_143022_abc123",
    "user_id": "99999",
    "file_name": "report.pdf",
    "file_hash": "d4f5e6a7b8c9...",
    "classification": "office",
    "action": "allow",
    "reason": "Official document within daily limit (1/3)",
    "copies": 1,
    "executive_summary": {...},
    "timestamp": "2025-01-29T14:30:22",
    "synced_to_firestore": 0
  }
]
```

---

### 3. Daily Statistics
Get statistics for specific user on specific date.

```http
GET /api/daily-stats?user_id={user_id}&date={YYYY-MM-DD}
```

**Parameters:**
- `user_id` (required): User ID
- `date` (required): Date in YYYY-MM-DD format

**Response:**
```json
{
  "user_id": "99999",
  "date": "2025-01-29",
  "total_attempts": 10,
  "allowed": 7,
  "blocked": 3,
  "by_classification": {
    "office": 6,
    "personal": 3,
    "confidential": 1
  },
  "by_action": {
    "allow": 7,
    "block": 3
  }
}
```

---

### 4. Search
Search classification history by keyword.

```http
GET /api/search?query={keyword}&field={field}&limit={limit}
```

**Parameters:**
- `query` (required): Search keyword
- `field` (required): Field to search (`file_name`, `classification`, `user_id`, `action`)
- `limit` (optional): Max results (default: 100)

**Response:**
```json
{
  "query": "personal",
  "field": "classification",
  "count": 3,
  "results": [
    {
      "id": 5,
      "classification": "personal",
      "action": "block",
      ...
    }
  ]
}
```

---

### 5. Summary Statistics
Get overall database statistics.

```http
GET /api/stats/summary
```

**Response:**
```json
{
  "total_records": 42,
  "unique_users": 5,
  "classification_breakdown": {
    "office": 25,
    "personal": 12,
    "confidential": 5
  },
  "action_breakdown": {
    "allow": 30,
    "block": 12
  }
}
```

---

### 6. Users List
Get list of all users with their statistics.

```http
GET /api/users?limit={limit}
```

**Parameters:**
- `limit` (optional): Max users (default: 100)

**Response:**
```json
[
  {
    "user_id": "99999",
    "total_prints": 15,
    "allowed": 10,
    "blocked": 5,
    "last_print": "2025-01-29T14:30:22"
  }
]
```

---

## 💻 PowerShell Examples

### Health Check
```powershell
Invoke-WebRequest -Uri "http://localhost:8001/" | Select-Object -ExpandProperty Content
```

### Get Classification History
```powershell
$headers = @{ "X-API-Key" = "ousl-sqlite-api-key-2025" }
Invoke-WebRequest -Uri "http://localhost:8001/api/classification-history?limit=10" -Headers $headers | Select-Object -ExpandProperty Content
```

### Get Daily Stats for User
```powershell
$headers = @{ "X-API-Key" = "ousl-sqlite-api-key-2025" }
$today = (Get-Date).ToString("yyyy-MM-dd")
Invoke-WebRequest -Uri "http://localhost:8001/api/daily-stats?user_id=99999&date=$today" -Headers $headers | Select-Object -ExpandProperty Content
```

### Search by Classification
```powershell
$headers = @{ "X-API-Key" = "ousl-sqlite-api-key-2025" }
Invoke-WebRequest -Uri "http://localhost:8001/api/search?query=personal&field=classification" -Headers $headers | Select-Object -ExpandProperty Content
```

### Get Summary Statistics
```powershell
$headers = @{ "X-API-Key" = "ousl-sqlite-api-key-2025" }
Invoke-WebRequest -Uri "http://localhost:8001/api/stats/summary" -Headers $headers | Select-Object -ExpandProperty Content
```

### Get Users List
```powershell
$headers = @{ "X-API-Key" = "ousl-sqlite-api-key-2025" }
Invoke-WebRequest -Uri "http://localhost:8001/api/users" -Headers $headers | Select-Object -ExpandProperty Content
```

---

## 🌐 cURL Examples

### Health Check
```bash
curl http://localhost:8001/
```

### Get Classification History
```bash
curl -H "X-API-Key: ousl-sqlite-api-key-2025" \
  "http://localhost:8001/api/classification-history?limit=10"
```

### Get Daily Stats
```bash
curl -H "X-API-Key: ousl-sqlite-api-key-2025" \
  "http://localhost:8001/api/daily-stats?user_id=99999&date=$(date +%Y-%m-%d)"
```

### Search
```bash
curl -H "X-API-Key: ousl-sqlite-api-key-2025" \
  "http://localhost:8001/api/search?query=personal&field=classification"
```

### Get Summary Stats
```bash
curl -H "X-API-Key: ousl-sqlite-api-key-2025" \
  "http://localhost:8001/api/stats/summary"
```

### Get Users
```bash
curl -H "X-API-Key: ousl-sqlite-api-key-2025" \
  "http://localhost:8001/api/users"
```

---

## 🔧 TypeScript/JavaScript Examples

### Using agentApiClient Service

```typescript
import { agentApiClient } from '@/services/agentApi';

// Health Check
const health = await agentApiClient.healthCheck();
console.log(health.status); // "online"

// Get Classification History
const history = await agentApiClient.getClassificationHistory({
  userId: '99999',
  limit: 50,
  offset: 0
});

// Get Daily Statistics
const today = new Date().toISOString().split('T')[0];
const stats = await agentApiClient.getDailyStats('99999', today);
console.log(`Allowed: ${stats.allowed}, Blocked: ${stats.blocked}`);

// Search
const searchResults = await agentApiClient.search('personal', 'classification');
console.log(`Found ${searchResults.count} records`);

// Get Summary Stats
const summary = await agentApiClient.getSummaryStats();
console.log(`Total records: ${summary.total_records}`);

// Get Users
const users = await agentApiClient.getUsers(20);
users.forEach(user => {
  console.log(`${user.user_id}: ${user.total_prints} prints`);
});
```

### Using Fetch API Directly

```javascript
const API_KEY = 'ousl-sqlite-api-key-2025';
const BASE_URL = 'http://localhost:8001';

// Helper function
async function apiRequest(endpoint) {
  const response = await fetch(`${BASE_URL}${endpoint}`, {
    headers: { 'X-API-Key': API_KEY }
  });
  return response.json();
}

// Get classification history
const history = await apiRequest('/api/classification-history?limit=10');

// Get daily stats
const stats = await apiRequest('/api/daily-stats?user_id=99999&date=2025-01-29');

// Search
const results = await apiRequest('/api/search?query=personal&field=classification');
```

---

## 🚦 Status Codes

| Code | Meaning | Cause |
|------|---------|-------|
| 200 | OK | Request successful |
| 401 | Unauthorized | Invalid or missing API key |
| 404 | Not Found | Endpoint doesn't exist |
| 500 | Internal Server Error | Database error or server issue |

---

## 🔐 Security Notes

- **API Key**: Stored in `sqlite_api_server.py` line 25
- **Change in production**: Update API_KEY constant
- **CORS**: Enabled for localhost:5173, 5174, 3000
- **Add origin**: Modify CORS middleware in server code

---

## 📊 Database Schema

### classification_history Table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Auto-increment primary key |
| job_id | TEXT | Unique job identifier |
| user_id | TEXT | User ID (e.g., "99999") |
| file_name | TEXT | Original filename |
| file_hash | TEXT | SHA256 hash of file |
| classification | TEXT | AI classification result |
| action | TEXT | "allow" or "block" |
| reason | TEXT | Detailed reason for action |
| copies | INTEGER | Number of copies requested |
| executive_summary | TEXT | JSON executive summary |
| timestamp | TIMESTAMP | When classification occurred |
| synced_to_firestore | INTEGER | 0 = not synced, 1 = synced |

### Indexes
- `idx_file_hash` on file_hash
- `idx_user_timestamp` on (user_id, timestamp)
- `idx_classification` on (classification, action)

---

## 🛠️ Start Server

```powershell
cd "c:\Users\user\Desktop\OCT Project\ouslpms-monorepo\backend"
python sqlite_api_server.py
```

Press `Ctrl+C` to stop.

---

## 📚 Related Documentation

- **Full Testing Guide**: `TESTING_GUIDE.md`
- **Sprint 5 Documentation**: `SPRINT5_FIRESTORE_POLICIES.md`
- **TypeScript Service**: `frontend/src/services/agentApi.ts`
- **React Component**: `frontend/src/components/AgentPrintHistory.tsx`

---

**Quick Reference Card - Last Updated: January 29, 2025**
