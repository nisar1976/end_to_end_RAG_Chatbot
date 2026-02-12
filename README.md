# End-to-End RAG Chatbot for Claude Code

A complete Retrieval-Augmented Generation (RAG) chatbot system that serves a web interface on a local server. The chatbot answers questions about Claude Code using sample lesson chapters stored in a vector database.

---

## 📍 Quick Navigation - Find Your Answer

**First time setting up?**
→ Go to **[Detailed Step-by-Step Setup Guide](#-detailed-step-by-step-setup-guide)** (Best for beginners)

**Already installed, getting an error?**
→ Go to **[Troubleshooting](#-troubleshooting)** (Specific error solutions)

**Just want quick summary?**
→ Go to **[Quick Start (Summary)](#-quick-start-summary)** (5 minute version)

**Server is running, how do I use it?**
→ Go to **[Example Questions](#-example-questions)** (Try these queries)

**Want to understand how it works?**
→ Go to **[Architecture](#-architecture)** (Technical details)

---

## 🎯 Features

- ✅ **Local FastAPI Server** - Runs on `http://localhost:8000`
- ✅ **RAG System** - Semantic search using ChromaDB and sentence-transformers
- ✅ **Claude API Integration** - Powered by Anthropic's Claude Opus 4.6
- ✅ **Vector Database** - ChromaDB for efficient document retrieval
- ✅ **Sample Lessons** - 5 comprehensive Claude Code learning chapters
- ✅ **Modern Web UI** - Clean, responsive chat interface
- ✅ **Source Citations** - Shows which chapters provided the answer
- ✅ **Easy Setup** - Simple installation and configuration

## 🎨 Interface Preview

![RAG Chatbot Interface](rag-chatbot-interface.png)

**Beautiful, intuitive chat interface with:**
- Sidebar course navigation with 5 learning paths
- Real-time chat messaging system
- Interactive learning modules
- Clean, modern UI design

## 📋 Prerequisites

- **Python 3.8+** - Required for FastAPI and dependencies
- **Anthropic API Key** - Get from https://console.anthropic.com/
- **10-15 minutes** - For initial setup and first run

## 🚀 Detailed Step-by-Step Setup Guide

### ⚠️ Prerequisites Check

Before starting, verify you have:
1. **Python 3.8+** installed on your system
2. **Anthropic API Key** from https://console.anthropic.com/

#### Check if Python is installed:

**Windows (Command Prompt):**
```bash
python --version
```

**Mac/Linux (Terminal):**
```bash
python3 --version
```

If you see a version number (e.g., `Python 3.10.0`), you're good! If not, download from https://www.python.org/

---

### Step 1: Open Terminal/Command Prompt

#### **Windows:**
1. Press `Win + R`
2. Type `cmd` and press Enter
3. You should see a black window with a cursor

#### **Mac:**
1. Press `Cmd + Space`
2. Type `terminal` and press Enter

#### **Linux:**
- Open your Terminal application

---

### Step 2: Navigate to Project Directory

Copy and paste this command (Windows, Mac, or Linux):

```bash
cd C:\Users\Nisar\Desktop\end_to_end_RAG_Chatbot
```

**Check you're in the right place:**
```bash
dir
```

You should see these files:
- `main.py`
- `rag_system.py`
- `requirements.txt`
- `README.md`
- `.env.example`

If you see these files, you're in the right directory! ✅

---

### Step 3: Install Python Dependencies

Run this command in your terminal:

```bash
pip install -r requirements.txt
```

**What you should see:**
```
Collecting fastapi
  Downloading fastapi-0.104.1-py3-none-any.whl (92 kB)
Collecting uvicorn
  Downloading uvicorn-0.24.0-py3-none-any.whl (60 kB)
...
Successfully installed fastapi-0.104.1 uvicorn-0.24.0 ...
```

**⚠️ Common Errors & Solutions:**

| Error | Solution |
|-------|----------|
| `'pip' is not recognized` | Python not in PATH. Restart terminal or reinstall Python with "Add Python to PATH" checked |
| `Could not find a version` | Try `pip install --upgrade pip` first, then retry |
| `Permission denied` | Use `pip install --user -r requirements.txt` |
| `Command exited with code 1` | Clear pip cache: `pip cache purge` then retry |

**If installation succeeds, you'll see:**
```
Successfully installed fastapi uvicorn anthropic chromadb sentence-transformers python-dotenv
```

---

### Step 4: Set Up the .env File (API Key)

**Option A: Using Windows Command Prompt (Easiest)**

1. Copy this entire command and paste it in your terminal:

```bash
copy .env.example .env
```

**Check it worked:**
```bash
type .env
```

You should see:
```
ANTHROPIC_API_KEY=
HOST=localhost
PORT=8000
```

2. Now open the `.env` file to add your API key:

```bash
notepad .env
```

3. Replace the `ANTHROPIC_API_KEY=` line with:
```
ANTHROPIC_API_KEY=sk-ant-api03-YOUR_ACTUAL_KEY_HERE
```

4. Save and close (Ctrl+S, then close window)

**Option B: Using Explorer (If Command Fails)**

1. Open File Explorer
2. Go to: `C:\Users\Nisar\Desktop\end_to_end_RAG_Chatbot`
3. Find `.env.example` file
4. Right-click → Copy
5. Right-click in empty space → Paste
6. Rename the copied file to `.env`
7. Right-click `.env` → Open with Notepad
8. Add your API key on the first line:
```
ANTHROPIC_API_KEY=sk-ant-api03-YOUR_ACTUAL_KEY_HERE
```
9. Save and close

**⚠️ Where to get your API Key:**

1. Go to https://console.anthropic.com/
2. Sign in or create account
3. Click "API Keys" in left sidebar
4. Click "Create Key"
5. Copy the entire key (starts with `sk-ant-api03-`)
6. Paste it into your `.env` file

**Verify .env is correct:**

In terminal, run:
```bash
type .env
```

Should output:
```
ANTHROPIC_API_KEY=sk-ant-api03-YOUR_KEY_HERE
HOST=localhost
PORT=8000
```

---

### Step 5: Run the Server

In your terminal, type:

```bash
python main.py
```

**What you should see (takes 1-2 minutes on first run):**

```
==================================================
Claude Code RAG Chatbot
==================================================
Server starting on http://localhost:8000
Open your browser to http://localhost:8000
==================================================

[stderr] C:\Users\Nisar\Desktop\end_to_end_RAG_Chatbot\main.py:34: DeprecationWarning: on_event is deprecated...
INFO:     Started server process [17796]
INFO:     Waiting for application startup.
Loading weights:   0%|          | 0/103 [00:00<?, ?it/s]...
Loading weights: 100%|##########| 103/103 [00:00<00:00, 1773.13it/s]
INFO:     Application startup complete.
INFO:     Uvicorn running on http://localhost:8000 (Press CTRL+C to quit)
```

**⚠️ If you see errors:**

| Error | What to do |
|-------|-----------|
| `ModuleNotFoundError: No module named 'fastapi'` | Run `pip install -r requirements.txt` again |
| `ERROR: ANTHROPIC_API_KEY not set in environment variables` | Your `.env` file is missing or API key is blank. Check Step 4 |
| `Port 8000 already in use` | Another program uses port 8000. See Troubleshooting section |
| `ImportError: cannot import name 'ValidationError'` | Run `pip install --upgrade -r requirements.txt` |

**✅ Server is running when you see:**
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://localhost:8000 (Press CTRL+C to quit)
```

---

### Step 6: Open the Chatbot in Your Browser

1. Open your web browser (Chrome, Firefox, Safari, Edge)
2. Go to: **http://localhost:8000**

**You should see:**
- A chat interface with "Claude Code RAG Chatbot" at the top
- A text input box at the bottom saying "Ask a question..."
- A clean, purple-blue themed interface

3. Type a question like:
```
How do I read files in Claude Code?
```

4. Press Enter or click the Send button

5. Wait 2-5 seconds for the answer (first query takes longer as it loads models)

---

### Step 7: Keep Server Running

**Important:** Keep the terminal window open while using the chatbot. The server must stay running.

To stop the server later:
- Press `Ctrl+C` in the terminal

To restart:
- Follow Step 5 again

---

## 🚀 Quick Start (Summary)

If you've already done the detailed setup, here's the quick version:

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `anthropic` - Claude API client
- `chromadb` - Vector database
- `sentence-transformers` - Embedding model
- `python-dotenv` - Environment variable management

### Step 2: Configure API Key

1. Copy the environment template:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=sk-ant-api03-YOUR_KEY_HERE
   ```

### Step 3: Run the Server

```bash
python main.py
```

Expected output:
```
==================================================
Claude Code RAG Chatbot
==================================================
Server starting on http://localhost:8000
Open your browser to http://localhost:8000
==================================================
...
INFO:     Application startup complete.
INFO:     Uvicorn running on http://localhost:8000 (Press CTRL+C to quit)
```

### Step 4: Open in Browser

Click the link or navigate to: **http://localhost:8000**

## 💬 Example Questions

Try asking the chatbot:

1. **Tools & Features**
   - "How do I read files in Claude Code?"
   - "What are the main tools available?"
   - "Explain the Bash tool"

2. **File Operations**
   - "How do I create a new file?"
   - "What's the best way to edit code?"
   - "Can I read PDF files?"

3. **Git Workflow**
   - "What are best practices for commits?"
   - "How do I create a pull request?"
   - "How do I fix a merge conflict?"

4. **Best Practices**
   - "What should I do before editing a file?"
   - "How do I debug efficiently?"
   - "What are performance optimization tips?"

## 📁 Project Structure

```
end_to_end_RAG_Chatbot/
├── main.py                    # FastAPI application & routes
├── rag_system.py              # RAG logic (retrieval + generation)
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
├── README.md                 # This file
├── data/
│   ├── chapters/             # Learning material
│   │   ├── chapter1_getting_started.md
│   │   ├── chapter2_tools_overview.md
│   │   ├── chapter3_file_operations.md
│   │   ├── chapter4_git_workflow.md
│   │   └── chapter5_best_practices.md
│   └── chroma_db/            # Vector database (auto-created)
├── static/
│   └── style.css             # Chat UI styling
└── templates/
    └── index.html            # Chat interface
```

## 🏗️ Architecture

### Backend Components

**1. RAG System (`rag_system.py`)**
- Loads and processes markdown chapters
- Generates embeddings using `sentence-transformers`
- Stores vectors in ChromaDB for fast retrieval
- Implements semantic search for relevant context
- Integrates with Claude API for response generation

**2. FastAPI Server (`main.py`)**
- RESTful API endpoints
- Serves static files and HTML templates
- Health check endpoint
- Database initialization endpoint

### Frontend Components

**1. HTML Interface (`templates/index.html`)**
- Chat message display
- Real-time message rendering
- User and bot message differentiation
- Source citations display

**2. CSS Styling (`static/style.css`)**
- Purple/blue gradient theme
- Responsive design for all devices
- Smooth animations
- Accessible color contrasts

## 🔧 API Endpoints

### GET `/`
Serves the main chat interface (index.html)

### GET `/api/health`
Health check endpoint
```json
{
  "status": "healthy",
  "service": "Claude Code RAG Chatbot",
  "rag_initialized": true
}
```

### POST `/api/query`
Handle chat queries
- **Request**: `{"question": "How do I read files?"}`
- **Response**:
  ```json
  {
    "answer": "To read files in Claude Code...",
    "sources": ["chapter3_file_operations"],
    "context_count": 3
  }
  ```

### POST `/api/initialize`
Initialize or rebuild the vector database
- **Response**:
  ```json
  {
    "status": "success",
    "documents_loaded": 25,
    "embeddings_created": 25,
    "message": "RAG system initialized with 25 documents"
  }
  ```

## 📚 Learning Content

The system includes 5 comprehensive chapters:

1. **Chapter 1: Getting Started**
   - Installation & setup
   - Authentication
   - First commands
   - Configuration

2. **Chapter 2: Tools Overview**
   - Read, Write, Edit tools
   - Bash and Grep tools
   - Glob for file finding
   - Tool combinations

3. **Chapter 3: File Operations**
   - Reading files
   - Creating new files
   - Editing with precision
   - Structured file operations
   - Batch operations

4. **Chapter 4: Git Workflow**
   - Commits and branches
   - Collaboration workflows
   - Pull requests
   - Common workflows
   - Troubleshooting

5. **Chapter 5: Best Practices**
   - Code organization
   - Testing & validation
   - Performance optimization
   - Security considerations
   - Debugging techniques

## 🔄 How RAG Works

1. **Document Loading** - Read markdown chapters from `data/chapters/`
2. **Chunking** - Split documents into logical sections
3. **Embedding** - Generate embeddings using sentence-transformers
4. **Storage** - Store embeddings in ChromaDB
5. **User Query** - Encode user question
6. **Retrieval** - Find top-3 most relevant chunks (cosine similarity)
7. **Context Building** - Format retrieved chunks as context
8. **Response Generation** - Call Claude API with context + question
9. **Citation** - Extract and display source chapters

## 🛠️ Troubleshooting

### ❌ "ERROR: ANTHROPIC_API_KEY not set in environment variables"

**What this means:** The server can't find your API key

**Solutions:**

1. **Check if .env file exists:**
   ```bash
   dir .env
   ```

   If you see `.env` listed, go to step 2.
   If you don't see it, create it:
   ```bash
   copy .env.example .env
   ```

2. **Check if API key is in the file:**
   ```bash
   type .env
   ```

   Should show:
   ```
   ANTHROPIC_API_KEY=sk-ant-api03-YOUR_KEY
   HOST=localhost
   PORT=8000
   ```

3. **Verify API key is valid:**
   - Go to https://console.anthropic.com/
   - Get a new key if needed
   - Make sure key starts with `sk-ant-api03-`
   - No spaces or quotes around the key

4. **Edit .env file:**
   ```bash
   notepad .env
   ```

   Update first line to:
   ```
   ANTHROPIC_API_KEY=sk-ant-api03-YOUR_ACTUAL_KEY
   ```

   Save and close.

5. **Restart the server:**
   ```bash
   python main.py
   ```

---

### ❌ "'pip' is not recognized as an internal or external command"

**What this means:** Python or pip isn't installed properly

**Solutions:**

1. **Check Python installation:**
   ```bash
   python --version
   ```

   Should show version like `Python 3.10.0`

2. **If Python is installed, try:**
   ```bash
   python -m pip install -r requirements.txt
   ```

3. **If that doesn't work, reinstall Python:**
   - Download from https://www.python.org/
   - Run installer
   - ✅ IMPORTANT: Check the box "Add Python to PATH"
   - Restart your terminal after installation
   - Try `pip install -r requirements.txt` again

---

### ❌ "ModuleNotFoundError: No module named 'fastapi'" (or anthropic, chromadb, etc.)

**What this means:** Dependencies aren't installed

**Solutions:**

1. **Reinstall all dependencies:**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **Clear pip cache and retry:**
   ```bash
   pip cache purge
   pip install -r requirements.txt
   ```

3. **If still failing, try:**
   ```bash
   pip install -r requirements.txt --no-cache-dir
   ```

4. **Check requirements.txt exists:**
   ```bash
   type requirements.txt
   ```

   Should show list of packages

---

### ❌ "Port 8000 already in use" or "Address already in use"

**What this means:** Another program is using port 8000

**Solutions (Windows):**

1. **Use a different port:**
   ```bash
   notepad .env
   ```

   Change `PORT=8000` to `PORT=8001`

   Then access at: **http://localhost:8001**

2. **Or kill the process using port 8000:**
   ```bash
   netstat -ano | findstr :8000
   ```

   This shows something like:
   ```
   TCP  127.0.0.1:8000  0.0.0.0:0  LISTENING  12345
   ```

   The last number is the Process ID. Kill it:
   ```bash
   taskkill /PID 12345 /F
   ```

   Then try `python main.py` again

**Solutions (Mac/Linux):**

1. **Use a different port (same as above)**

2. **Or kill the process:**
   ```bash
   lsof -i :8000
   ```

   Shows the process. Kill it:
   ```bash
   kill -9 PID
   ```

---

### ❌ Server won't start or crashes immediately

**What you see:**
```
Traceback (most recent call last):
  File "main.py", line X, in <module>
    ...
```

**Solutions:**

1. **Restart terminal:**
   - Close terminal completely
   - Open new terminal
   - Navigate to directory again
   - Run `python main.py`

2. **Update dependencies:**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **Check for typos in .env:**
   ```bash
   type .env
   ```

   Make sure it has exactly:
   ```
   ANTHROPIC_API_KEY=sk-ant-api03-YOUR_KEY
   HOST=localhost
   PORT=8000
   ```

4. **Delete cached Python files:**
   ```bash
   rmdir /S __pycache__
   ```

   Then try again

---

### ❌ Browser shows "Connection refused" or "Unable to reach server"

**What this means:** Server isn't running

**Solutions:**

1. **Check terminal window:**
   - Is the terminal still open?
   - Do you see "Uvicorn running on http://localhost:8000"?

   If not, go back to Step 5 and run `python main.py` again.

2. **Try different URL:**
   - Instead of `localhost:8000`, try `http://127.0.0.1:8000`

3. **Verify correct port:**
   - Check your `.env` file for PORT setting
   - If PORT=8001, visit `http://localhost:8001`

4. **Restart everything:**
   - Stop server: Press `Ctrl+C` in terminal
   - Close terminal
   - Open new terminal
   - Navigate to directory
   - Run `python main.py` again
   - Visit `http://localhost:8000`

---

### ❌ "No such file or directory: data/chapters"

**What this means:** The data folder or chapters are missing

**Solutions:**

1. **Check if folders exist:**
   ```bash
   dir data
   dir data\chapters
   ```

2. **If missing, they're included in the project. They should be there. If not:**
   - Download the project again from GitHub
   - Or create the folders manually:
     ```bash
     mkdir data
     mkdir data\chapters
     ```

---

### ❌ "Slow responses" or "Takes forever to answer"

**What this means:** Normal behavior on first run, but might be slow for other reasons

**Solutions:**

1. **First query takes 1-2 minutes:**
   - The embedding model loads on first query
   - This is normal
   - Subsequent queries are 2-5 seconds

2. **If still slow after first query:**
   - Check internet connection
   - Check CPU/RAM usage
   - Try simpler questions
   - Restart server: Ctrl+C then `python main.py`

3. **Check API limits:**
   - Verify Anthropic API is working
   - Visit https://console.anthropic.com/ to check usage
   - Check you have remaining API quota

---

### ❌ "Browser shows error 'No such file or directory' for static files"

**What this means:** CSS or JS files aren't loading properly

**Solutions:**

1. **Check folders exist:**
   ```bash
   dir static
   dir templates
   ```

2. **Verify files are there:**
   ```bash
   dir static\style.css
   dir templates\index.html
   ```

3. **If files are missing, download the project again**

4. **Restart server:**
   - Ctrl+C to stop
   - `python main.py` to restart

---

### ❌ "DeprecationWarning: on_event is deprecated"

**What this means:** Just a warning, not an error. Can ignore it.

**This is safe to ignore.** The server still works fine. The warning is about FastAPI internals.

## 🚀 Deployment Considerations

For production use:

1. **Use environment variables** for all secrets
2. **Set up proper logging** for monitoring
3. **Add authentication** for API endpoints
4. **Use production ASGI server** (Gunicorn + Uvicorn)
5. **Store ChromaDB** in persistent volume
6. **Implement rate limiting** for API
7. **Add caching** for frequent queries
8. **Monitor token usage** for cost control

## 🤝 Extending the System

### Add More Content
1. Create markdown files in `data/chapters/`
2. POST `/api/initialize` to rebuild database
3. Chatbot will use new content automatically

### Customize Embeddings
Edit `rag_system.py`:
```python
self.embedding_model = SentenceTransformer("your-model-name")
```

### Change Language Model
Edit `rag_system.py`:
```python
response = self.anthropic_client.messages.create(
    model="claude-sonnet-4-5-20250929",  # Or another model
    ...
)
```

### Adjust Retrieval Parameters
Edit `main.py`:
```python
context = rag_system.retrieve_context(question, top_k=5)  # Get top 5 instead of 3
```

## 📊 Performance

- **Initial Load**: ~2 minutes (loads embedding model)
- **Response Time**: 2-5 seconds per query
- **Database Size**: ~50 MB for 25 documents
- **Memory Usage**: ~500 MB with model loaded
- **Concurrent Users**: 1+ (single-threaded by default)

## 🔒 Security Notes

- API key stored locally in `.env` (not in version control)
- `.env` should be added to `.gitignore`
- All user inputs are HTML-escaped
- No data stored on external servers
- ChromaDB data stored locally

## 📖 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [ChromaDB Guide](https://docs.trychroma.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [Anthropic API Docs](https://docs.anthropic.com/)
- [Claude Code Official Docs](https://github.com/anthropics/claude-code)

## 📝 License

This project is provided as-is for educational and development purposes.

## 🐛 Reporting Issues

If you encounter issues:

1. Check this README's troubleshooting section
2. Verify all dependencies are installed
3. Ensure API key is valid
4. Check the console output for error messages

## ✨ Future Enhancements

Potential improvements:
- Multi-turn conversation memory
- Document upload functionality
- Answer feedback and rating
- Query caching
- Response streaming
- Voice input/output
- Export conversation
- Advanced analytics

---

**Ready to get started?** Run `python main.py` and open http://localhost:8000 in your browser!
