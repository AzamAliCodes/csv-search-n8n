#!/usr/bin/env python3
"""
Quick deployment script for PythonAnywhere
"""

import os
import zipfile
from pathlib import Path

def create_deployment_package():
    """Create a deployment package for PythonAnywhere"""
    
    # Files to include in deployment
    files_to_include = [
        "src/app.py",
        "src/build_index.py", 
        "src/search.py",
        "data/workflows.csv",
        "requirements.txt",
        "README.md"
    ]
    
    # Create deployment directory
    deploy_dir = Path("pythonanywhere_deploy")
    deploy_dir.mkdir(exist_ok=True)
    
    # Copy files
    for file_path in files_to_include:
        if Path(file_path).exists():
            dest_path = deploy_dir / file_path
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'r', encoding='utf-8') as src:
                with open(dest_path, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
    
    # Create PythonAnywhere specific files
    create_pythonanywhere_files(deploy_dir)
    
    # Create ZIP file
    zip_path = "csv_search_engine_pythonanywhere.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(deploy_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(deploy_dir)
                zipf.write(file_path, arcname)
    
    print(f"✅ Deployment package created: {zip_path}")
    return zip_path

def create_pythonanywhere_files(deploy_dir):
    """Create PythonAnywhere specific configuration files"""
    
    # Create WSGI file
    wsgi_content = """import sys
import os

# Add your project directory to the Python path
path = '/home/yourusername/csv_search_engine'
if path not in sys.path:
    sys.path.append(path)

# Change to your project directory
os.chdir(path)

# Import and run your Streamlit app
from src.app import main

if __name__ == '__main__':
    main()"""
    
    with open(deploy_dir / "pythonanywhere_wsgi.py", "w") as f:
        f.write(wsgi_content)
    
    # Create startup script
    startup_script = """#!/bin/bash
# PythonAnywhere startup script

# Install dependencies
pip3.9 install --user -r requirements.txt

# Build search index
python3.9 src/build_index.py

# Start Streamlit (for console testing)
# streamlit run src/app.py --server.port 8501 --server.address 0.0.0.0
"""
    
    with open(deploy_dir / "startup.sh", "w") as f:
        f.write(startup_script)
    
    # Create PythonAnywhere instructions
    instructions = """# PythonAnywhere Deployment Instructions

## Step 1: Upload Files
1. Go to https://www.pythonanywhere.com
2. Sign up for a free account
3. Go to 'Files' tab
4. Upload the csv_search_engine_pythonanywhere.zip file
5. Extract it in your home directory

## Step 2: Install Dependencies
1. Go to 'Consoles' tab
2. Start a new Bash console
3. Run these commands:
   cd csv_search_engine
   pip3.9 install --user -r requirements.txt
   python3.9 src/build_index.py

## Step 3: Set Up Web App
1. Go to 'Web' tab
2. Click 'Add a new web app'
3. Choose 'Manual configuration'
4. Select Python 3.9
5. In the WSGI file, replace the content with pythonanywhere_wsgi.py content
6. Update the path in the WSGI file to match your username

## Step 4: Configure Web App
- Source code: /home/yourusername/csv_search_engine
- Working directory: /home/yourusername/csv_search_engine
- WSGI file: /var/www/yourusername_pythonanywhere_com_wsgi.py

## Step 5: Reload Web App
Click 'Reload' button in the Web tab

## Access Your App
Your app will be live at: https://yourusername.pythonanywhere.com

## Troubleshooting
- Check the error log in the Web tab
- Make sure all dependencies are installed
- Verify the search index was built successfully
- Check file permissions
"""
    
    with open(deploy_dir / "PYTHONANYWHERE_INSTRUCTIONS.md", "w") as f:
        f.write(instructions)

def main():
    """Main function"""
    print("🐍 PythonAnywhere Deployment Package Creator")
    print("=" * 50)
    
    zip_file = create_deployment_package()
    
    print(f"\n📦 Package created: {zip_file}")
    print("\n📋 Next steps:")
    print("1. Go to https://www.pythonanywhere.com")
    print("2. Sign up for a free account")
    print("3. Upload the ZIP file")
    print("4. Follow the instructions in PYTHONANYWHERE_INSTRUCTIONS.md")
    print("\n🎉 Your CSV Search Engine will be live online!")

if __name__ == "__main__":
    main()
