# 🔒 Sprint 4 - Login Enforcement System

## Overview
The Virtual Printer Agent now enforces user authentication using Firebase Auth. All print jobs are blocked until the user logs in through the EcoPrint frontend or using the test login utility.

## Architecture

### Components
1. **AuthenticationManager** (virtual_printer_agent.py, lines 665-775)
   - Manages authentication state and token persistence
   - Verifies tokens with backend every 60 seconds
   - Stores token in `C:\AI_Prints\auth_token.txt`

2. **Backend Auth Endpoints** (app/routers/print.py)
   - `/print/authorize` - Verifies Firebase ID tokens
   - `/print/log-blocked-attempt` - Logs unauthorized print attempts
   - `/print/process-job` - Enhanced with token verification

3. **FastAPIClient** (virtual_printer_agent.py, lines 777-900)
   - Integrates with AuthenticationManager
   - Blocks print jobs if not authenticated
   - Includes auth token in all API requests

## Authentication Flow

### Agent Startup
```
1. Agent starts → AuthenticationManager loads token from file
2. If token exists → Verify with backend (/print/authorize)
3. If valid → Agent ready, user logged in
4. If invalid/missing → Agent ready but blocks all prints
5. User notified: "Please log in to EcoPrint to enable printing"
```

### Print Job Processing
```
1. User sends print job → PDF created in C:\AI_Prints
2. Agent detects file → Check authentication
3. If authenticated → Process normally (classify, approve/reject)
4. If NOT authenticated:
   - Block print job
   - Delete/quarantine PDF
   - Notify user: "Please log in to EcoPrint to continue printing"
   - Log blocked attempt to Firestore
```

### Token Verification
```
1. Agent checks auth status every 60 seconds (SESSION_CHECK_INTERVAL)
2. If token expired → Clear session, notify user
3. Backend validates token structure and signature
4. Backend queries Firestore for user role
5. Returns: user_id (EPF), role (user/admin/dean)
```

## Configuration

### Enable/Disable Authentication
In `virtual_printer_agent.py`:
```python
REQUIRE_AUTH = True  # Set to False to disable login enforcement
AUTH_TOKEN_FILE = r"C:\AI_Prints\auth_token.txt"
SESSION_CHECK_INTERVAL = 60  # Seconds between token checks
```

### Token File Format
`C:\AI_Prints\auth_token.txt`:
```json
{
  "token": "eyJhbGciOiJSUzI1NiIsImtpZCI6...",
  "user_id": "99999",
  "role": "user",
  "email": "99999@ousl.edu.lk"
}
```

## Testing

### Method 1: Using Test Login Utility (Recommended)
```bash
cd "C:\Users\user\Desktop\OCT Project\ouslpms-monorepo\backend"
python test_login.py
```

Select a test user:
- **Option 1**: Regular User (EPF: 99999, Password: 999999)
- **Option 2**: Admin User (EPF: 50005, Password: 5000555)
- **Option 3**: Dean User (EPF: 60001, Password: Dean123456)
- **Option 4**: Logout (removes token file)

### Method 2: Using Frontend Login
1. Start frontend: `npm run dev` (port 5173)
2. Navigate to login page
3. Login with test credentials
4. Frontend should write token to `auth_token.txt` (TODO: implement)

### Testing Blocked Prints
1. Ensure agent is running
2. **Without logging in**, try to print a document
3. Verify behavior:
   - PDF created in C:\AI_Prints
   - Agent detects file
   - Agent blocks job (check agent.log)
   - Desktop notification appears
   - Blocked attempt logged to Firestore

### Testing Authenticated Prints
1. Run `python test_login.py` and login as user 1
2. Print a document to "Microsoft Print to PDF"
3. Save to C:\AI_Prints\test_auth.pdf
4. Verify behavior:
   - Agent detects file
   - Auth check passes
   - Classification happens normally
   - Job approved/rejected based on content
   - Job logged to Firestore print_jobs collection

## Firestore Collections

