# 🚀 EcoPrint Agent - Auto-Startup Quick Reference

## ✅ YES - The Agent CAN Run Automatically!

---

## 🎯 Quick Setup (30 Seconds)

### **One-Click Installation:**

1. **Navigate to backend folder:**
   ```powershell
   cd "C:\Users\user\Desktop\OCT Project\ouslpms-monorepo\backend"
   ```

2. **Right-click** `INSTALL_AUTO_STARTUP.bat` → **"Run as administrator"**

3. **Done!** Agent will start automatically on every boot.

---

## 📋 What Gets Installed?

✅ **Task Scheduler Entry** - Runs agent on startup  
✅ **Auto-Restart** - Restarts if agent crashes (3 attempts)  
✅ **Background Mode** - No visible console window  
✅ **Event Logging** - Errors logged to Windows Event Viewer  

---

## 🔍 Verify It's Working

```powershell
# Check if scheduled task exists
Get-ScheduledTask -TaskName "EcoPrint Virtual Printer Agent"

# Check if agent is running
Get-Process python | Where-Object {$_.CommandLine -like "*virtual_printer*"}

# Start/Stop manually
Start-ScheduledTask -TaskName "EcoPrint Virtual Printer Agent"
Stop-ScheduledTask -TaskName "EcoPrint Virtual Printer Agent"
```

---

## 🛠️ Management

### **Start Agent:**
```powershell
Start-ScheduledTask -TaskName "EcoPrint Virtual Printer Agent"
```

### **Stop Agent:**
```powershell
Stop-ScheduledTask -TaskName "EcoPrint Virtual Printer Agent"
```

### **Disable Auto-Start:**
```powershell
Disable-ScheduledTask -TaskName "EcoPrint Virtual Printer Agent"
```

### **Enable Auto-Start:**
```powershell
Enable-ScheduledTask -TaskName "EcoPrint Virtual Printer Agent"
```

### **Uninstall:**
```powershell
Unregister-ScheduledTask -TaskName "EcoPrint Virtual Printer Agent" -Confirm:$false
```

---

## 📊 Manual Method (Alternative)

If you prefer to set it up manually:

### **Step 1:** Open Task Scheduler
- Press `Win+R`, type `taskschd.msc`, press Enter

### **Step 2:** Create Basic Task
- Click "Create Basic Task"
- Name: `EcoPrint Virtual Printer Agent`

### **Step 3:** Set Trigger
- When: `When the computer starts` OR `When I log on`

### **Step 4:** Set Action
- Action: `Start a program`
- Program: `C:\Users\user\Desktop\OCT Project\ouslpms-monorepo\backend\.venv\Scripts\python.exe`
- Arguments: `virtual_printer_agent.py`
- Start in: `C:\Users\user\Desktop\OCT Project\ouslpms-monorepo\backend`

### **Step 5:** Configure Settings
- ✅ Run whether user is logged on or not
- ✅ Run with highest privileges
- ✅ If task fails, restart every 1 minute (3 times max)

---

## 🎯 Production Deployment

For deploying to multiple computers:

1. **Test on one machine first** ✅
2. **Use Group Policy** for domain computers
3. **Or copy** `Install-AutoStartup.ps1` to each machine
4. **Run as admin** on each machine

---

## 📞 Troubleshooting

### Agent Not Starting?

**Check Task History:**
```
Task Scheduler → Find task → History tab
```

**Run Manually to See Errors:**
```powershell
cd "C:\Users\user\Desktop\OCT Project\ouslpms-monorepo\backend"
.\.venv\Scripts\python.exe virtual_printer_agent.py
```

**Common Fixes:**
- ✅ Verify paths are correct
- ✅ Run Task Scheduler as Administrator
- ✅ Check Python virtual environment exists
- ✅ Ensure backend folder has permissions

---

## 💡 Tips

**For Development:**
- Keep auto-start disabled
- Run manually when testing
- Use `START_AGENT.bat` for quick start

**For Production:**
- Enable auto-start
- Set up monitoring
- Check Event Viewer regularly
- Test restart after system reboot

---

## ✅ Verification Checklist

After installation:

- [ ] Reboot computer
- [ ] Agent starts automatically
- [ ] No console window appears
- [ ] Printing without login is blocked
- [ ] Notification appears when blocked
- [ ] Login allows printing
- [ ] Task shows as "Running" in Task Scheduler

---

## 🎉 Success!

Your EcoPrint Agent is now configured to run automatically!

**Next Steps:**
1. Test by rebooting
2. Try printing before login (should block)
3. Login via web dashboard
4. Try printing after login (should work)

**Questions?** See full guide: `AUTO_STARTUP_GUIDE.md`
