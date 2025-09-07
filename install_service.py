#!/usr/bin/env python3
"""
Windows Service Installer for CSV Search Engine
This creates a Windows service that runs the Streamlit app 24/7
"""

import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import time
import sys
import os
import subprocess
from pathlib import Path

class CSVSearchEngineService(win32serviceutil.ServiceFramework):
    """Windows Service for CSV Search Engine"""
    
    _svc_name_ = "CSVSearchEngine"
    _svc_display_name_ = "CSV Search Engine Service"
    _svc_description_ = "24/7 CSV Search Engine with Streamlit Web Interface"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.process = None
        
    def SvcStop(self):
        """Stop the service"""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        if self.process:
            self.process.terminate()
            
    def SvcDoRun(self):
        """Run the service"""
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        
        # Change to the project directory
        project_dir = Path(__file__).parent
        os.chdir(project_dir)
        
        # Start the Streamlit app
        self.start_streamlit()
        
        # Wait for stop signal
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
        
    def start_streamlit(self):
        """Start the Streamlit application"""
        try:
            # Activate virtual environment and start Streamlit
            src_dir = project_dir / "src"
            cmd = [
                str(project_dir / "venv" / "Scripts" / "python.exe"),
                "-m", "streamlit", "run", "app.py",
                "--server.port", "8501",
                "--server.address", "0.0.0.0",
                "--server.headless", "true"
            ]
            
            self.process = subprocess.Popen(cmd, cwd=src_dir)
            servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                                  servicemanager.PYS_SERVICE_STARTED,
                                  ("Streamlit started on port 8501", ''))
            
        except Exception as e:
            servicemanager.LogMsg(servicemanager.EVENTLOG_ERROR_TYPE,
                                  servicemanager.PYS_SERVICE_STOPPED,
                                  (f"Error starting Streamlit: {e}", ''))

def install_service():
    """Install the Windows service"""
    try:
        win32serviceutil.InstallService(
            CSVSearchEngineService._svc_reg_class_,
            CSVSearchEngineService._svc_name_,
            CSVSearchEngineService._svc_display_name_,
            description=CSVSearchEngineService._svc_description_
        )
        print("✅ Service installed successfully!")
        print("🔧 To start the service, run as Administrator:")
        print("   net start CSVSearchEngine")
        print("🛑 To stop the service:")
        print("   net stop CSVSearchEngine")
        print("🗑️  To remove the service:")
        print("   python install_service.py remove")
        
    except Exception as e:
        print(f"❌ Error installing service: {e}")

def remove_service():
    """Remove the Windows service"""
    try:
        win32serviceutil.RemoveService(CSVSearchEngineService._svc_name_)
        print("✅ Service removed successfully!")
    except Exception as e:
        print(f"❌ Error removing service: {e}")

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(CSVSearchEngineService)
        servicemanager.StartServiceCtrlDispatcher()
    elif sys.argv[1] == 'install':
        install_service()
    elif sys.argv[1] == 'remove':
        remove_service()
    else:
        win32serviceutil.HandleCommandLine(CSVSearchEngineService)
