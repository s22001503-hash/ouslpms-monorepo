# 🚀 Sprint 5 - Firestore-Driven Policy Enforcement

## Overview

Sprint 5 implements **admin-configurable print policies** using Firestore, removing all hardcoded limits from the agent and centralizing policy enforcement in the backend.

---

## ✨ What Changed

### **Before (Sprint 4 - Hardcoded Limits):**
```python
# Agent (virtual_printer_agent.py)
MAX_DAILY_PRINTS = 3  # ❌ Hardcoded
if daily_print_count >= MAX_DAILY_PRINTS:
    block_print()
```

### **After (Sprint 5 - Firestore-Driven):**
```python
# Backend (/process-job endpoint)
policies = firestore.get('system_policies/default')
max_daily_prints = policies['max_daily_prints']  # ✅ Admin-configurable

user_limits = firestore.get(f'user_daily_limits/{user_id}_{today}')
if user_limits['prints_today'] >= max_daily_prints:
    block_print()
```

---

## 🗄️ Firestore Collections

### 1. **`system_policies`** (Admin Configuration)

**Document ID:** `default`

```json
{
  "max_daily_prints": 3,
  "max_copies_per_document": 10,
  "personal_documents_allowed": false,
  "official_documents_allowed": true,
  "confidential_documents_allowed": true,
  "updated_at": "2025-10-29T10:00:00Z",
  "updated_by": "admin@ousl.ac.lk"
}
```

**How Admins Change Policies:**
- Firebase Console → Firestore → `system_policies` → `default`
- Edit values (e.g., change `max_daily_prints` from 3 to 5)
- Save → Changes apply immediately (no code deployment needed!)

---

### 2. **`user_daily_limits`** (Daily Print Tracking)

**Document ID:** `{user_id}_{date}` (e.g., `99999_2025-10-29`)

```json
{
  "user_id": "99999",
  "date": "2025-10-29",
  "prints_today": 2,
  "max_daily_prints": 3,
  "prints": [
    {
      "timestamp": "2025-10-29T09:00:00Z",
      "file_hash": "abc123...",
      "file_name": "Report.pdf",
      "classification": "office",
      "copies": 1
    },
    {
      "timestamp": "2025-10-29T14:00:00Z",
      "file_hash": "def456...",
      "file_name": "Memo.pdf",
      "classification": "confidential",
      "copies": 2
    }
  ],
  "updated_at": "2025-10-29T14:00:00Z"
}
```

**Auto-Reset:**
- New day → New document (e.g., `99999_2025-10-30`)
- Counter starts at 0 automatically

---

### 3. **`print_logs`** (Permanent Audit Trail)

```json
{
  "job_id": "PRINT_20251029_140000",
  "user_id": "99999",
  "file_name": "Report.pdf",
  "file_hash": "abc123...",
  "classification": "office",
  "action": "allow",
  "executive_summary": {
    "title": "Q3 Sales Report",
    "summary": "Executive summary of the document...",
    "key_topics": ["sales", "Q3", "analysis"],
    "sensitive_data_detected": false
  },
  "copies": 1,
  "timestamp": "2025-10-29T14:00:00Z",
  "logged_at": "SERVER_TIMESTAMP"
}
```

---

### 4. **`blocked_print_attempts`** (Security Audit)

```json
{
  "user_id": "99999",
  "file_name": "Birthday.pdf",
  "classification": "personal",
  "reason": "Personal documents are not allowed",
  "timestamp": "2025-10-29T15:00:00Z",
  "logged_at": "SERVER_TIMESTAMP"
}
```

---

## 📊 Print Flow (Sprint 5)

### **Scenario 1: Personal Document (BLOCKED)**
```
User prints "Birthday.pdf"
  ↓
AI Classification: "personal"
  ↓
❌ BLOCK IMMEDIATELY
  ↓
Log to blocked_print_attempts
  ↓
Daily counter NOT incremented
  ↓
Delete file
```

