"""Shared test fixtures and mocks for RAG chatbot tests."""
import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, MagicMock

import pytest
import chromadb
from sentence_transformers import SentenceTransformer


@pytest.fixture
def temp_chapters_dir():
    """Create a temporary directory for test markdown files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def ephemeral_chromadb():
    """Create an ephemeral (in-memory) ChromaDB instance for fast tests."""
    client = chromadb.EphemeralClient()
    yield client


@pytest.fixture
def mock_anthropic_client(mocker):
    """Mock Anthropic client to avoid real API calls."""
    mock = MagicMock()

    # Setup default response
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="Test response from Claude")]
    mock_response.stop_reason = "end_turn"
    mock_response.usage = MagicMock(input_tokens=10, output_tokens=20)

    mock.messages.create.return_value = mock_response

    return mock


@pytest.fixture
def mock_embedding_model(mocker):
    """Mock SentenceTransformer to avoid model download."""
    mock = MagicMock(spec=SentenceTransformer)

    # Return consistent embeddings for testing
    mock.encode.return_value = [[0.1] * 384 for _ in range(10)]

    mocker.patch('sentence_transformers.SentenceTransformer', return_value=mock)

    return mock


@pytest.fixture
def sample_valid_chapter(temp_chapters_dir):
    """Create a valid chapter with YAML frontmatter and ## headers."""
    chapter_path = Path(temp_chapters_dir) / "chapter1.md"
    content = """---
url: "https://example.com/chapter1"
---

# Chapter 1: Getting Started

## Section 1: Introduction

This is the introduction section with some content.

## Section 2: Setup

Here we discuss setup procedures.

## Section 3: First Steps

Getting started with the project.
"""
    chapter_path.write_text(content)
    return chapter_path


@pytest.fixture
def sample_no_headers_chapter(temp_chapters_dir):
    """Create a chapter with no ## headers (edge case)."""
    chapter_path = Path(temp_chapters_dir) / "chapter_no_headers.md"
    content = """---
url: "https://example.com/chapter"
---

# Chapter Without Headers

This entire chapter has no ## section headers,
so it should be treated as a single chunk.

Multiple paragraphs here, but still one logical section.
"""
    chapter_path.write_text(content)
    return chapter_path


@pytest.fixture
def sample_malformed_yaml_chapter(temp_chapters_dir):
    """Create a chapter with malformed YAML frontmatter."""
    chapter_path = Path(temp_chapters_dir) / "chapter_bad_yaml.md"
    content = """---
url: "https://example.com"
invalid_yaml: this is bad: yaml: content: [
---

## Section 1

Some content here.
"""
    chapter_path.write_text(content)
    return chapter_path


@pytest.fixture
def sample_yaml_in_code_block(temp_chapters_dir):
    """Create a chapter with code blocks containing --- and ## markers."""
    chapter_path = Path(temp_chapters_dir) / "chapter_code_yaml.md"
    content = """---
url: "https://example.com"
---

## Real Section 1

This section discusses YAML.

Here's a code block with YAML-like syntax:

```yaml
---
key: value
---
another: entry
```

## Real Section 2

More content after code block.
"""
    chapter_path.write_text(content)
    return chapter_path


@pytest.fixture
def sample_empty_chapter(temp_chapters_dir):
    """Create an empty markdown file."""
    chapter_path = Path(temp_chapters_dir) / "empty.md"
    chapter_path.write_text("")
    return chapter_path


@pytest.fixture
def sample_headers_no_space(temp_chapters_dir):
    """Create a chapter with ## but no space after (edge case)."""
    chapter_path = Path(temp_chapters_dir) / "chapter_no_space.md"
    content = """---
url: "https://example.com"
---

##Section1NoSpace
Content for section 1

##Section2NoSpace
Content for section 2
"""
    chapter_path.write_text(content)
    return chapter_path


@pytest.fixture
def sample_mixed_header_levels(temp_chapters_dir):
    """Create a chapter with ### and #### headers (not just ##)."""
    chapter_path = Path(temp_chapters_dir) / "chapter_mixed_headers.md"
    content = """---
url: "https://example.com"
---

## Main Section 1

### Subsection 1.1

Content for subsection.

#### Deep subsection

More content.

## Main Section 2

Only ## headers should split chunks.
"""
    chapter_path.write_text(content)
    return chapter_path


@pytest.fixture
def mock_rag_system(mock_anthropic_client, ephemeral_chromadb, mocker):
    """Create a mock RAG system for testing."""
    from rag_system import RAGSystem

    # Patch the Anthropic client
    mocker.patch('rag_system.Anthropic', return_value=mock_anthropic_client)

    # Patch ChromaDB to use ephemeral
    mocker.patch('rag_system.chromadb.PersistentClient', return_value=ephemeral_chromadb)

    # Create RAG system instance
    rag = RAGSystem(db_path=":memory:")
    rag.anthropic_client = mock_anthropic_client

    return rag


@pytest.fixture
def mock_fastapi_app(mock_rag_system, mocker):
    """Create a FastAPI test app with mocked RAG system."""
    from main import app
    from fastapi.testclient import TestClient

    # Patch global rag_system variable
    mocker.patch('main.rag_system', mock_rag_system)

    return TestClient(app)
