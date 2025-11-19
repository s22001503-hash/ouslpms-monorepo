# EcoPrint Agent - Automatic Startup Configuration Guide

## 🎯 Overview

This guide explains how to configure the Virtual Printer Agent to run automatically in production environments.

## 📋 Available Methods

### **Method 1: Windows Task Scheduler (RECOMMENDED)**
**Best for:** Production environments, servers, enterprise deployments

**Advantages:**
- ✅ Runs on system startup (before user login)
- ✅ Auto-restart on failure
- ✅ Full logging in Event Viewer
- ✅ Easy to manage via GUI
- ✅ No console window

**Installation:**

```powershell
# Run as Administrator
cd "C:\Users\user\Desktop\OCT Project\ouslpms-monorepo\backend"
powershell -ExecutionPolicy Bypass -File .\Install-AutoStartup.ps1
```

**Verification:**
```powershell
# Check if task is running
Get-ScheduledTask -TaskName "EcoPrint Virtual Printer Agent"

# View task status
Get-ScheduledTaskInfo -TaskName "EcoPrint Virtual Printer Agent"
```

**Management:**
- Open: `taskschd.msc` (Task Scheduler)
- Find: "EcoPrint Virtual Printer Agent"
- Right-click: Start, Stop, Disable, etc.

---

### **Method 2: Windows Startup Folder**
**Best for:** Development, single-user machines, testing

**Advantages:**
- ✅ Simple setup
- ✅ Runs when user logs in
- ✅ Easy to enable/disable

**Installation:**

1. **Copy the startup script:**
```powershell
# Copy to startup folder
$startupFolder = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
Copy-Item "C:\Users\user\Desktop\OCT Project\ouslpms-monorepo\backend\START_AGENT_SILENT.bat" $startupFolder
```

2. **Test it:**
```powershell
# Run the startup script manually
& "$startupFolder\START_AGENT_SILENT.bat"
```

**To Remove:**
```powershell
Remove-Item "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\START_AGENT_SILENT.bat"
```

---

### **Method 3: Windows Service (ADVANCED)**
**Best for:** Server environments, critical systems, 24/7 operation

**Advantages:**
- ✅ Runs as system service
- ✅ Starts before user login
- ✅ Highest reliability
- ✅ Professional deployment

**Requirements:**
```powershell
# Install required packages
cd "C:\Users\user\Desktop\OCT Project\ouslpms-monorepo\backend"
.\.venv\Scripts\Activate.ps1
pip install pywin32
```

**Installation:**
```powershell
# Run as Administrator
cd "C:\Users\user\Desktop\OCT Project\ouslpms-monorepo\backend"
.\.venv\Scripts\python.exe windows_service.py install

# Start the service
.\.venv\Scripts\python.exe windows_service.py start
```

**Management:**
```powershell
# Check service status
sc query EcoPrintAgent

# Stop service
.\.venv\Scripts\python.exe windows_service.py stop

# Remove service
.\.venv\Scripts\python.exe windows_service.py remove
```

---

## 🚀 Quick Setup (Task Scheduler - Recommended)

### Step 1: Open PowerShell as Administrator
```
Right-click Start Menu → Windows PowerShell (Admin)
```

### Step 2: Run Installation Script
```powershell
cd "C:\Users\user\Desktop\OCT Project\ouslpms-monorepo\backend"
Set-ExecutionPolicy Bypass -Scope Process -Force
.\Install-AutoStartup.ps1
```

### Step 3: Verify Installation
```powershell
# Check task exists
Get-ScheduledTask -TaskName "EcoPrint Virtual Printer Agent"

# Start immediately (without reboot)
Start-ScheduledTask -TaskName "EcoPrint Virtual Printer Agent"
```

### Step 4: Test Auto-Start
```powershell
# Restart computer to test
Restart-Computer
```

After reboot, the agent should be running automatically!

---

## 🔍 Verification & Monitoring

### Check if Agent is Running
```powershell
# Method 1: Check process
Get-Process -Name python | Where-Object {$_.CommandLine -like "*virtual_printer_agent*"}

# Method 2: Check listening port (if applicable)
Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue

# Method 3: Check C:\AI_Prints folder monitoring
Test-Path "C:\AI_Prints"
```

