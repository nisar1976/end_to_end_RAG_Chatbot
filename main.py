import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

from rag_system import RAGSystem

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Claude Code RAG Chatbot", version="1.0.0")

# Initialize RAG system (global instance)
rag_system = None


class QueryRequest(BaseModel):
    """Request model for chat queries."""
    question: str


class QueryResponse(BaseModel):
    """Response model for chat queries."""
    answer: str
    sources: list
    context_count: int


@app.on_event("startup")
async def startup_event():
    """Initialize RAG system on startup."""
    global rag_system

    try:
        rag_system = RAGSystem()

        # Check if ChromaDB already has data
        if rag_system.collection.count() == 0:
            print("Loading and embedding documents...")
            result = rag_system.initialize("data/chapters")
            print(result['message'])
        else:
            print(f"ChromaDB already initialized with {rag_system.collection.count()} documents")

    except Exception as e:
        print(f"Error initializing RAG system: {e}")
        raise


@app.get("/")
async def root():
    """Serve the main chat interface."""
    return FileResponse("templates/index.html")


@app.get("/api/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Claude Code RAG Chatbot",
        "rag_initialized": rag_system is not None and rag_system.collection.count() > 0
    }


@app.post("/api/query")
async def query(request: QueryRequest):
    """Handle chat queries using RAG system.

    Args:
        request: QueryRequest with user question

    Returns:
        QueryResponse with answer and sources
    """
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")

    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        result = rag_system.query(request.question)
        return QueryResponse(
            answer=result['answer'],
            sources=result['sources'],
            context_count=result['context_count']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.post("/api/initialize")
async def initialize():
    """Initialize or rebuild the vector database.

    Returns:
        Initialization status
    """
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not available")

    try:
        result = rag_system.initialize("data/chapters")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initializing: {str(e)}")


# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


def main():
    """Run the application."""
    # Verify API key is set
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set in environment variables")
        print("Please copy .env.example to .env and add your API key")
        return

    # Get configuration from environment
    host = os.getenv("HOST", "localhost")
    port = int(os.getenv("PORT", 8000))

    print(f"\n{'='*50}")
    print("Claude Code RAG Chatbot")
    print(f"{'='*50}")
    print(f"Server starting on http://{host}:{port}")
    print(f"Open your browser to http://{host}:{port}")
    print(f"{'='*50}\n")

    # Run uvicorn server
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )


if __name__ == "__main__":
    main()