### **Scenario 2: Official Document (Daily Limit Check)**
```
User prints "Report.pdf"
  ↓
AI Classification: "office"
  ↓
CHECK #1: Daily Limit
  ├─ Query Firestore: prints_today = 2, max_daily_prints = 3
  └─ 2 < 3 ✅ Continue
  ↓
CHECK #2: Copy Limit
  ├─ From spooler: copies = 5
  ├─ Query Firestore: max_copies_per_document = 10
  └─ 5 <= 10 ✅ Continue
  ↓
✅ ALLOW PRINT
  ↓
Increment counter: prints_today = 3
  ↓
Log to print_logs
  ↓
File stays in C:\AI_Prints
```

### **Scenario 3: Too Many Copies (BLOCKED)**
```
User prints "Contract.pdf" with 15 copies
  ↓
AI Classification: "confidential"
  ↓
CHECK #1: Daily Limit ✅ (2/3 prints today)
  ↓
CHECK #2: Copy Limit
  ├─ From spooler: copies = 15
  ├─ Query Firestore: max_copies_per_document = 10
  └─ 15 > 10 ❌ BLOCK
  ↓
Log to blocked_print_attempts
  ↓
Daily counter NOT incremented (still 2/3)
  ↓
Delete file
```

---

## 🔧 Setup Instructions

### **Step 1: Initialize Firestore Policies**

Run the initialization script to create the default policies:

```bash
cd backend
python scripts/init_firestore_policies.py
```

**Output:**
```
✅ System policies created successfully!

📋 Default Policies:
   • Max daily prints: 3
   • Max copies per document: 10
   • Personal documents: Blocked
   • Official documents: Allowed
   • Confidential documents: Allowed
```

---

### **Step 2: Restart Backend**

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Logs:**
```
✅ Firebase Admin initialized with service account key
✅ OpenAI API initialized for executive summary generation
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

### **Step 3: Restart Agent**

```bash
cd backend
python virtual_printer_agent.py
```

**Expected Logs:**
```
✅ User authenticated - proceeding with classification
✅ SPRINT 5: Daily print limit check REMOVED from agent
✅ Daily limits are now enforced by backend via Firestore
```

---

## 🎯 Admin Tasks

### **Change Daily Print Limit (3 → 5 prints/day):**

1. Open Firebase Console
2. Go to Firestore Database
3. Navigate to `system_policies` → `default`
4. Click "Edit document"
5. Change `max_daily_prints`: `3` → `5`
6. Save

**✅ Changes apply immediately!** (No server restart needed)

---

### **Change Copy Limit (10 → 20 copies/doc):**

1. Firebase Console → Firestore
2. `system_policies` → `default`
3. Edit `max_copies_per_document`: `10` → `20`
4. Save

---

### **Allow Personal Documents:**

1. Firebase Console → Firestore
2. `system_policies` → `default`
3. Edit `personal_documents_allowed`: `false` → `true`
4. Save

**⚠️ Warning:** This will allow users to print personal documents!

---

## 📝 Code Changes Summary

### **Backend (`app/routers/print.py`):**

**Changed:**
- `/process-job` endpoint now queries Firestore for policies
- Personal documents → BLOCK immediately (no checks)
- Official/Confidential → Check daily limit + copy limit
- Daily counter incremented ONLY on successful approval
- Executive summary generated for allowed prints only

**New Logic:**
```python
# Personal documents: BLOCK
if classification == 'personal':
    return {'action': 'block', 'reason': 'Personal documents not allowed'}

# Official/Confidential: Check Firestore limits
policies = firestore.get('system_policies/default')
user_limits = firestore.get(f'user_daily_limits/{user_id}_{today}')

if prints_today >= max_daily_prints:
    return {'action': 'block', 'reason': 'Daily limit reached'}

if copies > max_copies_per_document:
    return {'action': 'block', 'reason': 'Too many copies'}