### View Agent Logs
```powershell
# If using Task Scheduler, check Event Viewer
eventvwr.msc
# Navigate to: Windows Logs → Application
# Filter by: Task Scheduler

# Or check agent log file (if logging to file)
Get-Content "C:\Users\user\Desktop\OCT Project\ouslpms-monorepo\backend\agent.log" -Tail 50 -Wait
```

---

## 🛠️ Troubleshooting

### Agent Not Starting Automatically

**Check Task Scheduler:**
```powershell
Get-ScheduledTask -TaskName "EcoPrint Virtual Printer Agent" | Format-List *
```

**Check Task History:**
1. Open Task Scheduler (`taskschd.msc`)
2. Find "EcoPrint Virtual Printer Agent"
3. Click "History" tab
4. Look for errors

**Common Issues:**

1. **Python path wrong:**
   - Edit task: Update Python executable path
   - Use full path: `C:\Users\user\Desktop\OCT Project\ouslpms-monorepo\backend\.venv\Scripts\python.exe`

2. **Working directory incorrect:**
   - Set "Start in" directory to: `C:\Users\user\Desktop\OCT Project\ouslpms-monorepo\backend`

3. **Permissions issue:**
   - Run task as Administrator
   - Set "Run with highest privileges"

---

## 🔒 Security Considerations

### Production Deployment Checklist

- [ ] **Use Task Scheduler** (not Startup Folder) for better security
- [ ] **Run as service account** (not admin) in production
- [ ] **Enable logging** to monitor agent activity
- [ ] **Set up alerts** for agent failures
- [ ] **Regular updates** of dependencies
- [ ] **Backup configuration** (auth tokens, settings)
- [ ] **Test auto-restart** on failure

### Authentication Token Security

The agent stores authentication tokens in:
```
C:\AI_Prints\auth_token.txt
```

**Protect this file:**
```powershell
# Set appropriate permissions (only current user)
$acl = Get-Acl "C:\AI_Prints\auth_token.txt"
$acl.SetAccessRuleProtection($true, $false)
$rule = New-Object System.Security.AccessControl.FileSystemAccessRule(
    $env:USERNAME, "FullControl", "Allow"
)
$acl.SetAccessRule($rule)
Set-Acl "C:\AI_Prints\auth_token.txt" $acl
```

---

## 📊 Production Deployment Workflow

### For Office/Organization Deployment:

1. **Test thoroughly** on development machine
2. **Create Group Policy** to deploy Task Scheduler task
3. **Use centralized logging** (send logs to central server)
4. **Monitor agent health** (check-in service)
5. **Auto-update mechanism** (pull updates from repo)

### Example: Deploy to Multiple Machines

```powershell
# Create deployment package
$deployPath = "\\server\share\EcoPrintAgent"

# Copy necessary files
Copy-Item -Recurse -Path "backend" -Destination $deployPath

# Create deployment script for each machine
# (customize paths for each machine)
```

---

## 🎯 Recommended Setup

**For Production/Office Environment:**
```
✅ Use Task Scheduler method
✅ Run on system startup
✅ Auto-restart on failure (3 attempts)
✅ Log to Event Viewer
✅ Run with highest privileges
✅ Network available not required
```

**For Development/Testing:**
```
✅ Use Startup Folder method OR
✅ Run manually when needed
✅ Console window visible for debugging
```

---

## 📞 Support

If the agent fails to start automatically:

1. **Check Event Viewer** for errors
2. **Run manually** to see error messages:
   ```powershell
   cd "C:\Users\user\Desktop\OCT Project\ouslpms-monorepo\backend"
   .\.venv\Scripts\python.exe virtual_printer_agent.py
   ```
3. **Verify paths** in Task Scheduler are correct
4. **Check permissions** (run as admin if needed)

---

## 🎉 Success Verification

After setup, verify the agent is working:

1. **Reboot computer**
2. **Check Task Manager** → "python.exe" should be running
3. **Try printing** without logging in → should be blocked
4. **Login to dashboard** → prints should work
5. **Check notifications** appear correctly

The agent is now running automatically! 🚀
