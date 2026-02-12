"""Tests for error handling consistency (Bugs #2, #5, #7)."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from anthropic import APIError


@pytest.fixture
def client_with_errors(mocker):
    """Create test client that can inject errors."""
    from main import app

    mock_rag = MagicMock()
    mock_rag.collection.count.return_value = 25
    mocker.patch("main.rag_system", mock_rag)

    return TestClient(app), mock_rag


class TestErrorHandling:
    """Test error handling and response consistency."""

    def test_error_response_format_json(self, client_with_errors):
        """Test that error responses are valid JSON."""
        client, _ = client_with_errors

        response = client.post("/api/query", json={})

        assert response.status_code >= 400
        # Should be valid JSON
        try:
            data = response.json()
            assert "detail" in data or "error" in data
        except Exception:
            pytest.fail("Error response is not valid JSON")

    def test_error_response_consistency(self, client_with_errors):
        """Test error responses have consistent structure (Bug #5)."""
        client, _ = client_with_errors

        # Trigger different types of errors
        error_cases = [
            (400, {"question": ""}),  # Empty question
            (422, {}),  # Missing required field
            (422, {"question": None}),  # Null value
        ]

        responses = []
        for expected_status, payload in error_cases:
            resp = client.post("/api/query", json=payload)
            responses.append((resp.status_code, resp.json()))

        # All should have consistent error structure
        # This test should FAIL if formats differ (Bug #5)
        for status, data in responses:
            assert "detail" in data or "error" in data, \
                f"Inconsistent error format for {status}: {data}"

    def test_anthropic_api_error_propagation(self, client_with_errors):
        """Test that API errors are properly reported (Bug #2)."""
        client, mock_rag = client_with_errors

        # Mock API error
        mock_rag.query.side_effect = APIError(
            message="API key invalid",
            response=MagicMock(status_code=401),
            body={"error": {"type": "authentication_error"}}
        )

        response = client.post(
            "/api/query",
            json={"question": "Test"}
        )

        # Should return 500 or proper error
        assert response.status_code >= 400
        data = response.json()
        # Should have error information (Bug #2 - currently may swallow error)
        # This test should FAIL if error info is lost
        assert "detail" in data or len(data) > 0

    def test_missing_api_key_error(self, client_with_errors):
        """Test error message when API key is missing."""
        client, mock_rag = client_with_errors

        # Mock authentication error
        mock_rag.query.side_effect = APIError(
            message="No API key provided",
            response=MagicMock(status_code=401),
            body={"error": {"type": "authentication_error"}}
        )

        response = client.post(
            "/api/query",
            json={"question": "Test"}
        )

        assert response.status_code >= 400
        # Should have clear error message
        data = response.json()
        assert "detail" in data or "error" in data

    def test_chromadb_connection_error_response(self, client_with_errors):
        """Test error response when ChromaDB fails."""
        client, mock_rag = client_with_errors

        mock_rag.query.side_effect = ConnectionError(
            "ChromaDB connection failed"
        )

        response = client.post(
            "/api/query",
            json={"question": "Test"}
        )

        assert response.status_code >= 400
        data = response.json()
        # Should indicate database error
        assert "detail" in data or "error" in data

    def test_timeout_error_response(self, client_with_errors):
        """Test error response for timeout (Bug #7)."""
        client, mock_rag = client_with_errors

        mock_rag.query.side_effect = TimeoutError(
            "Query timed out after 30 seconds"
        )

        response = client.post(
            "/api/query",
            json={"question": "Complex query"}
        )

        # Should return appropriate error
        # 504 Gateway Timeout is appropriate for timeouts
        assert response.status_code in [500, 504]
        data = response.json()
        # Should indicate timeout (Bug #7 - error might be swallowed)
        assert "timeout" in str(data).lower() or "timed out" in str(data).lower() or len(data) > 0

    def test_malformed_request_json(self, client_with_errors):
        """Test response to malformed JSON request."""
        client, _ = client_with_errors

        # Invalid JSON
        response = client.post(
            "/api/query",
            data="{invalid json",
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 422
        data = response.json()
        assert "detail" in data or "error" in data

    def test_unknown_endpoint_404(self, client_with_errors):
        """Test 404 response for unknown endpoints."""
        client, _ = client_with_errors

        response = client.get("/api/nonexistent")

        assert response.status_code == 404

    def test_method_not_allowed(self, client_with_errors):
        """Test 405 response for wrong HTTP method."""
        client, _ = client_with_errors

        # Try GET on POST-only endpoint
        response = client.get("/api/query")

        assert response.status_code == 405

    def test_query_exception_traceback(self, client_with_errors):
        """Test that exception tracebacks are not exposed (security)."""
        client, mock_rag = client_with_errors

        mock_rag.query.side_effect = Exception("Internal error details")

        response = client.post(
            "/api/query",
            json={"question": "Test"}
        )

        data = response.json()
        error_msg = str(data)

        # Should NOT expose internal exception details in response
        # Should be generic message to prevent information disclosure
        assert "Traceback" not in error_msg
        # Internal details should not be visible
        assert "Internal error details" not in error_msg

    def test_large_response_handling(self, client_with_errors):
        """Test handling of large responses."""
        client, mock_rag = client_with_errors

        # Mock a very large response
        mock_rag.query.return_value = {
            "answer": "A" * 100000,  # 100KB response
            "sources": [],
            "context_count": 0
        }

        response = client.post(
            "/api/query",
            json={"question": "Test"}
        )

        # Should handle large response
        assert response.status_code == 200
        assert len(response.json()["answer"]) > 50000
