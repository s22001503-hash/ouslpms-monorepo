"""
Windows Service Wrapper for Virtual Printer Agent
Install this as a Windows Service to run automatically on system startup
"""
import os
import sys
import time
import servicemanager
import win32event
import win32service
import win32serviceutil
import subprocess
from pathlib import Path

# Add the backend directory to Python path
BACKEND_DIR = Path(__file__).parent.absolute()
sys.path.insert(0, str(BACKEND_DIR))

class VirtualPrinterService(win32serviceutil.ServiceFramework):
    """Windows Service for Virtual Printer Agent"""
    
    _svc_name_ = "EcoPrintAgent"
    _svc_display_name_ = "EcoPrint Virtual Printer Agent"
    _svc_description_ = "Monitors and classifies print jobs using AI"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_running = True
        self.agent_process = None
        
    def SvcStop(self):
        """Called when the service is being stopped"""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_running = False
        
        # Terminate the agent process
        if self.agent_process:
            self.agent_process.terminate()
            self.agent_process.wait(timeout=10)
        
    def SvcDoRun(self):
        """Called when the service starts"""
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        
        # Change to backend directory
        os.chdir(BACKEND_DIR)
        
        # Start the virtual printer agent
        try:
            # Activate virtual environment and run agent
            python_exe = BACKEND_DIR / ".venv" / "Scripts" / "python.exe"
            agent_script = BACKEND_DIR / "virtual_printer_agent.py"
            
            servicemanager.LogInfoMsg(f"Starting agent: {agent_script}")
            
            self.agent_process = subprocess.Popen(
                [str(python_exe), str(agent_script)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=str(BACKEND_DIR)
            )
            
            # Wait for stop signal
            while self.is_running:
                # Check if agent process crashed
                if self.agent_process.poll() is not None:
                    servicemanager.LogErrorMsg("Agent process terminated unexpectedly")
                    # Restart after 5 seconds
                    time.sleep(5)
                    self.agent_process = subprocess.Popen(
                        [str(python_exe), str(agent_script)],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        cwd=str(BACKEND_DIR)
                    )
                
                # Check stop event every second
                rc = win32event.WaitForSingleObject(self.hWaitStop, 1000)
                if rc == win32event.WAIT_OBJECT_0:
                    break
                    
        except Exception as e:
            servicemanager.LogErrorMsg(f"Error in service: {str(e)}")
            raise

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(VirtualPrinterService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(VirtualPrinterService)