### blocked_print_attempts
Logs all blocked print attempts:
```json
{
  "user_id": "unauthenticated",
  "file_name": "test_blocked.pdf",
  "reason": "Not logged in",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### print_jobs
Logs all successful print jobs:
```json
{
  "user_id": "99999",
  "file_name": "test_auth.pdf",
  "classification": "office",
  "action": "approved",
  "file_size": 53248,
  "timestamp": "2024-01-15T10:35:00Z"
}
```

## Desktop Notifications

### Blocked Print (Unauthenticated)
```
🔒 Print Job Blocked
Please log in to EcoPrint to continue printing.
```

### Startup Warning (No Token)
```
🔒 EcoPrint Authentication Required
Please log in to EcoPrint to enable printing.
```

### Approved Print
```
✅ Print Job Approved
Document: test_auth.pdf
Classification: office
```

### Rejected Print
```
❌ Print Job Rejected
Document: personal_photo.pdf
Classification: personal (policy violation)
```

## Security Features

1. **Token Verification**: Every print job verifies token with backend
2. **Auto-Refresh**: Token validity checked every 60 seconds
3. **Audit Logging**: All blocked attempts logged to Firestore
4. **Role-Based Access**: Backend extracts role from Firestore users collection
5. **Session Persistence**: Token survives agent restarts

## Integration Points

### Frontend Integration (TODO)
The frontend login component should:
1. Authenticate with Firebase (already implemented)
2. Retrieve ID token from Firebase Auth
3. Verify token with backend `/print/authorize`
4. **Write token to `C:\AI_Prints\auth_token.txt`** (NEW)
5. Show success notification

Example code:
```javascript
// After successful Firebase login
const idToken = await user.getIdToken();
const response = await fetch('http://localhost:8000/print/authorize', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    token: idToken,
    user_id: user.uid
  })
});

if (response.ok) {
  const data = await response.json();
  // Write token to agent file
  await window.electronAPI.saveAuthToken({
    token: idToken,
    user_id: data.user_id,
    role: data.role,
    email: user.email
  });
}
```

### Agent Auto-Login (TODO)
For production, consider:
1. Frontend writes token to shared location on login
2. Agent monitors token file for changes
3. Auto-reload token when updated
4. Background token refresh (Firebase SDK)

## Troubleshooting

### Agent blocks all prints
**Cause**: No valid authentication token
**Solution**: Run `test_login.py` or login via frontend

### "Token expired" errors
**Cause**: Firebase tokens expire after 1 hour
**Solution**: Re-authenticate using test_login.py

### Blocked attempts not logged to Firestore
**Cause**: Backend connection issue or Firestore permissions
**Solution**: Check backend logs, verify Firestore rules

### Desktop notifications not appearing
**Cause**: Windows notification settings or WPARAM error
**Solution**: Check Windows notification settings, errors suppressed in daemon thread

## Next Steps

1. ✅ Backend auth endpoints created
2. ✅ AuthenticationManager implemented
3. ✅ FastAPIClient integrated with auth
4. ✅ Print job blocking implemented
5. ✅ Desktop notifications added
6. ✅ Test login utility created
7. ⏳ Frontend token sharing (write to auth_token.txt)
8. ⏳ Periodic token refresh (background task)
9. ⏳ Admin dashboard for viewing blocked attempts
10. ⏳ Enhanced audit reporting

## Files Modified

1. **backend/virtual_printer_agent.py** (1278 lines)
   - Added AuthenticationManager class (lines 665-775)
   - Updated FastAPIClient with auth integration (lines 777-900)
   - Enhanced PrintInterceptionAgent.initialize() with auth check
   - Added REQUIRE_AUTH configuration

2. **backend/app/routers/print.py** (273 lines)
   - Added /print/authorize endpoint (POST)
   - Added /print/log-blocked-attempt endpoint (POST)
   - Enhanced /print/process-job with token verification
   - Added Firestore audit logging

3. **backend/test_login.py** (NEW - 118 lines)
   - Test utility for agent authentication
   - Supports 3 test users + logout
   - Writes token to auth_token.txt

## Testing Checklist

- [ ] Start backend server (port 8000)
- [ ] Start virtual printer agent
- [ ] Verify startup notification (auth required)
- [ ] Attempt print without login → Should block
- [ ] Login using test_login.py
- [ ] Verify login notification
- [ ] Attempt print after login → Should succeed
- [ ] Check agent.log for auth messages
- [ ] Verify Firestore collections (blocked_print_attempts, print_jobs)
- [ ] Logout using test_login.py
- [ ] Verify token file deleted
- [ ] Attempt print after logout → Should block again
