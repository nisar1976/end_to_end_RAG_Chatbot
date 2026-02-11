# ✅ SETUP CHECKLIST - Track Your Progress

Use this checklist as you follow the setup steps. Mark each item as complete.

---

## 📋 Pre-Setup Verification

- [ ] **Python installed?**
  - Open terminal and type: `python --version`
  - Should show: Python 3.8 or higher

- [ ] **API Key obtained?**
  - Visit: https://console.anthropic.com/
  - Create API key (starts with: `sk-ant-api03-`)
  - Keep it copied to clipboard

- [ ] **Terminal open?**
  - Windows: Win + R → cmd → Enter
  - Mac: Cmd + Space → terminal → Enter
  - Should show a black/white window with cursor

- [ ] **In correct folder?**
  - Type in terminal: `cd C:\Users\Nisar\Desktop\end_to_end_RAG_Chatbot`
  - Type: `dir`
  - Should see: main.py, requirements.txt, .env.example
  - If you see these files: ✅

---

## 🔧 Installation

### Step 1: Install Dependencies
- [ ] **Command entered:**
  ```
  pip install -r requirements.txt
  ```

- [ ] **Installation started?**
  - Should show: "Collecting fastapi", "Collecting uvicorn", etc.

- [ ] **Installation complete?**
  - Wait 2-5 minutes
  - Should show: "Successfully installed fastapi uvicorn anthropic chromadb sentence-transformers python-dotenv"
  - If you see this: ✅

---

## ⚙️ Configuration

### Step 2: Create Configuration File
- [ ] **Command entered:**
  ```
  copy .env.example .env
  ```

- [ ] **File created?**
  - Type: `type .env`
  - Should show:
    ```
    ANTHROPIC_API_KEY=
    HOST=localhost
    PORT=8000
    ```
  - If you see this: ✅

### Step 3: Add API Key
- [ ] **Notepad opened:**
  ```
  notepad .env
  ```

- [ ] **API Key pasted?**
  - First line should now show:
    ```
    ANTHROPIC_API_KEY=sk-ant-api03-YOUR_ACTUAL_KEY
    ```

- [ ] **File saved?**
  - Press: Ctrl + S
  - Close notepad

- [ ] **Verified?**
  - Type: `type .env`
  - Should show your API key on first line
  - If you see this: ✅

---

## 🚀 Starting Server

### Step 4: Run the Server
- [ ] **Command entered:**
  ```
  python main.py
  ```

- [ ] **Server starting?**
  - Should show messages about loading the model
  - Progress bars appearing for embedding model

- [ ] **Server ready?**
  - Wait 1-2 minutes
  - Should see:
    ```
    INFO:     Application startup complete.
    INFO:     Uvicorn running on http://localhost:8000 (Press CTRL+C to quit)
    ```
  - If you see this: ✅

- [ ] **Terminal kept open?**
  - Do NOT close the terminal window
  - Keep it running while using chatbot
  - If terminal is still visible: ✅

---

## 🌐 Browser Access

### Step 5: Open in Browser
- [ ] **Browser opened?**
  - Chrome, Firefox, Safari, or Edge

- [ ] **URL entered:**
  ```
  http://localhost:8000
  ```

- [ ] **Page loaded?**
  - Should see "Claude Code RAG Chatbot" title
  - Should see text input box at bottom
  - Should see "Ask a question..." placeholder
  - Purple/blue themed interface
  - If you see this: ✅

---

## 💬 Testing the Chatbot

### Step 6: Ask a Question
- [ ] **Clicked in text box?**
  - Click the input field at bottom of page

- [ ] **Question typed?**
  - Type: "How do I read files in Claude Code?"

- [ ] **Question submitted?**
  - Press Enter or click Send button

- [ ] **Waiting for response?**
  - First query takes 1-2 minutes
  - You should see a loading indicator

- [ ] **Got answer?**
  - Should see:
    - Your question displayed
    - Chatbot's answer with explanation
    - "Sources:" section showing which chapters were used
  - If you see this: ✅

---

## 🎯 Success Indicators

All of these should be true:

- [ ] Terminal shows "Uvicorn running on http://localhost:8000"
- [ ] Browser shows chat interface at localhost:8000
- [ ] Can type questions in text box
- [ ] Chatbot responds with answers
- [ ] Answers show source citations
- [ ] No error messages in terminal

**If all checked: 🎉 You're all set!**

---

## ⚠️ Troubleshooting Checklist

If something went wrong, check these:

### Server won't start:
- [ ] Is Python 3.8+ installed? (`python --version`)
- [ ] Are dependencies installed? Check: "Successfully installed..." message
- [ ] Is API key in .env file? Check: `type .env`
- [ ] Is API key valid? (Check at console.anthropic.com)
- [ ] Are you in the right folder? Check: `dir` shows main.py

### Browser shows "Connection refused":
- [ ] Is terminal still open with server running?
- [ ] Does terminal show "Uvicorn running on http://localhost:8000"?
- [ ] Try different URL: http://127.0.0.1:8000
- [ ] Try port 8001 if port changed: http://localhost:8001

### Installation failed (pip install):
- [ ] Is Python in PATH? Try: `python -m pip install -r requirements.txt`
- [ ] Clear cache: `pip cache purge`
- [ ] Retry: `pip install --no-cache-dir -r requirements.txt`

### No module errors:
- [ ] Wait for `pip install` to completely finish (2-5 minutes)
- [ ] Try again: `pip install -r requirements.txt`
- [ ] Check internet connection

### API Key error:
- [ ] Open .env file: `notepad .env`
- [ ] First line must have: `ANTHROPIC_API_KEY=sk-ant-api03-YOUR_KEY`
- [ ] No quotes around the key
- [ ] No spaces at start or end
- [ ] Save file and restart server

---

## 📞 Getting Help

If you're stuck:

1. **Read these files:**
   - README.md (full documentation)
   - SETUP_STEPS.md (detailed walkthrough)
   - QUICK_START_CARD.md (quick reference)

2. **Check terminal error message:**
   - Red text in terminal shows what went wrong
   - Search for the error message in README.md Troubleshooting section

3. **Common solutions:**
   - Restart terminal and try again
   - Update Python to latest version
   - Reinstall dependencies: `pip install --upgrade -r requirements.txt`
   - Clear browser cache and refresh page

---

## 🎓 After Setup Complete

### Try these questions:
- [ ] "How do I read files in Claude Code?"
- [ ] "What is the Edit tool?"
- [ ] "How do I create a pull request?"
- [ ] "What are best practices for commits?"
- [ ] "Explain the Bash tool"

### Bookmark these for later:
- [ ] http://localhost:8000 (add to bookmarks)
- [ ] Keep terminal running whenever using chatbot

### To stop the server later:
- [ ] Press Ctrl + C in terminal window
- [ ] Type Y if asked
- [ ] Terminal will close

### To restart the server:
- [ ] Open new terminal
- [ ] Navigate to folder: `cd C:\Users\Nisar\Desktop\end_to_end_RAG_Chatbot`
- [ ] Run: `python main.py`

---

**Print this page and check off items as you complete them!**

**You've got this! 🚀**
