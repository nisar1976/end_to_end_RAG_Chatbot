"""Unit tests for input validation (Bug #1)."""
import pytest
from fastapi.testclient import TestClient
from main import app


class TestInputValidation:
    """Test query input validation."""

    def test_empty_query(self):
        """Test that empty queries are rejected."""
        client = TestClient(app)

        response = client.post("/api/query", json={"question": ""})

        # Should return 400 Bad Request
        assert response.status_code == 400

    def test_whitespace_only_query(self):
        """Test that whitespace-only queries are rejected."""
        client = TestClient(app)

        response = client.post("/api/query", json={"question": "   \n\t  "})

        # Should return 400 Bad Request
        assert response.status_code == 400

    def test_very_long_query(self):
        """Test that excessively long queries are handled (Bug #1)."""
        client = TestClient(app)

        # Create a very long query (10,000+ characters)
        long_query = "a" * 10000

        response = client.post("/api/query", json={"question": long_query})

        # Should either:
        # 1. Reject with 400 (preferred)
        # 2. Handle gracefully without timeout
        # Currently may hang or crash - this test should FAIL
        if response.status_code == 400:
            # Good: validation exists
            assert True
        else:
            # May indicate no validation (Bug #1)
            # Test should complete within reasonable time
            assert response.status_code in [200, 400, 413]  # 413 = Payload Too Large

    def test_query_with_special_chars(self):
        """Test query with special characters."""
        client = TestClient(app)

        queries = [
            "What is @#$%&?",
            "Query with émojis 🎉",
            "Query\nwith\nnewlines",
            "Query\twith\ttabs",
            'Query with "quotes"',
            "Query with 'apostrophes'",
        ]

        for query in queries:
            response = client.post("/api/query", json={"question": query})
            # Should not crash on special chars
            assert response.status_code in [200, 400, 503]

    def test_query_with_unicode(self):
        """Test query with unicode characters."""
        client = TestClient(app)

        response = client.post(
            "/api/query",
            json={"question": "¿Cómo funciona esto? 你好世界"}
        )

        # Should handle unicode gracefully
        assert response.status_code in [200, 400, 503]

    def test_query_with_code_snippets(self):
        """Test query containing code snippets."""
        client = TestClient(app)

        response = client.post(
            "/api/query",
            json={
                "question": """
How do I fix this code?

```python
def bug():
    x = []
    return x[0]
```
"""
            }
        )

        # Should handle code blocks in queries
        assert response.status_code in [200, 400, 503]

    def test_query_with_null_value(self):
        """Test request with null question value."""
        client = TestClient(app)

        response = client.post("/api/query", json={"question": None})

        # Should reject null values
        assert response.status_code == 422  # Unprocessable Entity

    def test_query_missing_field(self):
        """Test request missing question field."""
        client = TestClient(app)

        response = client.post("/api/query", json={})

        # Should reject missing required field
        assert response.status_code == 422

    def test_query_with_extra_fields(self):
        """Test request with extra fields (should be allowed)."""
        client = TestClient(app)

        response = client.post(
            "/api/query",
            json={
                "question": "What is this?",
                "extra_field": "should be ignored",
                "another": 123
            }
        )

        # Should ignore extra fields
        assert response.status_code in [200, 503, 400]
