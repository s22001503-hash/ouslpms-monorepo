# Sprint 4: Print Interception System - Setup & Testing Guide

## 📋 Overview
The Virtual Printer Agent intercepts print jobs, classifies documents using AI, and enforces print policies based on admin settings.

## 🚀 Installation Steps

### 1. Install Python Dependencies
```powershell
cd backend
pip install pywin32 watchdog requests
```

### 2. Create Output Directory
```powershell
mkdir C:\AI_Prints
```

### 3. Configure Virtual Printer
The script will automatically set up "AI Classifier Printer" using Microsoft Print to PDF on first run.

## ▶️ Running the System

### Step 1: Start Backend API
```powershell
# Terminal 1
cd backend
uvicorn app.main:app --reload --port 8000
```

### Step 2: Start Virtual Printer Agent
```powershell
# Terminal 2
cd backend
python virtual_printer_agent.py
```

You should see:
```
✅ Print Spooler service is running
✅ Virtual Printer 'AI Classifier Printer' configured
🖨️ Virtual Printer Agent started...
📂 Monitoring: C:\AI_Prints
⏰ Spooler check interval: 5 seconds
```

## 🧪 Testing the System

### Test 1: Basic Print Interception
1. Open Notepad and type "Test Document - Office Report"
2. Click **File > Print**
3. Select **"AI Classifier Printer"** from printer list
4. Click **Print**
5. Check console output for:
   - ✅ Detected print job
   - ✅ Auth check passed
   - ✅ Metadata extracted
   - ✅ File saved to C:\AI_Prints
   - ✅ Classification result (office/personal/sensitive)

### Test 2: Authentication Check
The agent requires a valid Firebase Auth token. To test:

**Option A: Use Login Token (Recommended)**
1. Login to frontend (http://localhost:5173)
2. Open browser DevTools > Application > Local Storage
3. Copy `idToken` value
4. Modify `virtual_printer_agent.py` line 186:
   ```python
   headers = {'Authorization': f'Bearer {your_token_here}'}
   ```

**Option B: Bypass Auth for Testing**
1. Modify `virtual_printer_agent.py` line 174-188:
   ```python
   def check_user_auth(user_id: str) -> Dict[str, Any]:
       # Bypass auth for testing
       return {
           'authenticated': True,
           'role': 'user',
           'epf': user_id
       }
   ```

### Test 3: Document Classification
Print different documents to test classification:

**Office Document:**
- Filename: "Monthly_Report.pdf"
- Expected: Classification = `office`, Action = `approved`

**Personal Document:**
- Filename: "Birthday_Invitation.pdf"
- Expected: Classification = `personal`, Action = `block` (for regular users)

**Sensitive Document:**
- Filename: "Confidential_Budget.pdf"
- Expected: Classification = `sensitive`, Action = `require_approval`

### Test 4: Check API Response
After a print job is processed:
```powershell
# Check Firestore for logged job
# Or check console output for API response:
# {
#   "status": "success",
#   "classification": "office",
#   "action": "approved",
#   "message": "Document classified as office. Action: approved",
#   "job_id": "PRINT_20250117_143022"
# }
```

## 📊 Expected Flow

```
User Prints Document
       ↓
Windows Print Spooler → "AI Classifier Printer"
       ↓
Print Job appears in queue (win32print.EnumJobs)
       ↓
SpoolerManager detects job → Extract metadata
       ↓
PDF saved to C:\AI_Prints (Microsoft Print to PDF)
       ↓
PrintFolderWatcher detects new file
       ↓
Check user authentication (Firebase token)
       ↓
Send to FastAPI /print/process-job
       ↓
AI Classification (office/personal/sensitive)
       ↓
Policy Decision (approved/block/require_approval)
       ↓
Response sent back to agent
       ↓
[Optional] Forward to physical printer if approved
```

## 🔍 Troubleshooting

### Issue: "Print Spooler service is not running"
**Solution:**
```powershell
# Start Print Spooler
net start spooler
```

### Issue: "'Microsoft Print to PDF' printer not found"
**Solution:**
1. Open **Settings > Devices > Printers & scanners**
2. Click **Add a printer**
3. If "Microsoft Print to PDF" is missing:
   - Open **Settings > Apps > Optional features**
   - Click **Add a feature**
   - Search for "Microsoft Print to PDF"
   - Install it

### Issue: "No print jobs detected"
**Check:**
1. Printer is set to "AI Classifier Printer"
2. Print Spooler service is running
3. Script has admin privileges (run as Administrator if needed)

### Issue: "Authentication failed"
**Solution:**
1. Verify backend is running on port 8000
2. Check Firebase token is valid (not expired)
3. Use bypass auth method for testing

### Issue: "File not saved to C:\AI_Prints"
**Check:**
1. Folder exists and has write permissions
2. "Microsoft Print to PDF" is properly installed
3. Virtual printer name is exactly "AI Classifier Printer"

## 📝 Logging

The agent provides comprehensive logging:

**Print Job Detection:**
```
🔍 Detected print job: JobID=45, User=60001, Document=Report.pdf, Pages=3
```

**Authentication:**
```
✅ User authentication successful: EPF=60001, Role=admin
```

**Classification:**
```
📊 Classification: office, Action: approved
```

**Errors:**
```
❌ Error processing print job: Connection refused
```

## 🎯 Next Steps

1. **Enhance AI Classification:**
   - Integrate actual ML model (PyPDF2 + scikit-learn)
   - Extract text from PDF
   - Analyze content patterns

2. **Implement Firestore Logging:**
   - Store all print jobs in `print_jobs` collection
   - Track user print history
   - Generate audit reports

3. **Add Admin Dashboard Integration:**
   - Show pending approvals
   - Dean can approve/reject sensitive prints
   - Real-time print job monitoring

4. **Physical Printer Forwarding:**
   - Configure default physical printer
   - Forward approved jobs automatically
   - Handle printer errors gracefully

## 🔐 Security Considerations

- **Authentication:** Always validate Firebase tokens in production
- **File Access:** Restrict C:\AI_Prints to authorized users only
- **Logging:** Never log sensitive document content, only metadata
- **Approval Workflow:** Require Dean approval for all sensitive documents

## 📦 Production Deployment

1. **Run as Windows Service:**
   - Use `pywin32` to create Windows service
   - Auto-start on system boot
   - Run with minimal privileges

2. **Error Handling:**
   - Implement retry logic for API failures
   - Log all errors to file (not just console)
   - Send alerts for critical failures

3. **Performance:**
   - Optimize spooler polling interval (currently 5 seconds)
   - Implement file processing queue for high volume
   - Use async processing for API calls

## 📚 API Endpoints

### POST /print/process-job
Process intercepted print job.

**Request:**
```json
{
  "file_path": "C:\\AI_Prints\\Report_20250117_143022.pdf",
  "file_name": "Report.pdf",
  "file_size": 52428,
  "printer": "AI Classifier Printer",
  "user_id": "60001",
  "document": "Monthly Report",
  "total_pages": 3,
  "timestamp": "2025-01-17 14:30:22",
  "status": "printing"
}
```

**Response:**
```json
{
  "status": "success",
  "classification": "office",
  "action": "approved",
  "message": "Document classified as office. Action: approved",
  "job_id": "PRINT_20250117_143022"
}
```

### GET /print/print-stats
Get print job statistics.

**Response:**
```json
{
  "total_jobs": 156,
  "approved": 120,
  "blocked": 15,
  "pending_approval": 21
}
```

## ✅ Verification Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173
- [ ] Print Spooler service running
- [ ] C:\AI_Prints folder created
- [ ] "Microsoft Print to PDF" installed
- [ ] Python dependencies installed (pywin32, watchdog, requests)
- [ ] virtual_printer_agent.py running without errors
- [ ] Test print job successfully intercepted
- [ ] PDF file saved to C:\AI_Prints
- [ ] API /print/process-job returns classification
- [ ] Console shows complete flow logs

---

**Last Updated:** January 17, 2025  
**Version:** 1.0.0  
**Author:** Sprint 4 Implementation Team
