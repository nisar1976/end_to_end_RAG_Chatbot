---
title: "Tools Overview"
url: "https://docs.anthropic.com/claude-code/tools"
---

# Chapter 2: Tools Overview

## Introduction to Tools
Claude Code provides a comprehensive set of tools designed to handle different aspects of software development. These tools enable you to read, write, edit, search, and execute code across your project.

## Core Tools

### 1. Read Tool
The Read tool allows you to examine file contents without modifying them.

**Use Cases:**
- View file contents
- Inspect configuration files
- Review code before editing
- Read documentation

**Example:**
```bash
claude-code read "src/main.py"
```

**Features:**
- Read up to 2000 lines at once
- Specify line offsets and limits for large files
- Works with binary files, PDFs, images, and Jupyter notebooks
- Preserves formatting and line numbers

### 2. Write Tool
The Write tool creates new files with specified content.

**Use Cases:**
- Generate new files
- Create boilerplate code
- Write documentation
- Generate configuration files

**Example:**
```bash
claude-code write "requirements.txt" --content "flask==2.0.0\nrequests==2.25.1"
```

**Features:**
- Creates file with exact content
- Overwrites existing files
- Works with text and binary formats
- Maintains proper encoding

### 3. Edit Tool
The Edit tool modifies existing files with surgical precision.

**Use Cases:**
- Fix bugs in existing code
- Update functions
- Modify configurations
- Add or remove code sections

**Example:**
```bash
claude-code edit "app.py" --old "def hello():" --new "def hello_world():"
```

**Features:**
- Find and replace exact strings
- Preserves indentation
- Supports multiline replacements
- Shows diffs before applying

### 4. Bash Tool
Execute shell commands and terminal operations.

**Use Cases:**
- Run tests
- Execute build commands
- Git operations
- Install dependencies

**Example:**
```bash
claude-code bash "npm install && npm test"
```

**Features:**
- Execute any shell command
- Capture output
- Set timeouts (up to 600 seconds)
- Background execution support

### 5. Grep Tool
Search file contents using regex patterns.

**Use Cases:**
- Find specific code patterns
- Locate function definitions
- Search for error messages
- Identify usage patterns

**Example:**
```bash
claude-code grep "def.*api" src/ --type py
```

**Features:**
- Regex support (ripgrep syntax)
- Filter by file type
- Show context lines (-B, -A, -C flags)
- Case-insensitive search (-i flag)

### 6. Glob Tool
Find files matching patterns.

**Use Cases:**
- Locate configuration files
- Find all tests
- Identify unused files
- List assets

**Example:**
```bash
claude-code glob "**/*.test.js"
```

**Features:**
- Glob pattern support
- Recursive directory search
- Sort by modification time
- Efficient file discovery

## Tool Capabilities Matrix

| Tool | Read | Write | Execute | Interactive | Reversible |
|------|------|-------|---------|-------------|-----------|
| Read | ✓ | ✗ | ✗ | ✓ | ✓ |
| Write | ✗ | ✓ | ✗ | ✓ | ✗ |
| Edit | ✓ | ✓ | ✗ | ✓ | ✗ |
| Bash | ✗ | ✗ | ✓ | ✓ | ✗ |
| Grep | ✓ | ✗ | ✗ | ✓ | ✓ |
| Glob | ✓ | ✗ | ✗ | ✓ | ✓ |

## Tool Best Practices

### Reading Files
1. Always read before editing
2. Check file size for large files
3. Use offsets for targeted reading
4. Verify content matches expectations

### Writing Files
1. Create minimal viable files
2. Follow project conventions
3. Include necessary imports
4. Test immediately after creation

### Editing Code
1. Provide sufficient context for unique matches
2. Preserve formatting and indentation
3. Make surgical changes
4. Review changes before committing

### Bash Operations
1. Quote file paths with spaces
2. Use && for sequential commands
3. Set appropriate timeouts
4. Avoid dangerous flags without confirmation

## Tool Combinations

### Example: Code Refactoring
```bash
# 1. Find all occurrences
claude-code grep "oldFunction" src/

# 2. Read relevant files
claude-code read "src/utils.js"

# 3. Edit files
claude-code edit "src/utils.js" --old "oldFunction" --new "newFunction"

# 4. Verify changes
claude-code bash "npm test"
```

### Example: Project Analysis
```bash
# 1. Find all Python files
claude-code glob "**/*.py"

# 2. Search for patterns
claude-code grep "class.*:" --type py

# 3. Read implementation
claude-code read "src/models.py"
```

## Advanced Features

### Piping and Composition
Combine tools for complex workflows:
```bash
# Chain multiple commands
claude-code bash "find . -name '*.log' -exec rm {} +"
```

### Conditional Execution
```bash
# Only edit if grep finds matches
claude-code grep "TODO" src/ && claude-code read "src/main.py"
```

### Bulk Operations
```bash
# Process multiple files
for file in src/*.py; do
  claude-code read "$file"
done
```

## Next Steps
- Chapter 3 covers file operations in detail
- Chapter 4 explains git workflow integration
- Chapter 5 includes best practices and patterns
