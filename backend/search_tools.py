"""Tool definitions and implementations for the RAG system with tool calling support."""

import os
import glob
from pathlib import Path
from typing import Optional
import re

import yaml

# Module-level cache for course metadata
_course_metadata_cache = None
_cache_file_mtimes = None  # Track file modification times to invalidate cache


# Tool definitions in Anthropic format
def _get_chapter_file_mtimes(chapters_dir: str = "data/chapters") -> dict:
    """Get modification times for all chapter files.

    Args:
        chapters_dir: Directory containing markdown chapter files

    Returns:
        Dictionary mapping file path to modification time
    """
    file_mtimes = {}
    chapter_files = sorted(glob.glob(os.path.join(chapters_dir, "*.md")))

    for chapter_path in chapter_files:
        try:
            mtime = os.path.getmtime(chapter_path)
            file_mtimes[chapter_path] = mtime
        except OSError:
            pass

    return file_mtimes


def _cache_is_valid(chapters_dir: str = "data/chapters") -> bool:
    """Check if cached course metadata is still valid.

    Cache is invalid if:
    - No cache exists
    - Files have been added/removed
    - Files have been modified

    Args:
        chapters_dir: Directory containing markdown chapter files

    Returns:
        True if cache is valid, False otherwise
    """
    global _cache_file_mtimes

    if _course_metadata_cache is None:
        return False

    current_mtimes = _get_chapter_file_mtimes(chapters_dir)

    if _cache_file_mtimes is None:
        return False

    # Check if files have changed
    if set(current_mtimes.keys()) != set(_cache_file_mtimes.keys()):
        # Files added or removed
        return False

    # Check if any file was modified
    for filepath, current_mtime in current_mtimes.items():
        if _cache_file_mtimes.get(filepath) != current_mtime:
            return False

    return True


TOOLS = [
    {
        "name": "search_content",
        "description": "Search the Claude Code documentation for specific information. Use this when users ask 'how to', need details about features, or want examples.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to find relevant documentation content"
                },
                "top_k": {
                    "type": "integer",
                    "description": "Number of results to return (1-5, default 3)",
                    "default": 3
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_course_outline",
        "description": "Get the structure and lesson list for a course. Use this when users ask 'what's in chapter X', 'show me topics', or want navigation information.",
        "input_schema": {
            "type": "object",
            "properties": {
                "course_identifier": {
                    "type": "string",
                    "description": "Chapter identifier: number (1-5), chapter name (e.g., 'getting started', 'tools', 'file operations'), or 'all' for complete list"
                }
            },
            "required": ["course_identifier"]
        }
    }
]


