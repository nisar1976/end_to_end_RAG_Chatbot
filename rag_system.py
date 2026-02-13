import os
import glob
import re
from pathlib import Path
from typing import Optional

import yaml
import chromadb
from sentence_transformers import SentenceTransformer
from openai import OpenAI

# Import backend tools if available
try:
    from backend.search_tools import execute_tool
except ImportError:
    execute_tool = None


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

        # Initialize OpenAI client
        self.openai_client = OpenAI()

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

            # Extract YAML frontmatter and URL
            url = self._extract_frontmatter_url(content)

            # Remove YAML frontmatter from content before processing
            content = self._remove_frontmatter(content)

            # Split into chunks (approximate by splitting on ## headers)
            chunks = self._split_into_chunks(content, chapter_name)

            for chunk_idx, (chunk_title, chunk_text) in enumerate(chunks):
                if chunk_text.strip():
                    chunk_id = f"{chapter_name}_chunk_{chunk_idx}"
                    self.documents[chunk_id] = {
                        'chapter': chapter_name,
                        'title': chunk_title,
                        'content': chunk_text,
                        'url': url
                    }
                    doc_count += 1

        return doc_count

    def _extract_frontmatter_url(self, content: str) -> str:
        """Extract URL from YAML frontmatter in markdown.

        Args:
            content: Full document content

        Returns:
            URL string, or empty string if not found
        """
        if not content.startswith('---'):
            return ''

        try:
            # Find the closing --- of frontmatter
            lines = content.split('\n')
            end_idx = -1
            for i in range(1, len(lines)):
                if lines[i].startswith('---'):
                    end_idx = i
                    break

            if end_idx == -1:
                return ''

            # Extract YAML content
            yaml_content = '\n'.join(lines[1:end_idx])
            frontmatter = yaml.safe_load(yaml_content)

            if frontmatter and isinstance(frontmatter, dict):
                return frontmatter.get('url', '')
            return ''
        except Exception:
            return ''

    def _remove_frontmatter(self, content: str) -> str:
        """Remove YAML frontmatter from markdown content.

        Args:
            content: Full document content

        Returns:
            Content without frontmatter
        """
        if not content.startswith('---'):
            return content

        try:
            lines = content.split('\n')
            for i in range(1, len(lines)):
                if lines[i].startswith('---'):
                    # Return content after the closing ---
                    return '\n'.join(lines[i+1:])
            return content
        except Exception:
            return content

    def _split_into_chunks(self, content: str, chapter_name: str) -> list:
        """Split document content into logical chunks.

        Splits on ## headers while respecting code block boundaries.

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
        in_code_block = False

        for line in lines:
            # Track code block boundaries (triple backticks)
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                current_chunk.append(line)
                continue

            # Check for header (## with optional space) - but only outside code blocks
            if not in_code_block and re.match(r'^##\s*\S', line):
                # Start of new section
                if current_chunk:
                    chunk_text = '\n'.join(current_chunk)
                    chunks.append((current_title, chunk_text))
                    current_chunk = []
                # Extract title from header (remove ## and whitespace)
                current_title = re.sub(r'^##\s*', '', line).strip()
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
                    'url': doc.get('url', '')
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
                'url': metadata.get('url', ''),
                'relevance': 1 - (distance / 2) if distance else 0.8  # Convert distance to relevance
            })

        return context

    def generate_response(self, query: str, context: list) -> tuple:
        """Generate response using OpenAI API with retrieved context.

        Args:
            query: User query
            context: Retrieved context chunks

        Returns:
            Tuple of (response_text, sources_list)
        """
        # Format context
        context_text = ""
        sources = []
        seen_chapters = set()

        if context:
            context_text = "\n\n".join([
                f"From {item['chapter']} - {item['title']}:\n{item['content']}"
                for item in context
            ])
            # Build sources list with unique chapters and their URLs
            for item in context:
                if item['chapter'] not in seen_chapters:
                    sources.append({
                        'chapter': item['chapter'],
                        'url': item.get('url', '')
                    })
                    seen_chapters.add(item['chapter'])

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

        # Call OpenAI API
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            max_tokens=1024,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )

        return response.choices[0].message.content, sources

    def generate_response_with_tools(self, query: str, tools: list = None, max_iterations: int = 5) -> tuple:
        """Generate response using Claude API with tool calling.

        Args:
            query: User query
            tools: List of tool definitions in Anthropic format
            max_iterations: Maximum number of tool calling iterations

        Returns:
            Tuple of (response_text, sources_list, tool_calls_made)
        """
        if execute_tool is None:
            raise RuntimeError("Tool calling not available. Backend module not imported.")

        if not tools:
            tools = []

        # Build system prompt with tool descriptions
        system_prompt = """You are a helpful assistant specializing in Claude Code.
