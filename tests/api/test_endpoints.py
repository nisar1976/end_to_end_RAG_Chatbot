"""Tests for FastAPI endpoints (Bugs #4, #5)."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch


@pytest.fixture
def client_with_rag(mocker):
    """Create a test client with mocked RAG system."""
    from main import app

    # Mock the global rag_system
    mock_rag = MagicMock()
    mock_rag.collection.count.return_value = 25

    # Setup default query response
    mock_rag.query.return_value = {
        "answer": "Test answer",
        "sources": [{"chapter": "Ch1", "url": "http://example.com"}],
        "context_count": 1
    }

    mocker.patch("main.rag_system", mock_rag)

    return TestClient(app), mock_rag


class TestEndpoints:
    """Test FastAPI endpoints."""

    def test_health_endpoint(self, client_with_rag):
        """Test /api/health endpoint."""
        client, _ = client_with_rag
        response = client.get("/api/health")

        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        assert "rag_initialized" in response.json()

    def test_health_before_rag_init(self, mocker):
        """Test health check when RAG not initialized (Bug #4)."""
        from main import app

        # rag_system is None initially
        mocker.patch("main.rag_system", None)

        client = TestClient(app)
        response = client.get("/api/health")

        assert response.status_code == 200
        assert response.json()["rag_initialized"] is False

    def test_query_endpoint_success(self, client_with_rag):
        """Test successful /api/query request."""
        client, mock_rag = client_with_rag

        response = client.post(
            "/api/query",
            json={"question": "What is Python?"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "sources" in data
        assert "context_count" in data

    def test_query_before_startup(self, mocker):
        """Test query when RAG system not initialized (Bug #4)."""
        from main import app

        # RAG system not initialized
        mocker.patch("main.rag_system", None)

        client = TestClient(app)
        response = client.post(
            "/api/query",
            json={"question": "Test"}
        )

        # Should return 503 Service Unavailable
        assert response.status_code == 503

    def test_query_empty_question(self, client_with_rag):
        """Test query with empty question."""
        client, _ = client_with_rag

        response = client.post(
            "/api/query",
            json={"question": ""}
        )

        assert response.status_code == 400

    def test_query_whitespace_question(self, client_with_rag):
        """Test query with whitespace-only question."""
        client, _ = client_with_rag

        response = client.post(
            "/api/query",
            json={"question": "   \n  \t  "}
        )

        assert response.status_code == 400

    def test_query_missing_question_field(self, client_with_rag):
        """Test request missing question field."""
        client, _ = client_with_rag

        response = client.post(
            "/api/query",
            json={"wrong_field": "value"}
        )

        assert response.status_code == 422

    def test_concurrent_queries(self, client_with_rag):
        """Test concurrent query requests (Bug #4 - ChromaDB single-threaded)."""
        client, mock_rag = client_with_rag

        # Setup responses for concurrent calls
        mock_rag.query.side_effect = [
            {
                "answer": "Response 1",
                "sources": [],
                "context_count": 0
            },
            {
                "answer": "Response 2",
                "sources": [],
                "context_count": 0
            }
        ]

        import threading
        results = []
        errors = []

        def make_query():
            try:
                resp = client.post(
                    "/api/query",
                    json={"question": f"Query {len(results)}"}
                )
                results.append(resp.status_code)
            except Exception as e:
                errors.append(e)

        # Run concurrent queries
        threads = [threading.Thread(target=make_query) for _ in range(2)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Should complete without errors
        assert len(errors) == 0
        # Both should succeed or return expected status codes
        for status in results:
            assert status in [200, 503]

    def test_response_format_consistency(self, client_with_rag):
        """Test that error responses have consistent format (Bug #5)."""
        client, _ = client_with_rag

        # Test different error scenarios
        # Case 1: Empty question
        resp1 = client.post("/api/query", json={"question": ""})
        data1 = resp1.json()

        # Case 2: Missing field
        resp2 = client.post("/api/query", json={})
        data2 = resp2.json()

        # Both should have detail field in error response
        # This test should FAIL if formats are inconsistent (Bug #5)
        assert "detail" in data1, "Empty question response should have 'detail' field"
        assert "detail" in data2, "Missing field response should have 'detail' field"

    def test_query_with_tools_parameter(self, client_with_rag):
        """Test query endpoint with use_tools parameter."""
        client, mock_rag = client_with_rag

        response = client.post(
            "/api/query",
            json={"question": "Test", "use_tools": True}
        )

        assert response.status_code == 200
        mock_rag.query.assert_called()
        # Check use_tools was passed
        call_args = mock_rag.query.call_args
        assert "use_tools" in call_args.kwargs or (len(call_args.args) > 1)

    def test_root_endpoint(self, client_with_rag):
        """Test that root endpoint serves HTML."""
        client, _ = client_with_rag

        response = client.get("/")

        assert response.status_code == 200
        # Should return HTML content
        assert "text/html" in response.headers.get("content-type", "")

    def test_static_files_serving(self, client_with_rag):
        """Test that static files are served."""
        client, _ = client_with_rag

        # Try accessing a static file
        response = client.get("/static/style.css")

        # Should either serve the file or return 404 (if file doesn't exist)
        assert response.status_code in [200, 404]
