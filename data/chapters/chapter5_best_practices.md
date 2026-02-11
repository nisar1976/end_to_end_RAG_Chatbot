# Chapter 5: Best Practices & Advanced Usage

## Introduction
This chapter covers best practices, advanced patterns, and pro tips for using Claude Code effectively. These practices help you work more efficiently and maintain high code quality.

## Code Organization

### Project Structure Conventions
Organize your project logically:

```
project/
├── src/
│   ├── models/
│   ├── views/
│   ├── controllers/
│   └── utils/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── docs/
├── config/
└── data/
```

### Modular Code Design
Split functionality into focused modules:

```python
# Bad: Single large file
# app.py (3000+ lines)

# Good: Organized modules
# app/
#   ├── auth.py
#   ├── database.py
#   ├── models.py
#   └── routes.py
```

### Naming Conventions
Use clear, consistent naming:

```python
# Variables and functions: snake_case
user_name = "John"
def calculate_total_price():
    pass

# Classes: PascalCase
class UserProfile:
    pass

# Constants: UPPER_SNAKE_CASE
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30
```

## Working with Files Efficiently

### Before Editing
Always follow this checklist:

1. **Read first** - Understand the current state
2. **Verify context** - Ensure your understanding is correct
3. **Plan changes** - Know exactly what will change
4. **Check impact** - Consider side effects
5. **Stage changes** - Prepare git before editing

### Edit Strategy
Make edits methodically:

```bash
# 1. Read file
claude-code read "utils.py"

# 2. Identify exact text to replace
claude-code grep "old_function_name" src/

# 3. Edit with sufficient context
claude-code edit "utils.py" \
  --old "def old_function_name(x):
    return x * 2" \
  --new "def new_function_name(x):
    return x * 2"

# 4. Verify changes
claude-code read "utils.py"
```

### Handling Large Files
For files over 2000 lines:

```bash
# 1. Use grep to find relevant sections
claude-code grep "function_name" large_file.py

# 2. Read specific sections
claude-code read "large_file.py" --offset 500 --limit 100

# 3. Edit the specific section
claude-code edit "large_file.py" --old "old" --new "new"
```

## Advanced Search Patterns

### Finding Related Code
Locate all related functionality:

```bash
# Find all uses of a function
claude-code grep "calculate_tax" src/

# Find all class definitions
claude-code grep "^class " --type py src/

# Find TODO comments
claude-code grep "TODO|FIXME" src/ --type py

# Find imports
claude-code grep "^from|^import" --type py src/
```

### Complex Search Combinations
Combine tools for powerful searches:

```bash
# Find all test files
claude-code glob "**/*.test.js"

# Search within test files
claude-code grep "describe\|it\(" --type js --glob "**/*.test.js"

# Find specific patterns in multiple files
for file in $(claude-code glob "**/*.py"); do
  if claude-code grep "class.*Error" "$file"; then
    echo "$file has errors"
  fi
done
```

## Testing and Validation

### Running Tests
Always test after making changes:

```bash
# Run all tests
claude-code bash "npm test"
claude-code bash "pytest tests/"

# Run specific tests
claude-code bash "npm test -- --testNamePattern='auth'"

# Run with coverage
claude-code bash "npm test -- --coverage"
```

### Code Quality Tools
Maintain code standards:

```bash
# Linting
claude-code bash "eslint src/"
claude-code bash "pylint src/"

# Formatting
claude-code bash "black --check src/"
claude-code bash "prettier --check src/"

# Type checking (if applicable)
claude-code bash "mypy src/"
```

## Performance Optimization

### Identifying Bottlenecks
Use profiling to find slow code:

```bash
# Profile Python code
claude-code read "app.py"
# Add timing code, then run

# Check database queries
# Look for N+1 query problems

# Identify large files
claude-code bash "du -sh src/* | sort -h"
```

### Common Optimizations
Apply proven optimization patterns:

1. **Caching** - Cache expensive computations
2. **Lazy Loading** - Load data only when needed
3. **Batch Operations** - Group similar operations
4. **Indexing** - Add indexes for frequent queries
5. **Async Processing** - Use async for I/O operations

## Security Considerations

### Secure Coding Practices
Write secure code from the start:

```python
# Bad: SQL injection vulnerability
query = f"SELECT * FROM users WHERE id = {user_id}"

# Good: Use parameterized queries
query = "SELECT * FROM users WHERE id = ?"
db.execute(query, (user_id,))

# Bad: Hardcoded secrets
API_KEY = "sk_live_abcdef123456"

# Good: Use environment variables
API_KEY = os.environ.get('API_KEY')
```

### Input Validation
Always validate user input:

```python
def process_user_input(user_input):
    # Validate type
    if not isinstance(user_input, str):
        raise TypeError("Input must be string")

    # Validate length
    if len(user_input) > 1000:
        raise ValueError("Input too long")

    # Sanitize
    user_input = user_input.strip().lower()

    return user_input
```