def _load_course_metadata(chapters_dir: str = "data/chapters") -> dict:
    """Load and cache course metadata from markdown files.

    Cache is automatically invalidated when files are modified.

    Args:
        chapters_dir: Directory containing markdown chapter files

    Returns:
        Dictionary mapping chapter names to course information
    """
    global _course_metadata_cache, _cache_file_mtimes

    # Check if cached data is still valid
    if _cache_is_valid(chapters_dir):
        return _course_metadata_cache

    metadata = {}
    chapter_files = sorted(glob.glob(os.path.join(chapters_dir, "*.md")))

    for chapter_path in chapter_files:
        chapter_name = Path(chapter_path).stem

        with open(chapter_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract YAML frontmatter
        frontmatter = _extract_frontmatter(content)

        # Extract lessons from ## headers
        lessons = _extract_lessons(content)

        # Parse chapter number from filename (chapter1_... -> 1)
        chapter_num_match = re.search(r'chapter(\d+)', chapter_name)
        chapter_num = int(chapter_num_match.group(1)) if chapter_num_match else 0

        metadata[chapter_name] = {
            "id": chapter_name,
            "number": chapter_num,
            "title": frontmatter.get('title', chapter_name),
            "url": frontmatter.get('url', ''),
            "lesson_count": len(lessons),
            "lessons": lessons
        }

    _course_metadata_cache = metadata
    _cache_file_mtimes = _get_chapter_file_mtimes(chapters_dir)
    return metadata


def _extract_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown.

    Args:
        content: Full document content

    Returns:
        Dictionary with frontmatter fields
    """
    if not content.startswith('---'):
        return {}

    try:
        lines = content.split('\n')
        end_idx = -1
        for i in range(1, len(lines)):
            if lines[i].startswith('---'):
                end_idx = i
                break

        if end_idx == -1:
            return {}

        yaml_content = '\n'.join(lines[1:end_idx])
        frontmatter = yaml.safe_load(yaml_content)

        if frontmatter and isinstance(frontmatter, dict):
            return frontmatter
        return {}
    except Exception:
        return {}


def _extract_lessons(content: str) -> list:
    """Extract lessons from ## headers in markdown.

    Args:
        content: Document content (frontmatter already removed or not)

    Returns:
        List of lesson dictionaries with number and title
    """
    # Remove frontmatter first
    if content.startswith('---'):
        lines = content.split('\n')
        for i in range(1, len(lines)):
            if lines[i].startswith('---'):
                content = '\n'.join(lines[i+1:])
                break

    lessons = []
    lesson_num = 1

    for line in content.split('\n'):
        if line.startswith('## '):
            title = line.replace('## ', '').strip()
            lessons.append({
                "number": lesson_num,
                "title": title
            })
            lesson_num += 1

    return lessons


def _normalize_course_identifier(course_identifier: str) -> Optional[str]:
    """Normalize course identifier to chapter name.

    Args:
        course_identifier: Chapter number, name, or 'all'

    Returns:
        Chapter name or None if not found
    """
    metadata = _load_course_metadata()
    identifier_lower = course_identifier.lower().strip()

    # Special case: 'all'
    if identifier_lower == 'all':
        return 'all'

    # Try matching by chapter number
    try:
        chapter_num = int(identifier_lower)
        for chapter_name, info in metadata.items():
            if info['number'] == chapter_num:
                return chapter_name
    except ValueError:
        pass

    # Try fuzzy matching by name
    for chapter_name, info in metadata.items():
        title_lower = info['title'].lower()
        # Check if identifier is in title or title is in identifier
        if (identifier_lower in title_lower or
            title_lower.find(identifier_lower) != -1 or
            chapter_name.lower().find(identifier_lower) != -1):
            return chapter_name

    return None


def search_content(query: str, top_k: int = 3, rag_system=None) -> dict:
    """Search content using RAG system.

    Args:
        query: Search query
        top_k: Number of results to return
        rag_system: RAGSystem instance

    Returns:
        Dictionary with search results
    """
    if rag_system is None:
        return {
            "error": "RAG system not available",
            "results": [],
            "results_count": 0
        }

    # Validate top_k
    top_k = max(1, min(5, top_k))

    # Retrieve context
    context = rag_system.retrieve_context(query, top_k=top_k)

    # Format results
    results = []
    seen_chapters = set()

    for item in context:
        result = {
            "chapter": item['chapter'],
            "title": item['title'],
            "content": item['content'],
            "url": item.get('url', ''),
            "relevance": item.get('relevance', 0.5)
        }
        results.append(result)
        seen_chapters.add(item['chapter'])

    return {
        "results_count": len(results),
        "results": results,
        "query": query
    }


def get_course_outline(course_identifier: str) -> dict:
    """Get course outline with lessons.

    Args:
        course_identifier: Chapter number, name, or 'all'

    Returns:
        Dictionary with course information
    """
    metadata = _load_course_metadata()

    # Handle 'all' case
    if course_identifier.lower() == 'all':
        courses = []
        for chapter_name in sorted(metadata.keys(), key=lambda x: metadata[x]['number']):
            info = metadata[chapter_name]
            courses.append({
                "id": info['id'],
                "number": info['number'],
                "title": info['title'],
                "url": info['url'],
                "lesson_count": info['lesson_count']
            })

        return {
            "courses_count": len(courses),
            "courses": courses
        }

    # Find matching chapter
    matched_chapter = _normalize_course_identifier(course_identifier)

    if matched_chapter is None:
        # Return error with available courses
        available = sorted(
            [(info['number'], info['title'], name) for name, info in metadata.items()],
            key=lambda x: x[0]
        )
        return {
            "error": f"No course found matching '{course_identifier}'",
            "available_courses": [
                {
                    "number": num,
                    "title": title,
                    "identifier": name
                }
                for num, title, name in available
            ]
        }

    # Return matched course
    info = metadata[matched_chapter]
    return {
        "course": {
            "id": info['id'],
            "number": info['number'],
            "title": info['title'],
            "url": info['url'],
            "lesson_count": info['lesson_count'],
            "lessons": info['lessons']
        }
    }


def execute_tool(tool_name: str, tool_input: dict, rag_system=None) -> dict:
    """Execute a tool by name.

    Args:
        tool_name: Name of the tool to execute
        tool_input: Input parameters for the tool
        rag_system: RAGSystem instance (optional, needed for search_content)

    Returns:
        Tool execution result
    """
    try:
        if tool_name == "search_content":
            query = tool_input.get('query', '')
            top_k = tool_input.get('top_k', 3)
            if not query:
                return {"error": "query parameter is required"}
            return search_content(query, top_k, rag_system)

        elif tool_name == "get_course_outline":
            course_id = tool_input.get('course_identifier', 'all')
            if not course_id:
                return {"error": "course_identifier parameter is required"}
            return get_course_outline(course_id)

        else:
            return {"error": f"Unknown tool: {tool_name}"}

    except Exception as e:
        return {
            "error": f"Tool execution failed: {str(e)}"
        }


def clear_course_cache():
    """Clear the course metadata cache and file modification times."""
    global _course_metadata_cache, _cache_file_mtimes
    _course_metadata_cache = None
    _cache_file_mtimes = None
