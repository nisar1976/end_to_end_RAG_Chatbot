# Chapter 4: Git Workflow Integration

## Overview
Claude Code integrates seamlessly with Git, enabling you to manage version control directly alongside your development workflow. This chapter covers best practices for committing, managing branches, and creating pull requests.

## Setting Up Git with Claude Code

### Initial Configuration
Configure Git for Claude Code projects:

```bash
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### Initialize Repository
Start a new Git repository:

```bash
git init
git add .
git commit -m "Initial commit"
```

## Working with Commits

### Understanding Commits
A commit is a snapshot of your project at a specific point in time. Good commits are:
- Atomic (focused on one change)
- Well-documented with clear messages
- Logically grouped related changes
- Reversible if needed

### Creating Commits
Stage changes and commit:

```bash
# Check status
git status

# Stage files
git add filename.py
git add src/

# Commit with message
git commit -m "Fix login validation bug"
```

### Commit Message Format
Write effective commit messages:

```
[Type] Brief description (50 chars max)

Detailed explanation of the change. Explain what was changed,
why it was changed, and any important context.

- Point 1: Additional details
- Point 2: Impacts or testing notes

Fixes #123
```

### Commit Message Types
- **feat:** New feature
- **fix:** Bug fix
- **docs:** Documentation changes
- **style:** Code formatting
- **refactor:** Code restructuring
- **test:** Test additions/updates
- **chore:** Build, dependencies, etc.

### Examples
```bash
git commit -m "feat: Add user authentication system"
git commit -m "fix: Resolve null pointer in data parser"
git commit -m "docs: Update API documentation"
git commit -m "refactor: Simplify data validation logic"
```

## Managing Branches

### Creating Branches
Work on features in isolated branches:

```bash
# Create and switch to new branch
git checkout -b feature/user-auth

# Or using newer syntax
git switch -c feature/user-auth
```

### Branch Naming Conventions
Use descriptive branch names:

```
feature/add-login         # New feature
fix/auth-bug              # Bug fix
refactor/api-cleanup      # Code refactoring
docs/api-guide            # Documentation
test/coverage-improvement # Testing
```

### Switching Branches
Move between branches:

```bash
git checkout main
git switch develop
```

### Listing Branches
See all local and remote branches:

```bash
# Local branches
git branch

# Remote branches
git branch -r

# All branches
git branch -a
```

## Reviewing Changes

### Checking Status
See what's changed:

```bash
git status
```

### Viewing Diffs
Compare changes:

```bash
# Changes not yet staged
git diff

# Staged changes
git diff --cached

# Differences between branches
git diff main..feature/new-ui
```

### Viewing History
Review commit history:

```bash
# Last 10 commits
git log -10

# With formatted output
git log --oneline --graph --all

# Changes in specific file
git log -p filename.py
```

## Collaboration Workflows

### Pulling Latest Changes
Update your branch with remote changes:

```bash
# Fetch and merge
git pull origin main

# Fetch without merging
git fetch origin
```

### Pushing Changes
Send commits to remote:

```bash
# Push to tracking branch
git push

# Push to specific branch
git push origin feature/new-feature

# Push all branches
git push --all
```

### Handling Merge Conflicts
Resolve conflicts when merging:

```bash
# See conflicts
git status

# Read conflicted file
claude-code read "conflicted_file.py"

# Edit to resolve
claude-code edit "conflicted_file.py" \
  --old "<<<<<<< HEAD
  version_a
  =======
  version_b
  >>>>>>> branch" \
  --new "resolved_version"

# Mark as resolved
git add conflicted_file.py
git commit -m "Resolve merge conflict"
```

## Creating Pull Requests

### Preparing for PR
Before creating a pull request:

```bash
# Ensure branch is up to date
git pull origin main

# Run tests
npm test

# Review all changes
git diff main..HEAD

# Verify branch is pushed
git push origin feature/my-feature
```

### Creating a PR
Push your branch and create a pull request:

```bash
# Push changes
git push origin feature/feature-name

# Create PR (using GitHub CLI)
gh pr create --title "Add new feature" \
  --body "Description of changes"
```

### PR Description Template
Write clear PR descriptions:

```markdown
## Summary
Brief description of what this PR does.

## Changes
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Unit tests added
- [ ] Integration tests passed
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guide
- [ ] Documentation updated
- [ ] No breaking changes
```

## Common Git Workflows

### Feature Development Workflow
```bash
# 1. Create feature branch
git checkout -b feature/user-profile

# 2. Make changes and commit
claude-code edit "app.py" --old "old" --new "new"
git add app.py
git commit -m "feat: Add user profile page"

# 3. Push to remote
git push origin feature/user-profile

# 4. Create pull request
gh pr create --title "Add user profile page"

# 5. After PR approval, merge
git checkout main
git pull origin main
git merge feature/user-profile
```

### Bug Fix Workflow
```bash
# 1. Create fix branch from main
git checkout -b fix/login-bug

# 2. Identify and fix issue
claude-code read "auth.py"
claude-code edit "auth.py" --old "buggy_code" --new "fixed_code"

# 3. Test the fix
npm test

# 4. Commit with reference
git commit -m "fix: Resolve login timeout issue

Fixes #456"

# 5. Push and create PR
git push origin fix/login-bug
gh pr create
```

### Release Workflow
```bash
# 1. Create release branch
git checkout -b release/v1.2.0

# 2. Update version
claude-code edit "package.json" \
  --old '"version": "1.1.0"' \
  --new '"version": "1.2.0"'

# 3. Update changelog
claude-code edit "CHANGELOG.md" --old "Unreleased" --new "v1.2.0 - 2025-01-20"

# 4. Commit
git commit -m "chore: Release v1.2.0"

# 5. Create tag
git tag -a v1.2.0 -m "Release version 1.2.0"

# 6. Push
git push origin release/v1.2.0
git push origin v1.2.0
```

## Best Practices

### Commit Best Practices
✓ Commit frequently with logical grouping
✓ Write descriptive commit messages
✓ Keep commits atomic and focused
✓ Reference issues in commit messages
✓ Review changes before committing

### Branch Best Practices
✓ Use descriptive branch names
✓ Keep branches short-lived
✓ Keep branches updated with main
✓ Delete merged branches
✓ One feature per branch

### Collaboration Best Practices
✓ Communicate before major changes
✓ Review code before merging
✓ Write clear PR descriptions
✓ Respond to feedback promptly
✓ Keep commit history clean

## Troubleshooting

### Undoing Changes
```bash
# Unstage file
git reset HEAD filename.py

# Discard changes
git checkout -- filename.py

# Undo last commit (keep changes)
git reset --soft HEAD~1

# View lost commits
git reflog
```

### Recovering from Mistakes
```bash
# Amend last commit
git commit --amend -m "Corrected message"

# Revert specific commit
git revert <commit-hash>
```

## Integration with Claude Code Tools

### Combined Workflow
Use Claude Code tools alongside Git:

```bash
# 1. Search for code to modify
claude-code grep "deprecated_function" src/

# 2. Read relevant files
claude-code read "src/utils.py"

# 3. Make edits
claude-code edit "src/utils.py" --old "old" --new "new"

# 4. Check status
git status

# 5. Commit
git commit -m "refactor: Replace deprecated function"
```

## Next Steps
- Chapter 5 covers best practices and patterns
- Review the Git documentation for advanced topics
- Practice workflows with real projects