### Environment Secrets
Keep secrets secure:

```bash
# Create .env file (add to .gitignore)
echo "API_KEY=your_secret_key" > .env

# Load in application
from dotenv import load_dotenv
load_dotenv()
```

## Debugging Techniques

### Systematic Debugging
Follow a methodical approach:

1. **Reproduce** - Consistently reproduce the issue
2. **Isolate** - Narrow down the problem area
3. **Hypothesis** - Form a theory about the cause
4. **Test** - Verify or refute the hypothesis
5. **Fix** - Apply the solution
6. **Verify** - Confirm the fix works

### Adding Debug Logging
Temporary logging for investigation:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def problematic_function(x):
    logger.debug(f"Input: {x}")
    result = x * 2
    logger.debug(f"Result: {result}")
    return result
```

### Common Issues and Solutions
```python
# Issue: None values causing AttributeError
# Solution: Check for None before accessing
if user is not None:
    name = user.name

# Issue: Off-by-one errors
# Solution: Test boundary conditions
assert my_function(0) == expected
assert my_function(1) == expected
assert my_function(max_value) == expected

# Issue: State mutations
# Solution: Use immutable patterns
new_list = old_list + [item]  # Good
old_list.append(item)         # May cause bugs
```

## Documentation Best Practices

### Docstrings
Document functions and classes:

```python
def calculate_discount(price, discount_percent):
    """Calculate the discounted price.

    Args:
        price: The original price (float)
        discount_percent: Discount percentage (0-100)

    Returns:
        The discounted price as a float

    Raises:
        ValueError: If discount_percent is not 0-100
    """
    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount must be 0-100")
    return price * (1 - discount_percent / 100)
```

### Code Comments
Comment non-obvious logic:

```python
# Good: Explains why, not what
# We cache this result because user lookup is expensive
cached_user = cache.get(user_id)

# Bad: Just restates code
# Get the user from cache
cached_user = cache.get(user_id)
```

### README Best Practices
Create helpful documentation:

```markdown
# Project Name

## Quick Start
Instructions to get running in 5 minutes

## Installation
Step-by-step setup instructions

## Usage
Examples of common tasks

## Architecture
Explanation of how it works

## Contributing
Guidelines for contributors

## License
License information
```

## Performance Tips

### File Operations
Work efficiently with files:

```bash
# Bad: Reading same file multiple times
data1 = read("file.json")
data2 = read("file.json")

# Good: Read once, reuse
data = read("file.json")
process(data)
```

### Bash Operations
Efficient shell usage:

```bash
# Bad: Multiple grep passes
grep "error" log.txt | grep "critical"

# Good: Single grep with pattern
grep "error.*critical" log.txt

# Bad: Unnecessary pipes
cat file.txt | grep "pattern"

# Good: Direct grep
grep "pattern" file.txt
```

## Workflow Optimization

### Common Workflows
Standardize your approach:

**Workflow 1: Quick Fix**
1. Grep to find the issue
2. Read the file
3. Edit the specific line
4. Verify with bash (run tests)
5. Commit

**Workflow 2: Feature Addition**
1. Read related files for patterns
2. Create new files following conventions
3. Edit existing files as needed
4. Run full test suite
5. Review all changes
6. Commit

**Workflow 3: Investigation**
1. Grep for error patterns
2. Read relevant files
3. Check git history for changes
4. Add debug logging
5. Run and reproduce
6. Fix based on findings

## Pro Tips

### Quick Navigation
Use glob effectively:

```bash
# All Python files in src
claude-code glob "src/**/*.py"

# Config files
claude-code glob "**/*.{json,yaml,yml}"

# Test files
claude-code glob "**/*.test.{js,py}"
```

### Batch Automation
Script repetitive tasks:

```bash
#!/bin/bash
# Update all requirements files
for req_file in $(find . -name "requirements*.txt"); do
  echo "Processing $req_file"
  claude-code read "$req_file"
done
```

### Integration Tips
Combine tools effectively:

```bash
# Find all TODO items and their context
grep -r "TODO" src/ | while read line; do
  file=$(echo "$line" | cut -d: -f1)
  claude-code read "$file" --limit 20
done
```

## Summary of Best Practices

### Do's ✓
- Read files before editing
- Use meaningful commit messages
- Keep changes focused and atomic
- Test after making changes
- Document non-obvious code
- Use version control consistently
- Review changes before committing
- Keep code DRY (Don't Repeat Yourself)

### Don'ts ✗
- Edit without reading first
- Make multiple unrelated changes in one commit
- Skip testing before committing
- Leave debug code in commits
- Hardcode secrets or configuration
- Ignore warnings and errors
- Force push to shared branches
- Commit large binary files

## Next Steps
- Apply these practices to real projects
- Develop your own optimization patterns
- Share techniques with your team
- Continuously refine your workflow
