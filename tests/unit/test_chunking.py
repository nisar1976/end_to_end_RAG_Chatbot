"""Unit tests for markdown chunking logic (Bug #6)."""
import pytest
from rag_system import RAGSystem


class TestChunkingLogic:
    """Test the _split_into_chunks method."""

    def test_chunking_with_valid_headers(self, temp_chapters_dir, sample_valid_chapter):
        """Test that standard markdown with ## headers chunks correctly."""
        rag = RAGSystem()

        content = """## Section 1
Content for section 1

## Section 2
Content for section 2

## Section 3
Content for section 3"""

        chunks = rag._split_into_chunks(content, "test_chapter")

        # Should have 3 chunks
        assert len(chunks) == 3
        assert chunks[0][0] == "Section 1"
        assert chunks[1][0] == "Section 2"
        assert chunks[2][0] == "Section 3"

    def test_chunking_without_space(self):
        """Test chunking fails with ## but no space (Bug #6 - expects FAIL)."""
        rag = RAGSystem()

        content = """##Section1NoSpace
Content for section 1

##Section2NoSpace
Content for section 2"""

        chunks = rag._split_into_chunks(content, "test_chapter")

        # BUG: Currently expects 1 chunk, but should be 2
        # This test should FAIL - proving the bug exists
        assert len(chunks) == 2, "Bug #6: ##NoSpace should be recognized as headers"

    def test_chunking_in_code_blocks(self):
        """Test that ## inside code blocks are not treated as headers (Bug #6)."""
        rag = RAGSystem()

        content = """## Real Section

Here's a code block:

```python
## This looks like a header but it's code
x = 1
```

More content for this section."""

        chunks = rag._split_into_chunks(content, "test_chapter")

        # Should have 1 chunk, not 2 (code block should not split)
        # This test should FAIL - proving the bug exists
        assert len(chunks) == 1, "Bug #6: ## in code blocks should not split chunks"

    def test_chunking_no_headers(self):
        """Test that content without ## headers creates single chunk."""
        rag = RAGSystem()

        content = """# Just a Title

Paragraph 1

Paragraph 2

Paragraph 3"""

        chunks = rag._split_into_chunks(content, "test_chapter")

        # Should have 1 chunk since no ## headers
        assert len(chunks) == 1
        assert len(chunks[0][1]) > 0

    def test_chunking_mixed_header_levels(self):
        """Test that only ## is recognized, not ### or ####."""
        rag = RAGSystem()

        content = """## Section 1

### Subsection (should not split)

Content here

#### Deep subsection (should not split)

More content

## Section 2

Final section"""

        chunks = rag._split_into_chunks(content, "test_chapter")

        # Should have only 2 chunks (## headers only)
        # ### and #### should NOT cause splits
        assert len(chunks) == 2
        assert chunks[0][0] == "Section 1"
        assert chunks[1][0] == "Section 2"

    def test_chunking_empty_sections(self):
        """Test handling of empty sections between headers."""
        rag = RAGSystem()

        content = """## Section 1

## Section 2

## Section 3
Content here"""

        chunks = rag._split_into_chunks(content, "test_chapter")

        # Empty sections should be skipped or handled gracefully
        # At minimum, should not crash
        assert isinstance(chunks, list)
        assert len(chunks) > 0

    def test_chunking_preserves_content(self):
        """Test that chunking doesn't lose or corrupt content."""
        rag = RAGSystem()

        original_content = """## Intro
Introduction text with special chars: café, naïve, Ñ

## Body
Body content with code: `print("hello")`

## Conclusion
Final thoughts."""

        chunks = rag._split_into_chunks(original_content, "test_chapter")

        # Reconstruct content and verify nothing is lost
        reconstructed = "\n".join([chunk[1] for chunk in chunks])
        # Content should be preserved (allowing for whitespace differences)
        assert "café" in reconstructed
        assert 'print("hello")' in reconstructed
        assert "Final thoughts" in reconstructed

    def test_chunking_with_leading_content(self):
        """Test chunking with content before first header."""
        rag = RAGSystem()

        content = """Introduction before any headers

This is preamble content that comes before sections.

## Section 1
Actual section content

## Section 2
More content"""

        chunks = rag._split_into_chunks(content, "test_chapter")

        # Should handle preamble content
        assert len(chunks) >= 2
