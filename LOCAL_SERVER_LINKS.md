# Local Server Links

## 🚀 Access Your Chatbot

After running `python main.py`, use these links to access your local server:

---

## 🌐 Main Chatbot Interface

### Primary URL
```
http://localhost:8000
```

**Copy and paste into your browser:**
```
http://localhost:8000/
```

### Alternative (Using IP Address)
```
http://127.0.0.1:8000
```

---

## 📡 API Endpoints

### Health Check
```
http://localhost:8000/api/health
```
Returns system status and initialization status.

**Example Response:**
```json
{
  "status": "healthy",
  "service": "Claude Code RAG Chatbot",
  "rag_initialized": true
}
```

### Initialize Database
```
POST http://localhost:8000/api/initialize
```
Rebuild the vector database with chapters.

### Query Endpoint
```
POST http://localhost:8000/api/query
```
Send chat queries (use the web interface for this).

---

## 🎯 Quick Access Guide

### Step 1: Start the Server
```bash
python main.py
```

You should see:
```
==================================================
Claude Code RAG Chatbot
==================================================
Server starting on http://localhost:8000
Open your browser to http://localhost:8000
==================================================
```

### Step 2: Click or Copy One of These Links

**Option A: Direct localhost**
```
http://localhost:8000
```

**Option B: IP address**
```
http://127.0.0.1:8000
```

**Option C: With trailing slash**
```
http://localhost:8000/
```

### Step 3: Enjoy the Chat!

---

## 💡 Common Access Methods

### Copy & Paste Ready Links

**For Chrome/Firefox/Edge:**
```
http://localhost:8000
```

**For Safari/Mobile:**
```
http://127.0.0.1:8000
```

**For Terminal/Command Line:**
```bash
# Linux/Mac - open in default browser
open http://localhost:8000

# Windows - open in default browser
start http://localhost:8000

# Or type in address bar:
localhost:8000
```

---

## 🔗 All Available Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Chat interface (HTML) |
| `/api/query` | POST | Submit questions |
| `/api/health` | GET | System health check |
| `/api/initialize` | POST | Rebuild database |
| `/static/style.css` | GET | CSS styling |

---

## 📱 Access from Different Devices

### Same Computer
```
http://localhost:8000
http://127.0.0.1:8000
```

### From Another Computer on Network
First, find your computer's IP:

**Windows:**
```bash
ipconfig
```
Look for "IPv4 Address"

**Linux/Mac:**
```bash
ifconfig
```
Look for "inet"

Then use:
```
http://<your-ip>:8000
```

**Example:**
```
http://192.168.1.100:8000
```

---

## 🐛 Troubleshooting Connection

### "Connection refused" error?
1. Make sure server is running: `python main.py`
2. Check for error messages in terminal
3. Try waiting a few seconds for startup

### "Page not found"?
1. Verify you're using correct URL: `http://localhost:8000`
2. Check trailing slash: `/` or no slash both work
3. Clear browser cache (Ctrl+Shift+Delete)

### Server won't start?
1. Check Python installed: `python --version`
2. Check dependencies: `pip install -r requirements.txt`
3. Check API key in `.env` file
4. Try different port: Edit `.env`, change `PORT=8000` to `PORT=8001`

### Port already in use?
If port 8000 is busy, edit `.env`:
```
PORT=8001
```

Then access at:
```
http://localhost:8001
```

---

## 🎮 Browser Tips

### Fastest Access
1. Type in address bar: `localhost:8000` (no http:// needed)
2. Press Enter

### Bookmark It
Save these URLs as bookmarks in your browser:
- `http://localhost:8000` - Main chat
- `http://localhost:8000/api/health` - Health check

### Keyboard Shortcuts
- **Ctrl+L** - Focus address bar
- **Ctrl+R** - Refresh page
- **F12** - Open developer tools (for debugging)

---

## 📊 Monitoring

### Check if Server is Running
```bash
curl http://localhost:8000/api/health
```

Should return JSON:
```json
{"status": "healthy", "service": "Claude Code RAG Chatbot", "rag_initialized": true}
```

### View Server Logs
Terminal output shows:
- Requests made
- Errors (if any)
- Database status
- Response times

---

## 🚀 Quick Links Card

**Save this for quick reference:**

```
╔════════════════════════════════════════╗
║     Claude Code RAG Chatbot            ║
╠════════════════════════════════════════╣
║  🌐 Main:    http://localhost:8000     ║
║  ✅ Status:  http://localhost:8000/    ║
║  📊 Health:  /api/health               ║
║  🔄 Init:    /api/initialize           ║
╠════════════════════════════════════════╣
║  Start:  python main.py                ║
║  Stop:   Ctrl+C in terminal            ║
╚════════════════════════════════════════╝
```

---

## 📝 Common Tasks

### View Chat Interface
```
http://localhost:8000
```

### Check System Health
```
http://localhost:8000/api/health
```

### Rebuild Database
Use HTTP POST tool or curl:
```bash
curl -X POST http://localhost:8000/api/initialize
```

### Change Port
Edit `.env`:
```
PORT=3000
```

Then access:
```
http://localhost:3000
```

---

## ✅ Verify Server Running

**In Terminal:**
```bash
# Shows: Connection established ✓
curl -I http://localhost:8000

# Or just try to access it in browser
http://localhost:8000
```

**In Browser:**
- Open: `http://localhost:8000`
- You should see the chat interface
- Try typing a question
- You should get a response from Claude

---

## 🎉 You're All Set!

**Use this link to access your chatbot:**

# 🌐 [http://localhost:8000](http://localhost:8000)

Or copy and paste into your browser:
```
http://localhost:8000
```

**Happy chatting!** 🚀
