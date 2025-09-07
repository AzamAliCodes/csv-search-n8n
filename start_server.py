#!/usr/bin/env python3
"""
24/7 CSV Search Engine Server
This script ensures the Streamlit app runs continuously with auto-restart
"""

import subprocess
import time
import sys
import os
from pathlib import Path

def start_streamlit():
    """Start the Streamlit app with proper configuration"""
    try:
        # Change to the src directory
        src_dir = Path(__file__).parent / "src"
        os.chdir(src_dir)
        
        # Start Streamlit with 24/7 configuration
        cmd = [
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0",  # Allow external access
            "--server.headless", "true",     # No browser auto-open
            "--server.runOnSave", "true",    # Auto-reload on file changes
            "--server.enableCORS", "false",  # Disable CORS for local use
            "--server.enableXsrfProtection", "false"  # Disable XSRF for local use
        ]
        
        print("🚀 Starting CSV Search Engine Server...")
        print("📡 Server will be accessible at:")
        print("   - Local: http://localhost:8501")
        print("   - Network: http://0.0.0.0:8501")
        print("   - External: http://YOUR_IP:8501")
        print("🔄 Auto-restart enabled - server will restart if it crashes")
        print("⏹️  Press Ctrl+C to stop the server")
        print("-" * 60)
        
        # Start the process
        process = subprocess.Popen(cmd)
        
        # Wait for the process to complete or be interrupted
        process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        if 'process' in locals():
            process.terminate()
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False
    
    return True

def main():
    """Main function with auto-restart logic"""
    restart_count = 0
    max_restarts = 10
    
    while restart_count < max_restarts:
        print(f"🔄 Starting server (attempt {restart_count + 1}/{max_restarts})")
        
        if start_streamlit():
            break
        
        restart_count += 1
        if restart_count < max_restarts:
            print(f"⏳ Waiting 5 seconds before restart...")
            time.sleep(5)
    
    if restart_count >= max_restarts:
        print("❌ Maximum restart attempts reached. Please check the logs.")

if __name__ == "__main__":
    main()
