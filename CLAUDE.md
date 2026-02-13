# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Start Commands

```bash
# Install dependencies (run once, takes 2-5 minutes)
# IMPORTANT: Always use uv for dependency management, never pip directly
uv sync

# Run the application (blocks terminal, visit http://localhost:8000)
# IMPORTANT: Always use uv to run the server
uv run python main.py

# Create/update .env configuration file
copy .env.example .env
notepad .env
# Add: OPENAI_API_KEY=sk-YOUR_KEY
```

## Architecture Overview

This is a **Retrieval-Augmented Generation (RAG) Chatbot** with clear separation of concerns:

```
Browser (HTML/CSS/JavaScript)
    ↕ HTTP REST API
FastAPI Server (main.py)
    ↓
RAG System (rag_system.py)
    ├─ ChromaDB (Vector Database)
    └─ OpenAI API
```

### Data Flow for a User Query

1. **Frontend** (templates/index.html): User types question → JavaScript captures it
2. **HTTP POST /api/query**: Sends `{"question": "..."}` to backend
3. **FastAPI** (main.py:query): Validates input, calls rag_system.query()
4. **Retrieval** (rag_system.py:retrieve_context):
   - Encodes question to embedding vector using sentence-transformers
   - Searches ChromaDB for top-3 most similar document chunks
5. **Generation** (rag_system.py:generate_response):
   - Formats retrieved chunks as context
   - Calls OpenAI API with context + question
   - Returns answer + sources
6. **Response**: FastAPI returns JSON with answer, sources, context_count
7. **Display** (JavaScript): Renders answer in chat with citations

### Document Processing Pipeline

- **Load**: Read .md files from `data/chapters/`
- **Chunk**: Split on `## Headers` to create logical sections
- **Embed**: Convert each chunk to 384-dimensional vector using all-MiniLM-L6-v2
- **Store**: Save embeddings + metadata in ChromaDB (persistent SQLite)
- **Retrieve**: Cosine similarity search for top-K chunks
- **Context**: Format chunks as "From Chapter X - Title Y: content" strings

## Project Structure

```
main.py                    # FastAPI app: routes, startup, response formatting
rag_system.py              # RAG core: retrieve + generate, ChromaDB, Claude API
templates/index.html       # Chat UI, sidebar, course navigation, message display
static/style.css           # Styling (purple/blue theme, responsive layout)
data/chapters/             # 5 markdown files (learning content)
data/chroma_db/            # ChromaDB vector database (auto-created, persistent)
requirements.txt           # Python dependencies
.env.example               # Configuration template (copy to .env)
```

## Key Code Paths

### Adding a New Chapter
1. Create `data/chapters/chapter6_topic.md` with `## Section Headers`
2. POST `/api/initialize` endpoint to rebuild embeddings
3. New content automatically available in RAG system

**Important**: Chapters are split on `##` headers. Structure markdown with headers to define logical chunks.

### Modifying the Chat UI
1. **Message styling**: Edit `.message` classes in static/style.css
2. **Chat layout**: Modify `<div class="chat-area">` in templates/index.html
3. **Course sidebar**: Change course cards in `<div class="courses-container">`
4. **Input handling**: JavaScript event listener at line ~290 in index.html

### Changing the Welcome Message
- Line 99 in templates/index.html: Initial bot message
- Line 228 in templates/index.html: "Ask Me Directly" mode message
- Both messages display code safety notice (lines 106-108, 233-236)

### Customizing the AI Model/Behavior
- **Model choice**: rag_system.py, change `model="gpt-3.5-turbo"` to another OpenAI model
- **System prompt**: rag_system.py, modify assistant instructions
- **Max tokens**: rag_system.py, adjust response length limit
- **Retrieval count**: rag_system.py, change `top_k=3` for more/fewer chunks

### API Response Structure
All queries return:
```python
{
    "answer": str,           # Generated response text
    "sources": list,         # Chapter names used in context
    "context_count": int     # Number of chunks retrieved (max 3)
}
```

## Important Implementation Details

### Embedding Model
- **Model**: sentence-transformers/all-MiniLM-L6-v2
- **Size**: 22M parameters, ~384-dimensional vectors
- **First load**: ~2 seconds (then cached)
- **Per-query**: ~10ms to encode question
- **Search**: Cosine similarity in ChromaDB (~50ms for 25 chunks)

