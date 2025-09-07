#!/usr/bin/env python3
"""
CSV Search Engine - Deploy Anywhere Script
This script helps you deploy your CSV search engine to various platforms
"""

import os
import json
import subprocess
import sys
from pathlib import Path

def create_deployment_files():
    """Create necessary files for deployment"""
    
    # Create Procfile for Heroku/Railway
    procfile_content = """web: streamlit run src/app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
release: python src/build_index.py"""
    
    with open("Procfile", "w") as f:
        f.write(procfile_content)
    
    # Create runtime.txt for Python version
    with open("runtime.txt", "w") as f:
        f.write("python-3.9.18")
    
    # Create .streamlit/config.toml for deployment
    os.makedirs(".streamlit", exist_ok=True)
    config_content = """[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false"""
    
    with open(".streamlit/config.toml", "w") as f:
        f.write(config_content)
    
    # Create app.yaml for Google Cloud
    app_yaml_content = """runtime: python39

env_variables:
  PORT: 8080

handlers:
- url: /.*
  script: auto"""
    
    with open("app.yaml", "w") as f:
        f.write(app_yaml_content)
    
    # Create Dockerfile
    dockerfile_content = """FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python src/build_index.py

EXPOSE 8501

CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]"""
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    
    # Create docker-compose.yml
    docker_compose_content = """version: '3.8'
services:
  csv-search:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
      - ./embeddings:/app/embeddings
    restart: unless-stopped"""
    
    with open("docker-compose.yml", "w") as f:
        f.write(docker_compose_content)
    
    print("✅ Deployment files created successfully!")

def deploy_to_streamlit_cloud():
    """Instructions for Streamlit Cloud deployment"""
    print("\n🌐 STREAMLIT CLOUD (FREE)")
    print("=" * 50)
    print("1. Push your code to GitHub")
    print("2. Go to https://share.streamlit.io")
    print("3. Click 'New app'")
    print("4. Connect your GitHub repository")
    print("5. Set main file path: src/app.py")
    print("6. Click 'Deploy!'")
    print("\nYour app will be live at: https://your-app-name.streamlit.app")

def deploy_to_heroku():
    """Instructions for Heroku deployment"""
    print("\n🚀 HEROKU")
    print("=" * 50)
    print("1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli")
    print("2. Login to Heroku: heroku login")
    print("3. Create app: heroku create your-app-name")
    print("4. Deploy:")
    print("   git init")
    print("   git add .")
    print("   git commit -m 'Initial commit'")
    print("   git push heroku main")
    print("\nYour app will be live at: https://your-app-name.herokuapp.com")

def deploy_to_railway():
    """Instructions for Railway deployment"""
    print("\n🚂 RAILWAY")
    print("=" * 50)
    print("1. Go to https://railway.app")
    print("2. Sign up with GitHub")
    print("3. Click 'New Project'")
    print("4. Select 'Deploy from GitHub repo'")
    print("5. Choose your repository")
    print("6. Railway will auto-detect and deploy!")
    print("\nYour app will be live at: https://your-app-name.railway.app")

def deploy_to_render():
    """Instructions for Render deployment"""
    print("\n🎨 RENDER")
    print("=" * 50)
    print("1. Go to https://render.com")
    print("2. Sign up with GitHub")
    print("3. Click 'New +' → 'Web Service'")
    print("4. Connect your GitHub repository")
    print("5. Set build command: pip install -r requirements.txt && python src/build_index.py")
    print("6. Set start command: streamlit run src/app.py --server.port $PORT --server.address 0.0.0.0")
    print("7. Click 'Create Web Service'")
    print("\nYour app will be live at: https://your-app-name.onrender.com")

def deploy_to_pythonanywhere():
    """Instructions for PythonAnywhere deployment"""
    print("\n🐍 PYTHONANYWHERE")
    print("=" * 50)
    print("1. Go to https://www.pythonanywhere.com")
    print("2. Create a free account")
    print("3. Go to 'Web' tab")
    print("4. Click 'Add a new web app'")
    print("5. Choose 'Manual configuration'")
    print("6. Select Python 3.9")
    print("7. Upload your files via 'Files' tab")
    print("8. Install dependencies in 'Consoles' tab:")
    print("   pip3.9 install --user -r requirements.txt")
    print("   python3.9 src/build_index.py")
    print("9. Set up WSGI file (see pythonanywhere_wsgi.py)")
    print("\nYour app will be live at: https://yourusername.pythonanywhere.com")

def create_pythonanywhere_wsgi():
    """Create WSGI file for PythonAnywhere"""
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
    
    with open("pythonanywhere_wsgi.py", "w") as f:
        f.write(wsgi_content)
    
    print("✅ Created pythonanywhere_wsgi.py")
    print("📝 Remember to update the path with your actual username!")

def deploy_to_google_colab():
    """Instructions for Google Colab deployment"""
    print("\n📊 GOOGLE COLAB (FREE)")
    print("=" * 50)
    print("1. Go to https://colab.research.google.com")
    print("2. Create a new notebook")
    print("3. Upload your files to Google Drive")
    print("4. Run this code in Colab:")
    print("""
!pip install streamlit pandas numpy sentence-transformers faiss-cpu
!streamlit run src/app.py --server.port 8501 --server.address 0.0.0.0
""")
    print("5. Use ngrok for public access:")
    print("!pip install pyngrok")
    print("from pyngrok import ngrok")
    print("public_url = ngrok.connect(8501)")
    print("print(public_url)")

def main():
    """Main deployment menu"""
    print("🚀 CSV SEARCH ENGINE - DEPLOY ANYWHERE")
    print("=" * 60)
    
    # Create deployment files
    create_deployment_files()
    create_pythonanywhere_wsgi()
    
    print("\nChoose your deployment platform:")
    print("1. Streamlit Cloud (FREE) - Recommended")
    print("2. Heroku (FREE tier available)")
    print("3. Railway (FREE tier available)")
    print("4. Render (FREE tier available)")
    print("5. PythonAnywhere (FREE tier available)")
    print("6. Google Colab (FREE)")
    print("7. Show all options")
    
    choice = input("\nEnter your choice (1-7): ").strip()
    
    if choice == "1":
        deploy_to_streamlit_cloud()
    elif choice == "2":
        deploy_to_heroku()
    elif choice == "3":
        deploy_to_railway()
    elif choice == "4":
        deploy_to_render()
    elif choice == "5":
        deploy_to_pythonanywhere()
    elif choice == "6":
        deploy_to_google_colab()
    elif choice == "7":
        deploy_to_streamlit_cloud()
        deploy_to_heroku()
        deploy_to_railway()
        deploy_to_render()
        deploy_to_pythonanywhere()
        deploy_to_google_colab()
    else:
        print("Invalid choice!")
    
    print("\n🎉 Deployment files created!")
    print("📁 Check the following files:")
    print("   - Procfile (for Heroku/Railway)")
    print("   - Dockerfile (for Docker deployment)")
    print("   - app.yaml (for Google Cloud)")
    print("   - .streamlit/config.toml (for Streamlit config)")
    print("   - pythonanywhere_wsgi.py (for PythonAnywhere)")

if __name__ == "__main__":
    main()
