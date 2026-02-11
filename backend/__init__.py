"""Backend package for search tools and tool calling support."""

from .search_tools import (
    TOOLS,
    execute_tool,
    search_content,
    get_course_outline,
    clear_course_cache,
)

__all__ = [
    'TOOLS',
    'execute_tool',
    'search_content',
    'get_course_outline',
    'clear_course_cache',
]
