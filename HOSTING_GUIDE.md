# 🚀 24/7 Hosting Guide for CSV Search Engine

This guide shows you multiple ways to host your CSV Search Engine 24/7.

## 🎯 Quick Start (Recommended)

### Option 1: Simple 24/7 Server
```bash
# Double-click this file or run in terminal:
start_24_7.bat
```

This will:
- ✅ Start the server with auto-restart
- ✅ Make it accessible from your network
- ✅ Auto-reload when you make changes
- ✅ Restart if it crashes

**Access URLs:**
- Local: `http://localhost:8501`
- Network: `http://YOUR_IP:8501`

---

## 🔧 Advanced Options

### Option 2: Windows Service (True 24/7)

**Step 1: Install Service Dependencies**
```bash
pip install pywin32
```

**Step 2: Install as Windows Service (Run as Administrator)**
```bash
python install_service.py install
```

**Step 3: Start the Service**
```bash
net start CSVSearchEngine
```

**Service Commands:**
- Start: `net start CSVSearchEngine`
- Stop: `net stop CSVSearchEngine`
- Remove: `python install_service.py remove`

---

### Option 3: Task Scheduler (Windows)

1. Open **Task Scheduler**
2. Create **Basic Task**
3. Set trigger: **At startup**
4. Action: **Start a program**
5. Program: `C:\Users\emaza\Desktop\csv_search_engine\start_24_7.bat`
6. ✅ **Run whether user is logged on or not**

---

### Option 4: Cloud Hosting

#### Streamlit Cloud (Free)
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy automatically

#### Heroku
1. Create `Procfile`:
```
web: streamlit run src/app.py --server.port $PORT --server.address 0.0.0.0
```

2. Deploy:
```bash
git init
git add .
git commit -m "Initial commit"
heroku create your-app-name
git push heroku main
```

#### Railway
1. Connect GitHub repository
2. Set build command: `pip install -r requirements.txt && python src/build_index.py`
3. Set start command: `streamlit run src/app.py --server.port $PORT`

---

## 🌐 Network Access

### Make Accessible from Other Devices

**Find Your IP Address:**
```bash
ipconfig
```

**Access from other devices:**
- Phone/Tablet: `http://YOUR_IP:8501`
- Other computers: `http://YOUR_IP:8501`

**Firewall Setup:**
1. Open **Windows Defender Firewall**
2. **Allow an app through firewall**
3. Add **Python** and **Streamlit**
4. Allow on **Private** and **Public** networks

---

## 🔍 Monitoring & Maintenance

### Check if Server is Running
```bash
# Check if port 8501 is in use
netstat -an | findstr 8501
```

### View Logs
- Service logs: **Event Viewer** → **Windows Logs** → **Application**
- Console logs: Check the terminal where you started the server

### Restart Server
```bash
# Kill existing process
taskkill /f /im streamlit.exe

# Start again
start_24_7.bat
```

---

## 🛠️ Troubleshooting

### Port Already in Use
```bash
# Find process using port 8501
netstat -ano | findstr 8501

# Kill the process (replace PID with actual number)
taskkill /f /pid PID_NUMBER
```

### Service Won't Start
1. Run **Command Prompt as Administrator**
2. Check service status: `sc query CSVSearchEngine`
3. View service logs in **Event Viewer**

### Can't Access from Network
1. Check Windows Firewall settings
2. Ensure server is bound to `0.0.0.0:8501`
3. Verify your IP address is correct

---

## 📊 Performance Tips

### For Large Datasets
- Use `--server.maxUploadSize 200` for larger files
- Consider using `faiss-gpu` instead of `faiss-cpu` if you have a GPU
- Increase memory: `--server.maxMessageSize 200`

### For Multiple Users
- Use a reverse proxy (nginx)
- Consider load balancing
- Monitor memory usage

---

## 🔒 Security Considerations

### For Production Use
1. **Enable Authentication:**
```python
# Add to app.py
import streamlit_authenticator as stauth
```

2. **Use HTTPS:**
```bash
streamlit run app.py --server.sslCertFile cert.pem --server.sslKeyFile key.pem
```

3. **Restrict Access:**
```bash
# Only allow local access
streamlit run app.py --server.address 127.0.0.1
```

---

## 🎉 Success!

Your CSV Search Engine is now running 24/7! 

**Quick Access:**
- Local: `http://localhost:8501`
- Network: `http://YOUR_IP:8501`

**Features Available:**
- ✅ Semantic search through 2,058 workflows
- ✅ Real-time similarity scoring
- ✅ JSON workflow viewer
- ✅ CSV export functionality
- ✅ Mobile-friendly interface

Happy searching! 🔍
