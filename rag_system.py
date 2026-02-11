import os
import glob
from pathlib import Path
from typing import Optional

import chromadb
from sentence_transformers import SentenceTransformer
from anthropic import Anthropic


class RAGSystem:
    """RAG System for Claude Code chatbot using ChromaDB and Anthropic API."""

    def __init__(self, db_path: str = "data/chroma_db", model_name: str = "all-MiniLM-L6-v2"):
        """Initialize the RAG system.

        Args:
            db_path: Path to ChromaDB storage
            model_name: Sentence transformer model name
        """
        self.db_path = db_path
        self.model_name = model_name

        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(
            name="claude_code_lessons",
            metadata={"hnsw:space": "cosine"}
        )

        # Initialize embedding model
        self.embedding_model = SentenceTransformer(model_name)

        # Initialize Anthropic client
        self.anthropic_client = Anthropic()

        # Store documents info
        self.documents = {}

    def load_documents(self, chapters_dir: str = "data/chapters") -> int:
        """Load markdown documents from chapters directory.

        Args:
            chapters_dir: Directory containing markdown chapter files

        Returns:
            Number of documents loaded
        """
        chapter_files = sorted(glob.glob(os.path.join(chapters_dir, "*.md")))

        if not chapter_files:
            raise FileNotFoundError(f"No markdown files found in {chapters_dir}")

        doc_count = 0

        for chapter_path in chapter_files:
            chapter_name = Path(chapter_path).stem

            with open(chapter_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Split into chunks (approximate by splitting on ## headers)
            chunks = self._split_into_chunks(content, chapter_name)

            for chunk_idx, (chunk_title, chunk_text) in enumerate(chunks):
                if chunk_text.strip():
                    chunk_id = f"{chapter_name}_chunk_{chunk_idx}"
                    self.documents[chunk_id] = {
                        'chapter': chapter_name,
                        'title': chunk_title,
                        'content': chunk_text
                    }
                    doc_count += 1

        return doc_count

    def _split_into_chunks(self, content: str, chapter_name: str) -> list:
        """Split document content into logical chunks.

        Args:
            content: Full document content
            chapter_name: Name of the chapter

        Returns:
            List of (title, text) tuples
        """
        chunks = []
        lines = content.split('\n')
        current_chunk = []
        current_title = chapter_name

        for line in lines:
            if line.startswith('## '):
                # Start of new section
                if current_chunk:
                    chunk_text = '\n'.join(current_chunk)
                    chunks.append((current_title, chunk_text))
                    current_chunk = []
                current_title = line.replace('## ', '').strip()
            else:
                current_chunk.append(line)

        # Add final chunk
        if current_chunk:
            chunk_text = '\n'.join(current_chunk)
            chunks.append((current_title, chunk_text))

        return chunks

    def create_embeddings(self) -> int:
        """Create embeddings for all documents and store in ChromaDB.

        Returns:
            Number of embeddings created
        """
        if not self.documents:
            raise ValueError("No documents loaded. Call load_documents() first.")

        # Clear existing collection
        if self.collection.count() > 0:
            # Get all IDs and delete
            all_data = self.collection.get()
            if all_data['ids']:
                self.collection.delete(ids=all_data['ids'])

        # Process documents in batches
        batch_size = 10
        doc_ids = list(self.documents.keys())

        for i in range(0, len(doc_ids), batch_size):
            batch_ids = doc_ids[i:i+batch_size]
            batch_docs = []
            batch_metadatas = []
            batch_embeddings = []

            for doc_id in batch_ids:
                doc = self.documents[doc_id]
                text = f"{doc['chapter']}: {doc['title']}\n{doc['content']}"

                # Generate embedding
                embedding = self.embedding_model.encode(text).tolist()

                batch_docs.append(text)
                batch_embeddings.append(embedding)
                batch_metadatas.append({
                    'chapter': doc['chapter'],
                    'title': doc['title'],
                })

            # Add to collection
            self.collection.add(
                ids=batch_ids,
                embeddings=batch_embeddings,
                documents=batch_docs,
                metadatas=batch_metadatas
            )

        return len(self.documents)

    def retrieve_context(self, query: str, top_k: int = 3) -> list:
        """Retrieve relevant context for a query.

        Args:
            query: User query
            top_k: Number of top results to return

        Returns:
            List of relevant document chunks with metadata
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query).tolist()

        # Search in ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        if not results['documents'] or not results['documents'][0]:
            return []

        # Format results
        context = []
        for i, doc in enumerate(results['documents'][0]):
            metadata = results['metadatas'][0][i]
            distance = results['distances'][0][i] if 'distances' in results else 0

            context.append({
                'content': doc,
                'chapter': metadata.get('chapter', 'Unknown'),
                'title': metadata.get('title', 'Unknown'),
                'relevance': 1 - (distance / 2) if distance else 0.8  # Convert distance to relevance
            })

        return context

    def generate_response(self, query: str, context: list) -> tuple:
        """Generate response using Claude API with retrieved context.

        Args:
            query: User query
            context: Retrieved context chunks

        Returns:
            Tuple of (response_text, sources_list)
        """
        # Format context
        context_text = ""
        sources = set()

        if context:
            context_text = "\n\n".join([
                f"From {item['chapter']} - {item['title']}:\n{item['content']}"
                for item in context
            ])
            sources = {item['chapter'] for item in context}

        # Build system prompt
        system_prompt = """You are a helpful assistant specializing in Claude Code.
You answer questions about Claude Code features, tools, and best practices.
Always cite the source chapters when providing information.
If you don't know the answer based on the provided context, say so clearly.
Be concise and practical in your responses."""

        # Build user message with context
        if context_text:
            user_message = f"""Based on the following Claude Code documentation:

{context_text}

---

Please answer this question: {query}"""
        else:
            user_message = f"Question: {query}\n\nNote: I don't have specific documentation on this topic."

        # Call Claude API
        response = self.anthropic_client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        return response.content[0].text, list(sources)

    def query(self, user_question: str) -> dict:
        """End-to-end RAG pipeline: retrieve context and generate response.

        Args:
            user_question: Question from user

        Returns:
            Dictionary with answer and sources
        """
        # Retrieve context
        context = self.retrieve_context(user_question)

        # Generate response
        answer, sources = self.generate_response(user_question, context)

        return {
            'answer': answer,
            'sources': sources,
            'context_count': len(context)
        }

    def initialize(self, chapters_dir: str = "data/chapters") -> dict:
        """Initialize the RAG system by loading and embedding documents.

        Args:
            chapters_dir: Directory containing chapter files

        Returns:
            Initialization status dictionary
        """
        try:
            # Load documents
            doc_count = self.load_documents(chapters_dir)

            # Create embeddings
            embed_count = self.create_embeddings()

            return {
                'status': 'success',
                'documents_loaded': doc_count,
                'embeddings_created': embed_count,
                'message': f'RAG system initialized with {embed_count} documents'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
