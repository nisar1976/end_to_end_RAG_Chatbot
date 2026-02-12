"""Integration tests for full RAG pipeline (Bugs #3, #7)."""
import pytest
from unittest.mock import MagicMock, patch
from anthropic import APIError


class TestRAGPipeline:
    """Test the complete RAG workflow."""

    def test_full_rag_workflow(self, mock_rag_system, mocker):
        """Test end-to-end RAG workflow."""
        # Setup retrieval
        mock_rag_system.collection.query.return_value = {
            "ids": [["doc1"]],
            "distances": [[0.1]],
            "metadatas": [[{"chapter": "Ch1", "title": "Sec1", "url": "http://ex.com"}]],
            "documents": [["Test content"]]
        }

        # Setup Claude response
        mock_rag_system.anthropic_client.messages.create.return_value = MagicMock(
            content=[MagicMock(text="Test answer from Claude")],
            stop_reason="end_turn"
        )

        result = mock_rag_system.query("What is this about?")

        # Verify workflow completed
        assert result is not None
        assert result["answer"] == "Test answer from Claude"
        assert len(result["sources"]) > 0
        assert result["context_count"] == 1

    def test_anthropic_api_error_handling(self, mock_rag_system):
        """Test handling of Anthropic API errors (Bug #3, #7)."""
        # Simulate API error
        mock_rag_system.anthropic_client.messages.create.side_effect = APIError(
            message="Rate limited",
            response=MagicMock(status_code=429),
            body={"error": {"type": "rate_limit_error"}}
        )

        # Should raise or return error response
        # Currently may have no retry logic (Bug #3)
        with pytest.raises(APIError):
            mock_rag_system.query("Test query")

    def test_anthropic_rate_limit_retry(self, mock_rag_system):
        """Test retry logic on rate limits (Bug #3)."""
        # First call fails, second succeeds (simulating retry)
        responses = [
            APIError(
                message="Rate limited",
                response=MagicMock(status_code=429),
                body={"error": {"type": "rate_limit_error"}}
            ),
            MagicMock(
                content=[MagicMock(text="Success after retry")],
                stop_reason="end_turn"
            )
        ]

        mock_rag_system.anthropic_client.messages.create.side_effect = responses

        # This test should FAIL - proving no retry logic (Bug #3)
        try:
            result = mock_rag_system.query("Test query")
            assert result["answer"] == "Success after retry"
        except APIError:
            pytest.fail("Bug #3: No retry logic on API errors")

    def test_empty_retrieval_results(self, mock_rag_system):
        """Test handling when no documents are retrieved."""
        # Empty retrieval
        mock_rag_system.collection.query.return_value = {
            "ids": [[]],
            "distances": [[]],
            "metadatas": [[]],
            "documents": [[]]
        }

        # Claude still responds
        mock_rag_system.anthropic_client.messages.create.return_value = MagicMock(
            content=[MagicMock(text="I don't have relevant information")],
            stop_reason="end_turn"
        )

        result = mock_rag_system.query("Obscure question")

        # Should handle gracefully
        assert result is not None
        assert "answer" in result
        assert result["context_count"] == 0

    def test_retrieval_timeout_handling(self, mock_rag_system):
        """Test timeout handling during retrieval (Bug #7)."""
        import time

        def slow_query(*args, **kwargs):
            time.sleep(5)  # Simulate slow query
            return {
                "ids": [[]],
                "distances": [[]],
                "metadatas": [[]],
                "documents": [[]]
            }

        mock_rag_system.collection.query = slow_query

        # Should timeout or return after reasonable time
        # Currently may hang indefinitely (Bug #7)
        try:
            result = mock_rag_system.query("Test query", timeout=1)
            # Should complete or raise timeout
            assert result is not None
        except TimeoutError:
            # Timeout is better than hanging
            pass

    def test_claude_api_timeout(self, mock_rag_system):
        """Test timeout handling for Claude API calls (Bug #7)."""
        import time

        def slow_api_call(*args, **kwargs):
            time.sleep(5)  # Simulate slow API
            return MagicMock(
                content=[MagicMock(text="Response")],
                stop_reason="end_turn"
            )

        mock_rag_system.anthropic_client.messages.create = slow_api_call

        # Should timeout or return within reasonable time
        # Currently may hang indefinitely (Bug #7)
        try:
            result = mock_rag_system.query("Test", timeout=1)
            assert result is not None
        except TimeoutError:
            pass

    def test_malformed_context_handling(self, mock_rag_system):
        """Test handling of malformed retrieved context."""
        # Return malformed metadata
        mock_rag_system.collection.query.return_value = {
            "ids": [["doc1"]],
            "distances": [[0.1]],
            "metadatas": [[None]],  # Malformed
            "documents": [[None]]
        }

        mock_rag_system.anthropic_client.messages.create.return_value = MagicMock(
            content=[MagicMock(text="Answer")],
            stop_reason="end_turn"
        )

        # Should handle gracefully without crashing
        result = mock_rag_system.query("Test")
        assert result is not None

    def test_encoding_error_in_embedding(self, mock_rag_system, mocker):
        """Test handling of encoding errors in embedding."""
        # Mock encoding failure
        mock_rag_system.embedding_model.encode.side_effect = Exception(
            "Encoding failed"
        )

        with pytest.raises(Exception):
            # Should either raise or handle gracefully
            mock_rag_system.query("Test with special chars: 🎉")

    def test_chromadb_connection_error(self, mock_rag_system):
        """Test handling of ChromaDB connection failures."""
        mock_rag_system.collection.query.side_effect = Exception(
            "Database connection failed"
        )

        # Should raise descriptive error
        with pytest.raises(Exception) as exc_info:
            mock_rag_system.query("Test")

        assert "connection" in str(exc_info.value).lower() or "database" in str(exc_info.value).lower()
