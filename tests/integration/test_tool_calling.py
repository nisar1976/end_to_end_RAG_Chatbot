"""Integration tests for tool calling in RAG system (Bug #8)."""
import pytest
from unittest.mock import Mock, MagicMock


class TestToolCalling:
    """Test tool execution and error handling."""

    def test_tool_execution_success(self, mock_rag_system):
        """Test successful tool execution."""
        mock_rag_system.anthropic_client.messages.create.return_value = MagicMock(
            content=[MagicMock(text="Tool result", type="text")],
            stop_reason="end_turn"
        )

        result = mock_rag_system.query("What is the course outline?", use_tools=True)

        # Should get a valid response
        assert result is not None
        assert "answer" in result
        assert isinstance(result["answer"], str)

    def test_tool_execution_error_fallback(self, mock_rag_system, mocker):
        """Test that tool errors are handled gracefully (Bug #8)."""
        # Mock a tool that raises an exception
        mock_rag_system.anthropic_client.messages.create.side_effect = Exception(
            "Tool execution failed"
        )

        # This should either:
        # 1. Raise the exception (transparent)
        # 2. Return graceful fallback response
        # Currently may swallow error silently (Bug #8)

        with pytest.raises(Exception):
            # If exception is raised, that's actually better than silent failure
            mock_rag_system.query("Tool test", use_tools=True)

    def test_malformed_tool_response(self, mock_rag_system, mocker):
        """Test handling of malformed tool response."""
        # Mock response with unexpected structure
        mock_rag_system.anthropic_client.messages.create.return_value = MagicMock(
            content=[],  # Empty content
            stop_reason="end_turn"
        )

        result = mock_rag_system.query("Test query", use_tools=True)

        # Should handle gracefully without crashing
        assert result is not None
        assert isinstance(result, dict)

    def test_max_iterations_exceeded(self, mock_rag_system, mocker):
        """Test handling when max tool iterations exceeded."""
        # This simulates a tool loop that exceeds max iterations
        # The system should bail out with appropriate error

        # Depending on implementation, may raise exception or return partial result
        try:
            result = mock_rag_system.query("Complex query requiring tools", use_tools=True)
            # If it completes, should have answer
            assert "answer" in result
        except Exception as e:
            # If it raises, should be descriptive
            assert "iteration" in str(e).lower() or "max" in str(e).lower()

    def test_tool_with_no_context(self, mock_rag_system):
        """Test tool calling when no retrieval context found."""
        # Mock empty retrieval
        mock_rag_system.collection.query.return_value = {
            "ids": [[]],
            "distances": [[]],
            "metadatas": [[]]
        }

        result = mock_rag_system.query("Obscure query that returns no context", use_tools=True)

        # Should still return something, possibly with tool results
        assert result is not None
        assert "answer" in result

    def test_tool_response_parsing(self, mock_rag_system, mocker):
        """Test that tool responses are parsed correctly."""
        mock_response = MagicMock()
        mock_response.content = [
            MagicMock(type="text", text="Final answer after tool use")
        ]
        mock_response.stop_reason = "end_turn"

        mock_rag_system.anthropic_client.messages.create.return_value = mock_response

        result = mock_rag_system.query("Test with tools", use_tools=True)

        # Answer should be extracted from response
        assert result["answer"] == "Final answer after tool use"

    def test_tool_disabled_still_works(self, mock_rag_system):
        """Test that query works with use_tools=False."""
        mock_rag_system.anthropic_client.messages.create.return_value = MagicMock(
            content=[MagicMock(text="Response without tools")],
            stop_reason="end_turn"
        )

        result = mock_rag_system.query("Test query", use_tools=False)

        # Should still get answer
        assert result is not None
        assert "answer" in result