### OpenAI API Calls
- **Model**: gpt-3.5-turbo (cost-effective and fast)
- **Latency**: ~2 seconds per request (network + inference)
- **Context window**: Up to 2048 tokens per response
- **Cost**: Pay-per-token via OpenAI API key (~$0.002 per 1K tokens)
- **Error handling**: Raised as HTTP 500 in FastAPI if API fails

### ChromaDB Persistent Storage
- **Location**: `data/chroma_db/chroma.sqlite3`
- **Auto-created**: On first server startup if missing
- **Survives restart**: Database persists between server restarts
- **Rebuild trigger**: POST `/api/initialize` or delete `data/chroma_db/`
- **Collection**: Named "claude_code_lessons", stores metadata + embeddings

### Frontend State Management
- **No framework**: Vanilla JavaScript, no React/Vue/Svelte
- **Event handling**: Form submit listener captures user input
- **DOM updates**: Direct appendChild() for messages
- **State**: Course selection tracked in `selectedCourse` variable
- **Auto-scroll**: Manual scroll-to-bottom after adding messages

## Configuration (.env)

```
OPENAI_API_KEY=sk-...               # Required: OpenAI API key
HOST=localhost                      # Optional: Server host (default: localhost)
PORT=8000                           # Optional: Server port (default: 8000)
```

**Gotchas**:
- API key is required; server won't start without it
- Port 8000 is default; change if already in use
- .env should NEVER be committed (add to .gitignore)

## Common Modifications

### Add Custom Course/Category
Modify `courses` array in templates/index.html (~line 155). Each course needs:
- `title`: Display name
- `icon`: Emoji icon
- `questions`: Array of suggested questions for that course

These are purely frontend; questions route through same RAG system.

### Change Model Provider
To use a different OpenAI model:
1. rag_system.py: Change model to "gpt-4" or another OpenAI model
2. System prompt remains the same
3. Costs and latencies will differ

### Adjust Retrieval Sensitivity
- More chunks: rag_system.py line 160, change `top_k=3` to `top_k=5`
- Will increase context size and API usage
- May improve relevance or increase noise

### Run Health Check
```python
# In Python REPL with cwd=repository
import requests
response = requests.get('http://localhost:8000/api/health')
print(response.json())  # Shows RAG initialization status
```

## Known Limitations & Gotchas

1. **First query is slow** (~2-3 seconds): Model loads on first embedding
2. **Subsequent queries fast** (~2-3 seconds): Still waiting for Claude API, not model
3. **ChromaDB single-threaded**: Concurrent requests may queue (fine for single user)
4. **No conversation memory**: Each query is independent, no multi-turn context
5. **HTML escaping in JS**: `escapeHtml()` function prevents XSS (important for safety)
6. **Markdown chunking**: Chapters MUST have `## Headers` to split properly; no headers = single chunk
7. **No authentication**: Anyone with access to localhost:8000 can query (local only)

## Testing & Validation

### Manual Testing
1. Start server: `uv run python main.py`
2. Open http://localhost:8000
3. Click each course card (verify suggestions load)
4. Click "Ask Me Directly" (verify mode switches)
5. Type a question and verify:
   - Loading state appears
   - Answer displays with sources
   - Status returns to "Ready"

### Check Database Status
```python
import chromadb
client = chromadb.PersistentClient(path="data/chroma_db")
coll = client.get_or_create_collection("claude_code_lessons")
print(f"Documents in DB: {coll.count()}")  # Should be ~25
```

### Test RAG System Directly
```python
from rag_system import RAGSystem
rag = RAGSystem()
result = rag.query("How do I read files?")
print(result['answer'])      # Generated response
print(result['sources'])     # Chapters used
```

## Performance Notes

| Operation | Time | Notes |
|-----------|------|-------|
| Server startup | 1-2 sec | Loads embedding model |
| First query (full) | 2-3 sec | Embedding + retrieval + Claude |
| Subsequent queries | 2-3 sec | ChromaDB fast, Claude API is bottleneck |
| Vector search | ~50ms | 25 chunks with cosine similarity |
| Question encoding | ~10ms | Sentence-Transformer model |
| Claude API call | ~2 sec | Network latency + inference |

## Dependencies & Versions

Critical dependencies (from requirements.txt):
- **fastapi==0.104.1**: Web framework (must match for type hints)
- **openai>=1.0.0**: OpenAI API client (may have breaking changes in newer versions)
- **chromadb==0.4.24**: Vector database (persistence format specific to version)
- **sentence-transformers==2.2.2**: Embedding model (changing version affects vector dimensions)

Updating versions may require retraining embeddings or data migration.
