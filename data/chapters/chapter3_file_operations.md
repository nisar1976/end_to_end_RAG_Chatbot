---
title: "File Operations"
url: "https://docs.anthropic.com/claude-code/file-operations"
---

# Chapter 3: File Operations

## Overview
File operations form the core of Claude Code's capabilities. Whether you're reading existing code, creating new files, or modifying existing ones, understanding how to work with files efficiently is essential.

## Reading Files

### Basic Reading
Read the entire contents of a file:

```bash
claude-code read "path/to/file.py"
```

### Reading Large Files
For files larger than 2000 lines, use offset and limit:

```bash
# Read lines 100-200
claude-code read "path/to/large_file.txt" --offset 100 --limit 100

# Read lines 1-50
claude-code read "path/to/large_file.txt" --limit 50
```

### Reading Binary Files
Claude Code can read and display binary files, including PDFs and images:

```bash
claude-code read "diagram.png"
claude-code read "document.pdf"
```

### Reading Jupyter Notebooks
Extract code and visualizations from notebooks:

```bash
claude-code read "analysis.ipynb"
```

### Tips for Reading
- Always read before editing to understand context
- Use grep first to find relevant sections
- Check file size to determine if you need offsets
- Preview configuration files before making changes

## Creating Files

### Simple File Creation
Create a new file with content:

```bash
claude-code write "config.json" --content '{"debug": true, "port": 8000}'
```

### Creating Multi-line Files
Use heredoc syntax for multiple lines:

```bash
claude-code write "README.md" --content "# Project Name

## Description
This is my project.

## Usage
Run it with: python main.py"
```

### Creating from Templates
Create files based on project conventions:

```bash
# Create a Python module with imports
claude-code write "utils.py" --content "import os
import sys

def helper_function():
    pass"
```

### File Creation Best Practices
1. Only create files when necessary
2. Follow project naming conventions
3. Include essential boilerplate
4. Keep initial versions minimal
5. Don't create duplicate files

## Editing Files

### Basic Editing
Replace exact text in a file:

```bash
claude-code edit "app.py" \
  --old "def process(data):" \
  --new "def process_data(data):"
```

### Multiline Editing
Edit larger blocks of code:

```bash
claude-code edit "main.py" \
  --old "if __name__ == '__main__':
    app.run()" \
  --new "if __name__ == '__main__':
    app.run(debug=True, port=5000)"
```

### Complex Replacements
When simple strings aren't unique enough, include context:

```bash
claude-code edit "utils.py" \
  --old "def validate(x):
    return x > 0" \
  --new "def validate(x):
    if not isinstance(x, (int, float)):
        raise TypeError('Must be numeric')
    return x > 0"
```

### Using Replace All
Replace all occurrences in a file:

```bash
claude-code edit "styles.css" \
  --old "color: blue;" \
  --new "color: #0066ff;" \
  --replace-all
```

## Structured File Operations

### JSON Files
Read and understand JSON structure:

```bash
# Read configuration
claude-code read "config.json"

# Update a setting
claude-code edit "config.json" \
  --old '"port": 3000' \
  --new '"port": 8000'
```

### YAML Configuration
Work with YAML files:

```bash
# Examine deployment config
claude-code read "deployment.yaml"

# Update environment variable
claude-code edit "deployment.yaml" \
  --old 'environment: development' \
  --new 'environment: production'
```

### Code Files (Python, JavaScript, etc.)
Handle language-specific files:

```bash
# Read Python class
claude-code read "models.py"

# Update method
claude-code edit "models.py" \
  --old 'def save(self):' \
  --new 'def save(self, backup=True):'
```

### Markdown Files
Create and edit documentation:

```bash
# Create documentation
claude-code write "CONTRIBUTING.md" --content "# Contributing
Please follow PEP 8 for Python code."

# Update section
claude-code edit "README.md" \
  --old "## Installation" \
  --new "## Installation & Setup"
```

## File Organization Patterns

### Creating Project Structure
```bash
# Create directory tree
mkdir -p src/models src/utils src/views
mkdir -p tests/{unit,integration}
mkdir -p docs data config
```

### Organizing Imports
Structure file imports logically:

```python
# Standard library
import os
import sys

# Third-party
import flask
import numpy

# Local
from utils import helper
from models import User
```

### Consistent File Layouts
Standard patterns for different file types:

**Python modules:**
```python
"""Module docstring."""

import section

def function():
    pass

class MyClass:
    pass
```

**JavaScript files:**
```javascript
// Imports
const express = require('express');

// Constants
const PORT = 3000;

// Functions
function handler() {}

// Exports
module.exports = { handler };
```

## Advanced File Operations

### Batch Operations
Process multiple files:

```bash
# Apply same edit to multiple files
for file in src/*.py; do
  claude-code edit "$file" --old "old_pattern" --new "new_pattern"
done
```

### File Comparison
Compare files before and after:

```bash
# Copy original
cp original.py backup.py

# Make edits
claude-code edit original.py --old "a" --new "b"

# Compare (using diff tool)
diff backup.py original.py
```

### Version Control Integration
Track file changes:

```bash
# See file changes
git diff filename.py

# Read previous version
git show HEAD:filename.py | claude-code read

# Stage changes
git add filename.py
```

## Common File Operations Workflows

### Workflow 1: Bug Fix
1. Read the file with the bug
2. Identify the issue
3. Edit the specific function
4. Run tests to verify

### Workflow 2: Feature Addition
1. Read existing code for patterns
2. Create new file or edit existing
3. Follow established conventions
4. Run tests and linting

### Workflow 3: Code Refactoring
1. Find all references with grep
2. Read relevant files
3. Edit carefully with proper context
4. Run full test suite

## Best Practices Summary

✓ Always read before editing
✓ Keep edits surgical and focused
✓ Verify changes work before committing
✓ Follow project conventions
✓ Use meaningful file names
✓ Include necessary boilerplate
✓ Document non-obvious code
✓ Test immediately after changes

## Next Steps
- Chapter 4 covers git workflow integration
- Chapter 5 provides additional best practices
- Explore the examples in the documentation
