"""Unit tests for YAML frontmatter parsing (Bug #10)."""
import pytest
from rag_system import RAGSystem


class TestYAMLParsing:
    """Test YAML frontmatter extraction logic."""

    def test_valid_yaml_extraction(self):
        """Test that valid YAML frontmatter is extracted correctly."""
        rag = RAGSystem()

        content = """---
url: "https://example.com/chapter1"
title: "Chapter 1"
---

## Content Section

Actual content here."""

        url = rag._extract_frontmatter_url(content)

        assert url == "https://example.com/chapter1"

    def test_yaml_in_code_block(self):
        """Test that --- inside code blocks don't break parsing (Bug #10)."""
        rag = RAGSystem()

        content = """---
url: "https://example.com"
---

## Code Example

Here's a code block:

```yaml
---
config: value
---
```

More content."""

        url = rag._extract_frontmatter_url(content)

        # Should extract the real URL, not get confused by code block
        # This test should FAIL - proving the bug exists
        assert url == "https://example.com", "Bug #10: Code block --- should not interfere with YAML parsing"

    def test_missing_closing_yaml(self):
        """Test handling of missing closing --- delimiter."""
        rag = RAGSystem()

        content = """---
url: "https://example.com"
title: "Missing Close"

## Content

Body without closing ---"""

        # Should not crash, even if malformed
        try:
            url = rag._extract_frontmatter_url(content)
            # Either extracts correctly or returns empty string gracefully
            assert isinstance(url, str)
        except Exception as e:
            # This test should FAIL if exception is raised
            pytest.fail(f"Bug #10: Malformed YAML should be handled gracefully, got: {e}")

    def test_malformed_yaml(self):
        """Test that malformed YAML doesn't crash the system."""
        rag = RAGSystem()

        content = """---
url: "https://example.com"
bad_yaml: this is bad: [yaml: syntax: {
---

## Content

Some content."""

        # Should not crash even with invalid YAML
        try:
            url = rag._extract_frontmatter_url(content)
            # Should return something (empty string or partial extract)
            assert isinstance(url, str)
        except Exception as e:
            pytest.fail(f"Bug #10: Should handle malformed YAML gracefully, got: {e}")

    def test_multiple_yaml_separators(self):
        """Test ambiguous YAML with multiple --- separators."""
        rag = RAGSystem()

        content = """---
url: "https://example.com"
---

---
another_yaml: "value"
---

## Content

Body"""

        # Should use first --- pair, not get confused
        url = rag._extract_frontmatter_url(content)
        assert url == "https://example.com"

    def test_empty_frontmatter(self):
        """Test handling of empty YAML frontmatter."""
        rag = RAGSystem()

        content = """---
---

## Content

Body without URL"""

        url = rag._extract_frontmatter_url(content)

        # Should return empty string, not crash
        assert url == ""

    def test_no_frontmatter(self):
        """Test content with no YAML frontmatter."""
        rag = RAGSystem()

        content = """## Content

Just markdown, no YAML."""

        url = rag._extract_frontmatter_url(content)

        # Should return empty string
        assert url == ""

    def test_yaml_with_special_chars(self):
        """Test YAML with special characters in URL."""
        rag = RAGSystem()

        content = """---
url: "https://example.com/path?query=value&other=123#anchor"
---

## Content"""

        url = rag._extract_frontmatter_url(content)

        assert url == "https://example.com/path?query=value&other=123#anchor"

    def test_yaml_with_unicode(self):
        """Test YAML with unicode characters."""
        rag = RAGSystem()

        content = """---
title: "Chapitre 1: Introduction"
url: "https://example.com/章节1"
---

## Contenu

Contenu en français et 中文"""

        url = rag._extract_frontmatter_url(content)

        assert url == "https://example.com/章节1"

    def test_remove_frontmatter(self):
        """Test that _remove_frontmatter correctly strips YAML."""
        rag = RAGSystem()

        content = """---
url: "https://example.com"
---

## Real Content

This should remain."""

        cleaned = rag._remove_frontmatter(content)

        # URL should not be in output
        assert "https://example.com" not in cleaned
        # Content should remain
        assert "Real Content" in cleaned
        assert "This should remain" in cleaned
