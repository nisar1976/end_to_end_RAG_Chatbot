# ⚡ QUICK START REFERENCE CARD

**Print this and keep it handy!**

---

## 🎯 The 5 Commands You Need

### 1. Open Terminal
```
Windows: Win + R → type: cmd → Enter
Mac: Cmd + Space → type: terminal → Enter
```

### 2. Go to Folder
```
cd C:\Users\Nisar\Desktop\end_to_end_RAG_Chatbot
```

### 3. Install Programs
```
pip install -r requirements.txt
```
(Takes 2-5 minutes)

### 4. Create Config
```
copy .env.example .env
notepad .env
```
Then add your API key and save.

### 5. Start Server
```
python main.py
```
(Takes 1-2 minutes on first run)

### 6. Open Browser
```
http://localhost:8000
```

---

## 📋 Pre-Check List

Before starting, verify:

- ✅ Python installed? (`python --version`)
- ✅ API key obtained? (https://console.anthropic.com/)
- ✅ You're in right folder? (`dir` shows main.py)
- ✅ Terminal is open

---

## ⚠️ Common Issues & Quick Fixes

| Problem | Solution |
|---------|----------|
| "pip not found" | Reinstall Python with "Add to PATH" |
| "API Key error" | Check .env file has your real key |
| "Port in use" | Change PORT=8000 to PORT=8001 in .env |
| "Module not found" | Run: `pip install -r requirements.txt` again |
| "Connection refused" | Is terminal window still open? |
| "ModuleNotFoundError" | Wait for `pip install` to finish completely |

---

## 📊 What to Expect

| Action | Time | Expected Output |
|--------|------|-----------------|
| `pip install` | 2-5 min | "Successfully installed..." |
| First server start | 1-2 min | Embedding model loading |
| First query | 1-2 min | Takes time to load model |
| Normal queries | 2-5 sec | Quick responses |

---

## 🔍 Server Status Checklist

### Server is RUNNING when you see:
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://localhost:8000
```

### Server FAILED if you see:
```
ERROR: ANTHROPIC_API_KEY not set
ModuleNotFoundError
[Traceback...]
Address already in use
```

---

## 🌐 Browser Access

| Try this | If first fails |
|----------|---|
| http://localhost:8000 | http://127.0.0.1:8000 |
| Same but with port 8001 | If port changed in .env |

---

## 🛑 Emergency Stop

```
Ctrl + C
```
(In terminal window where server is running)

---

## 🔄 Restart After Stop

```
python main.py
```
(Same command as before)

---

## 📞 Need Help?

1. Read: `README.md` (full documentation)
2. Read: `SETUP_STEPS.md` (detailed walkthrough)
3. Check: "Troubleshooting" section in README

---

## 🎓 Example Questions

After server is running, ask the chatbot:

- "How do I read files in Claude Code?"
- "What is the Edit tool?"
- "How do I create a pull request?"
- "What are best practices for commits?"
- "Explain the Bash tool"

---

**Last Check Before Starting:**
- [ ] Terminal open
- [ ] Python version shown (3.8+)
- [ ] In correct folder (see main.py with `dir`)
- [ ] Have API key ready
- [ ] Browser bookmarked: http://localhost:8000

**You're ready to go! 🚀**
