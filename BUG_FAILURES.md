# Quick Reference: Bug Failures

## Bug #1 - Input Validation (CONFIRMED ❌)

### Tests Failing:
1. `tests/unit/test_validation.py::TestInputValidation::test_empty_query`
2. `tests/unit/test_validation.py::TestInputValidation::test_whitespace_only_query`
3. `tests/unit/test_validation.py::TestInputValidation::test_very_long_query`

### What's Wrong:
Empty queries and whitespace-only queries are not consistently validated. Very long queries (10,000+ chars) have no length limit.

### Example:
```python
# This should fail but may not
response = client.post("/api/query", json={"question": "   \n  \t  "})
# Expected: 400 Bad Request
# Actual: May pass through

# This has no limit
response = client.post("/api/query", json={"question": "a" * 10000})
# No length validation exists
```

### Code Location:
`main.py` lines 92-93

### Impact:
- Security: No DoS protection
- UX: Poor validation feedback
- Performance: Long queries strain API

---

## Bug #6 - Chunking Logic (CONFIRMED ❌)

### Tests Failing:
1. `tests/unit/test_chunking.py::TestChunkingLogic::test_chunking_without_space`
2. `tests/unit/test_chunking.py::TestChunkingLogic::test_chunking_in_code_blocks`

### What's Wrong:
Markdown chunking only recognizes `## ` with a space. Headers without space and code blocks containing `##` break the parser.

### Example 1 - Headers Without Space:
```markdown
##Section1NoSpace
Content here

##Section2NoSpace
More content
```

```python
chunks = rag._split_into_chunks(content, "test")
# Expected: 2 chunks (one for each ##)
# Actual: 1 chunk (##NoSpace not recognized)
print(len(chunks))  # Returns: 1 (WRONG!)
```

### Example 2 - Code Blocks:
```markdown
## Real Section

```python
## This looks like a header but it's code
x = 1
```

More content
```

```python
chunks = rag._split_into_chunks(content, "test")
# Expected: 1 chunk (code block ignored)
# Actual: 2 chunks (code block `##` treated as header)
print(len(chunks))  # Returns: 2 (WRONG!)
```

### Code Location:
`rag_system.py` line 163

```python
chunks = content.split('## ')  # Only handles '## ' with space
```

### Impact:
- Content Structure: Markdown not parsed correctly
- Data Integrity: Content split at wrong boundaries
- User Experience: Headers must have specific format

---

## Bug #9 - Cache Never Invalidates (CONFIRMED ❌)

### Test Failing:
`tests/unit/test_search_tools.py::TestSearchToolsCache::test_cache_with_new_file`

### What's Wrong:
Course cache in `search_tools.py` is never cleared. When new markdown files are added to the data directory, they don't appear in search results until server restart.

### Example:
```python
from backend.search_tools import get_course_outline

# Step 1: Get initial outline
outline_before = get_course_outline("courses")
print(outline_before["available_courses"])
# Output: 5 courses

# Step 2: Add a new chapter file
from pathlib import Path
new_file = Path("data/chapters/chapter6.md")
new_file.write_text("# New Chapter")

# Step 3: Get outline again
outline_after = get_course_outline("courses")
print(outline_after["available_courses"])
# Expected: 6 courses (new one included)
# Actual: 5 courses (cache unchanged)
# SAME RESULTS! Cache not invalidated!

assert outline_before != outline_after
# AssertionError: Cache not updated
```

### Code Location:
`backend/search_tools.py` - likely around line 64

Pattern:
```python
course_cache = {}  # Global cache never cleared

def get_course_outline(course_name):
    if course_name in course_cache:
        return course_cache[course_name]  # Always returns cached version

    # Load from filesystem...
    result = load_courses()
    course_cache[course_name] = result
    return result
```

### Impact:
- Data Freshness: New chapters don't appear
- Usability: Server restart required to update
- Maintenance: Users confused why changes don't reflect

---

## Bug #10 - YAML Parsing (NOT CONFIRMED ✅)

### Status:
**ALL TESTS PASSED** - This area is solid.

### Tests Passing:
```
✅ test_valid_yaml_extraction
✅ test_yaml_in_code_block
✅ test_missing_closing_yaml
✅ test_malformed_yaml
✅ test_multiple_yaml_separators
✅ test_empty_frontmatter
✅ test_no_frontmatter
✅ test_yaml_with_special_chars
✅ test_yaml_with_unicode
✅ test_remove_frontmatter
```

### Conclusion:
YAML parsing is **robust and correct**. No action needed for this component.

---

## Running Failed Tests Only

```bash
# All failures
uv run pytest tests/ -v --tb=short -x

# Specific failures
uv run pytest tests/unit/test_validation.py::TestInputValidation::test_empty_query -v
uv run pytest tests/unit/test_validation.py::TestInputValidation::test_whitespace_only_query -v
uv run pytest tests/unit/test_validation.py::TestInputValidation::test_very_long_query -v

uv run pytest tests/unit/test_chunking.py::TestChunkingLogic::test_chunking_without_space -v
uv run pytest tests/unit/test_chunking.py::TestChunkingLogic::test_chunking_in_code_blocks -v

uv run pytest tests/unit/test_search_tools.py::TestSearchToolsCache::test_cache_with_new_file -v
```

---

## Test Failure Output Examples

### test_chunking_without_space
```
AssertionError: assert 1 == 2
 +  where 1 = len([('', '##Section1NoSpace\nContent for section 1\n\n##Section2NoSpace\nContent for section 2')])
 >       assert len(chunks) == 2, "Bug #6: ##NoSpace should be recognized as headers"
```

### test_chunking_in_code_blocks
```
AssertionError: assert 2 == 1
 +  where 2 = len([..., ...])
 >       assert len(chunks) == 1, "Bug #6: ## in code blocks should not split chunks"
```

### test_cache_with_new_file
```
AssertionError: Bug #9: Cache should include new files
assert {
    'available_courses': [
        {'identifier': 'chapter1_getting_started', 'number': 1, ...},
        ...
    ],
    'error': "No course found matching 'courses'"
} != {
    'available_courses': [
        {'identifier': 'chapter1_getting_started', 'number': 1, ...},
        ...
    ],
    'error': "No course found matching 'courses'"
}  # Identical results - cache not updated!
```

---

## Next Steps

### To Fix Bug #1 (Input Validation):
1. Add maximum length validation
2. Normalize whitespace checking
3. Add content validation (prevent prompt injection)

### To Fix Bug #6 (Chunking):
1. Use regex instead of string split
2. Respect code block boundaries
3. Handle headers with/without space

### To Fix Bug #9 (Cache):
1. Add file watcher or modification timestamp check
2. Implement cache invalidation on file changes
3. Or add manual cache clear endpoint

---

## References

- Full report: `TEST_REPORT.md`
- Test code: `tests/` directory
- Implementation: See code locations listed above