# ✅ ALLOW and increment counter
increment_daily_count()
```

---

### **Agent (`virtual_printer_agent.py`):**

**Removed:**
- `MAX_DAILY_PRINTS` constant
- `daily_print_count` variable
- `daily_reset_date` tracking
- Daily limit check in `process_file()`
- Counter increment logic

**Why?**
- All policy enforcement moved to backend
- Agent just sends to backend and handles response
- Simpler, more maintainable code

---

## 🧪 Testing

### **Test 1: Print Official Document (Should Allow)**

```python
# User: 99999, Daily prints: 0/3
# Action: Print "Report.pdf" (official, 1 copy)

Expected Result:
✅ Classification: office
✅ Daily limit check: 0 < 3 (pass)
✅ Copy limit check: 1 <= 10 (pass)
✅ ALLOW print
✅ Counter: 1/3
✅ Log to print_logs
```

---

### **Test 2: Print Personal Document (Should Block)**

```python
# User: 99999
# Action: Print "Birthday.pdf" (personal)

Expected Result:
❌ Classification: personal
❌ BLOCK immediately (no further checks)
❌ Counter unchanged
❌ Log to blocked_print_attempts
```

---

### **Test 3: Exceed Daily Limit (Should Block)**

```python
# User: 99999, Daily prints: 3/3
# Action: Print "Memo.pdf" (official, 1 copy)

Expected Result:
✅ Classification: office
❌ Daily limit check: 3 >= 3 (fail)
❌ BLOCK print
❌ Counter unchanged (3/3)
❌ Log to blocked_print_attempts
```

---

### **Test 4: Too Many Copies (Should Block)**

```python
# User: 99999, Daily prints: 2/3
# Action: Print "Contract.pdf" (official, 15 copies)

Expected Result:
✅ Classification: office
✅ Daily limit check: 2 < 3 (pass)
❌ Copy limit check: 15 > 10 (fail)
❌ BLOCK print
❌ Counter unchanged (2/3)
❌ Log to blocked_print_attempts
```

---

## 📊 Firestore Queries (For Analytics)

### **Get user's print history:**
```javascript
db.collection('print_logs')
  .where('user_id', '==', '99999')
  .where('date', '==', '2025-10-29')
  .orderBy('timestamp', 'desc')
  .get()
```

### **Get all blocked attempts today:**
```javascript
db.collection('blocked_print_attempts')
  .where('timestamp', '>=', startOfDay)
  .orderBy('timestamp', 'desc')
  .get()
```

### **Get total prints per user:**
```javascript
db.collection('user_daily_limits')
  .where('user_id', '==', '99999')
  .orderBy('date', 'desc')
  .limit(30)  // Last 30 days
  .get()
```

---

## 🔐 Security Notes

1. **Firestore Rules:** Ensure proper security rules in Firebase Console
2. **Admin Access:** Only admins should edit `system_policies`
3. **Audit Trail:** All changes logged with `updated_by` field
4. **User Limits:** Users CANNOT modify their own daily limits

---

## 🎉 Benefits

### **Before Sprint 5:**
- ❌ Hardcoded limits in agent code
- ❌ Need code deployment to change policies
- ❌ No centralized configuration
- ❌ Users lose quota even if print blocked

### **After Sprint 5:**
- ✅ Admin-configurable limits (no code changes!)
- ✅ Centralized policy enforcement in backend
- ✅ Instant policy updates via Firestore
- ✅ Fair quota tracking (blocked prints don't count)
- ✅ Complete audit trail in Firestore
- ✅ Executive summaries for approved prints

---

## 📞 Support

**Issues?**
- Check Firestore Console for policy values
- Verify `system_policies/default` document exists
- Run `scripts/init_firestore_policies.py` if missing

**Questions?**
- Contact: admin@ousl.ac.lk
- Documentation: This file!

---

**✅ Sprint 5 Complete!** Enjoy admin-configurable, Firestore-driven print policies! 🎉
