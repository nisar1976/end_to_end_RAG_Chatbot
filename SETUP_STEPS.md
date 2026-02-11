# 🚀 SETUP GUIDE - Follow These Steps

This guide walks you through starting the server step-by-step.

---

## STEP 1: Open Terminal/Command Prompt

### Windows:
1. Press: `Win + R`
2. Type: `cmd`
3. Press: `Enter`
4. You should see a black window

### Mac:
1. Press: `Cmd + Space`
2. Type: `terminal`
3. Press: `Enter`

### Linux:
- Open Terminal application from menu

---

## STEP 2: Go to Project Folder

Copy this command and paste in terminal:

```
cd C:\Users\Nisar\Desktop\end_to_end_RAG_Chatbot
```

Press: `Enter`

**Check:** Type `dir` and press Enter

You should see files like:
- main.py
- requirements.txt
- .env.example
- README.md

✅ If you see these files, you're in the right place!

---

## STEP 3: Install Required Programs

Copy this command and paste in terminal:

```
pip install -r requirements.txt
```

Press: `Enter`

**Wait** - this will take 2-5 minutes

**You should see:**
```
Collecting fastapi
Collecting uvicorn
...
Successfully installed fastapi uvicorn anthropic chromadb
```

✅ When you see "Successfully installed...", move to next step

---

## STEP 4: Create Configuration File

Copy this command and paste in terminal:

```
copy .env.example .env
```

Press: `Enter`

**Check:** Type `type .env` and press Enter

Should show:
```
ANTHROPIC_API_KEY=
HOST=localhost
PORT=8000
```

✅ If you see this, file was created!

---

## STEP 5: Add Your API Key

Copy this command and paste in terminal:

```
notepad .env
```

Press: `Enter`

A notepad window will open showing:
```
ANTHROPIC_API_KEY=
HOST=localhost
PORT=8000
```

### Add your API key:

1. Click at the end of first line (after `ANTHROPIC_API_KEY=`)
2. Paste your Anthropic API key (from https://console.anthropic.com/)
3. It should look like:
   ```
   ANTHROPIC_API_KEY=sk-ant-api03-YOUR_KEY_HERE
   ```

4. Press: `Ctrl + S` to save
5. Close the notepad window

✅ File is saved!

---

## STEP 6: Start the Server

Copy this command and paste in terminal:

```
python main.py
```

Press: `Enter`

**Wait** - first run takes 1-2 minutes (loading the model)

You should see:
```
==================================================
Claude Code RAG Chatbot
==================================================
Server starting on http://localhost:8000
Open your browser to http://localhost:8000
==================================================

INFO:     Application startup complete.
INFO:     Uvicorn running on http://localhost:8000
```

✅ When you see this message, the server is RUNNING!

**⚠️ IMPORTANT:** Keep this terminal window open! Don't close it while using the chatbot.

---

## STEP 7: Open in Browser

1. Open your web browser (Chrome, Firefox, Safari, Edge, etc.)
2. Go to this address:
   ```
   http://localhost:8000
   ```

3. Press: `Enter`

**You should see:**
- A chat interface
- "Claude Code RAG Chatbot" title
- A text box saying "Ask a question..."
- Purple/blue themed design

✅ You're in! The chatbot is ready to use!

---

## STEP 8: Ask a Question

1. Click in the text box at the bottom
2. Type a question:
   ```
   How do I read files in Claude Code?
   ```

3. Press: `Enter` or click Send button

4. Wait 2-5 seconds for the answer
   (First query might take longer)

5. You should see:
   - The question you asked
   - The chatbot's answer
   - Source chapters used

✅ It's working!

---

## STEP 9: Keep Using It

You can ask more questions anytime. The terminal must stay open.

### To stop the server:
- Click in terminal window
- Press: `Ctrl + C`
- Type: `Y` and press `Enter` if asked

### To restart the server:
- Run Step 6 again: `python main.py`

---

## 🎯 Example Questions to Try

- "How do I read files in Claude Code?"
- "What's the Edit tool?"
- "How do I create a pull request?"
- "What are best practices for commits?"
- "Explain the Bash tool"

---

## ⚠️ Something Went Wrong?

### Error: "ANTHROPIC_API_KEY not set"
- Your API key is missing from .env file
- Do Step 5 again (add your API key to the file)

### Error: "Port 8000 already in use"
- Another program uses port 8000
- Edit .env: change `PORT=8000` to `PORT=8001`
- Visit: `http://localhost:8001`

### Error: "'pip' is not recognized"
- Python isn't installed or in PATH
- Download Python from https://www.python.org/
- Run installer and CHECK "Add Python to PATH"
- Restart terminal and try again

### Error: "ModuleNotFoundError"
- Dependencies didn't install properly
- Run Step 3 again: `pip install -r requirements.txt`

### Browser shows "Connection refused"
- Server isn't running
- Check terminal window - do you see "Uvicorn running"?
- If not, run Step 6 again: `python main.py`
- If terminal closed, open new one and run Step 6

### Server is slow/taking forever
- This is normal on first run (loading models)
- First query takes 1-2 minutes
- Subsequent queries are 2-5 seconds

---

## ✅ You Did It!

Your chatbot is now running at **http://localhost:8000**

Enjoy using your AI-powered chatbot! 🎉

For more help, see README.md in the project folder.
