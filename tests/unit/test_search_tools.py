"""Unit tests for search tools cache invalidation (Bug #9)."""
import pytest
import time
from pathlib import Path


class TestSearchToolsCache:
    """Test caching behavior in search_tools module."""

    def test_course_cache_invalidation(self):
        """Test that course cache is properly invalidated (Bug #9)."""
        # This test requires checking if search_tools.py has caching
        try:
            from backend.search_tools import get_course_outline, course_cache
        except ImportError:
            pytest.skip("search_tools module not available")

        # Get initial cache state
        initial_cache_size = len(course_cache) if hasattr(course_cache, '__len__') else 0

        # Simulate cache being populated
        result1 = get_course_outline("test_course")

        # Get cache after first call
        after_first_cache = len(course_cache) if hasattr(course_cache, '__len__') else 0

        # Verify cache was used
        assert after_first_cache >= initial_cache_size, "Cache should populate"

        # Get again (should use cache)
        result2 = get_course_outline("test_course")

        assert result1 == result2, "Cached results should be identical"

        # Now test if cache ever invalidates
        # This test should FAIL if cache never clears (Bug #9)
        # In a real scenario, we'd modify the underlying data and expect new results
        # But since we can't easily do that in tests, we check the implementation
        # to see if there's any invalidation logic at all

        has_invalidation = False
        try:
            import inspect
            import backend.search_tools as st
            source = inspect.getsource(st)
            # Check if cache invalidation code exists
            if "cache.clear" in source or "cache = {}" in source or "del course_cache" in source:
                has_invalidation = True
        except:
            pass

        # This test should FAIL - proving no cache invalidation exists (Bug #9)
        assert has_invalidation, "Bug #9: No cache invalidation logic found"

    def test_cache_after_file_modification(self, temp_chapters_dir):
        """Test that cache reflects file modifications (Bug #9)."""
        try:
            from backend.search_tools import search_course_content, course_cache
        except ImportError:
            pytest.skip("search_tools module not available")

        # Create a test file
        test_file = Path(temp_chapters_dir) / "test_course.md"
        test_file.write_text("Original content")

        # Search and populate cache
        result1 = search_course_content("test_course", "content")

        # Modify the file
        time.sleep(0.1)  # Small delay
        test_file.write_text("Modified content")

        # Search again
        result2 = search_course_content("test_course", "content")

        # Results should differ if cache is invalidated
        # This test should FAIL - proving cache persists despite file changes (Bug #9)
        assert result1 != result2, "Bug #9: Cache should invalidate after file modification"

    def test_cache_with_new_file(self, temp_chapters_dir):
        """Test that new files are reflected in cache (Bug #9)."""
        try:
            from backend.search_tools import get_course_outline
        except ImportError:
            pytest.skip("search_tools module not available")

        # Get outline before new file
        initial_outline = get_course_outline("courses")

        # Add new file
        new_file = Path(temp_chapters_dir) / "new_course.md"
        new_file.write_text("New course content")

        # Get outline after new file
        updated_outline = get_course_outline("courses")

        # Should differ if cache invalidates
        # This test should FAIL - proving new files not reflected (Bug #9)
        assert initial_outline != updated_outline, "Bug #9: Cache should include new files"

    def test_cache_thread_safety(self):
        """Test that cache operations are thread-safe."""
        try:
            from backend.search_tools import course_cache
        except ImportError:
            pytest.skip("search_tools module not available")

        import threading

        results = []
        errors = []

        def access_cache():
            try:
                # Simulate concurrent cache access
                if hasattr(course_cache, 'get'):
                    course_cache.get("test_key")
                elif isinstance(course_cache, dict):
                    _ = course_cache.get("test_key")
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=access_cache) for _ in range(10)]

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        # Should not have race condition errors
        assert len(errors) == 0, f"Thread safety issues: {errors}"
