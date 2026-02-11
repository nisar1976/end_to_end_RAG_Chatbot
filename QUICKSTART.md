# Quick Start Guide

Get the Claude Code RAG Chatbot running in 3 simple steps!

## Step 1: Install Dependencies (2 minutes)

```bash
pip install -r requirements.txt
```

This will install all required packages:
- FastAPI web framework
- ChromaDB vector database
- Sentence transformers for embeddings
- Anthropic SDK for Claude API
- And more...

**Note:** First installation may take a few minutes as it downloads the embedding model (~200MB).

## Step 2: Configure Your API Key (1 minute)

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Get your API key:
   - Go to https://console.anthropic.com/
   - Create or copy your API key

3. Edit `.env` and add your key:
   ```
   ANTHROPIC_API_KEY=sk_your_key_here
   ```

## Step 3: Run the Server (30 seconds)

```bash
python main.py
```

Wait for the startup message:
```
==================================================
Claude Code RAG Chatbot
==================================================
Server starting on http://localhost:8000
Open your browser to http://localhost:8000
==================================================
```

## Open the Chat Interface

Click on the link or open your browser to:
```
http://localhost:8000
```

## Start Chatting!

Try these example questions:

1. "How do I read files with Claude Code?"
2. "What are the best practices for git commits?"
3. "Can you explain the different tools available?"
4. "How do I edit files efficiently?"
5. "What's the recommended workflow for bug fixes?"

## First-Run Notes

- **First query may take 1-2 minutes** as the embedding model loads from disk
- Subsequent queries will be much faster (2-5 seconds)
- The vector database is automatically created in `data/chroma_db/`
- All chapter content is pre-loaded from `data/chapters/`

## Keyboard Shortcuts

- **Enter** - Send your message
- **Shift + Enter** - (For future multi-line support)

## Stop the Server

Press `Ctrl+C` in your terminal to stop the server.

## Troubleshooting

### Port 8000 is already in use?
Edit `.env` and change the PORT:
```
PORT=8001
```

### API Key error?
Make sure `.env` file exists and has your actual API key (not the example).

### "Module not found" error?
Reinstall dependencies:
```bash
pip install -r requirements.txt --upgrade
```

### Slow responses?
- First query loads the model (takes longer)
- Check your internet connection
- Restart the server if needed

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the chapter content in `data/chapters/`
- Customize the styling in `static/style.css`
- Extend with more chapters or content

## Getting Help

For detailed information:
- See [README.md](README.md) for architecture and API details
- Check the [5 Claude Code chapters](data/chapters/) for learning material
- Review error messages for specific issues

---

**Enjoy your Claude Code RAG Chatbot!** 🚀

Have fun exploring and learning about Claude Code features. The chatbot is powered by Claude AI and can answer virtually any question about the topics covered in the chapters.