You have access to tools to help answer questions:

1. **search_content**: Search the documentation for specific information
   - Use when: User asks "how to", needs details about a feature, or wants examples

2. **get_course_outline**: Get the structure and lesson list for a course
   - Use when: User asks "what's in chapter X", "show me topics", or wants navigation

Guidelines:
- You can use both tools in sequence if needed
- Always cite sources when presenting search results
- Format course outlines clearly with lesson numbers and titles
- Be concise and practical"""

        # Initialize conversation
        messages = [
            {"role": "user", "content": query}
        ]

        tool_calls_made = []
        current_iteration = 0

        while current_iteration < max_iterations:
            current_iteration += 1

            # Call OpenAI API with tools
            messages_with_system = [
                {"role": "system", "content": system_prompt}
            ] + messages

            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                max_tokens=1024,
                tools=tools,
                messages=messages_with_system
            )

            # Check stop reason
            if response.stop_reason == "tool_use":
                # Extract tool use blocks
                assistant_content = response.content

                # Add assistant response to messages
                messages.append({
                    "role": "assistant",
                    "content": assistant_content
                })

                # Process each tool use block
                tool_results = []
                for content_block in assistant_content:
                    if content_block.type == "tool_use":
                        tool_name = content_block.name
                        tool_input = content_block.input
                        tool_use_id = content_block.id

                        # Execute tool
                        tool_result = execute_tool(tool_name, tool_input, self)

                        # Track tool call
                        tool_calls_made.append({
                            "tool": tool_name,
                            "input": tool_input,
                            "result_summary": str(tool_result)[:200] if isinstance(tool_result, dict) else str(tool_result)[:200]
                        })

                        # Add tool result to messages
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": tool_use_id,
                            "content": str(tool_result)
                        })

                # Add tool results as user message
                if tool_results:
                    messages.append({
                        "role": "user",
                        "content": tool_results
                    })

            elif response.stop_reason == "end_turn":
                # Extract final response
                final_text = ""
                sources = []

                for content_block in response.content:
                    if hasattr(content_block, 'text'):
                        final_text += content_block.text

                # Extract sources from tool calls if any search_content calls were made
                for tool_call in tool_calls_made:
                    if tool_call['tool'] == 'search_content':
                        # Try to extract sources from the tool result
                        # This is a simplified approach - sources come from the search results
                        pass

                return final_text, sources, tool_calls_made

            else:
                # Unexpected stop reason
                break

        # Fallback if max iterations reached
        return "I encountered complexity processing your request. Please try rephrasing your question.", [], tool_calls_made

    def query(self, user_question: str, use_tools: bool = True) -> dict:
        """End-to-end RAG pipeline: retrieve context and generate response.

        Args:
            user_question: Question from user
            use_tools: Whether to use tool calling (default True)

        Returns:
            Dictionary with answer, sources, context_count, and optional tool_calls
        """
        if use_tools and execute_tool is not None:
            # Use tool calling approach
            try:
                from backend.search_tools import TOOLS
                answer, sources, tool_calls = self.generate_response_with_tools(
                    user_question,
                    tools=TOOLS,
                    max_iterations=5
                )
                return {
                    'answer': answer,
                    'sources': sources,
                    'context_count': len(sources),
                    'tool_calls': tool_calls
                }
            except Exception as e:
                # Fall back to traditional RAG on tool calling error
                print(f"Tool calling failed, falling back to traditional RAG: {e}")
                pass

        # Traditional RAG pipeline (fallback or when use_tools=False)
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
