---
title: "Getting Started with Claude Code"
url: "https://docs.anthropic.com/claude-code/getting-started"
---

# Chapter 1: Getting Started with Claude Code

## Introduction
Claude Code is Anthropic's official command-line interface (CLI) for Claude. It enables developers to work with Claude directly from their terminal, making it easy to integrate AI-powered coding assistance into your workflow.

## Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 14+ (optional, for some tools)
- A valid Anthropic API key

### Installation Steps

1. **Via pip (Recommended)**
   ```bash
   pip install claude-code
   ```

2. **Via npm**
   ```bash
   npm install -g claude-code
   ```

3. **From Source**
   ```bash
   git clone https://github.com/anthropics/claude-code.git
   cd claude-code
   pip install -e .
   ```

## Initial Setup

### 1. Authentication
Set your Anthropic API key as an environment variable:

```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

On Windows:
```cmd
set ANTHROPIC_API_KEY=your-api-key-here
```

### 2. Verify Installation
Test that Claude Code is working:

```bash
claude-code --version
claude-code --help
```

### 3. First Command
Get started with a simple query:

```bash
claude-code "What is the capital of France?"
```

## Understanding the CLI

### Basic Usage
```bash
claude-code [command] [options]
```

### Common Options
- `--model` - Specify which Claude model to use (default: claude-opus-4-6)
- `--context` - Add context files for the query
- `--verbose` - Enable verbose logging
- `--timeout` - Set operation timeout in seconds

## Project Workflow

### Example 1: Code Analysis
```bash
claude-code analyze-code main.py --model claude-opus-4-6
```

### Example 2: Generate Code
```bash
claude-code generate "Create a Python function that validates email addresses"
```

### Example 3: Debug Assistance
```bash
claude-code debug error.log --context src/
```

## Configuration

### .claude/config.json
Store persistent settings in your home directory:

```json
{
  "model": "claude-opus-4-6",
  "max_tokens": 2048,
  "temperature": 0.7,
  "timeout": 300
}
```

### Environment Variables
- `ANTHROPIC_API_KEY` - Your API key
- `CLAUDE_CODE_MODEL` - Default model override
- `CLAUDE_CODE_TIMEOUT` - Default timeout

## Troubleshooting

### API Key Not Found
Ensure your API key is set correctly:
```bash
echo $ANTHROPIC_API_KEY  # Linux/Mac
echo %ANTHROPIC_API_KEY%  # Windows
```

### Connection Issues
Check your internet connection and API key validity. Use `--verbose` for debugging.

### Permission Errors
On Linux/Mac, you may need to chmod the executable:
```bash
chmod +x /usr/local/bin/claude-code
```

## Next Steps
- Read Chapter 2 to learn about available tools
- Explore the tools reference for detailed usage
- Check out best practices in Chapter 5
