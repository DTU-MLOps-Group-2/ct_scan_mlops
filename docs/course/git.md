# Git Version Control Guide

Source: https://skaftenicki.github.io/dtu_mlops/s2_organisation_and_version_control/git/

## Core Git Workflow

**Three-stage process for committing changes:**
1. `git add` - moves changes to staging area
2. `git commit -m "message"` - creates local commit with unique hash
3. `git push` - uploads commit to remote repository

## Essential Commands

| Command | Purpose |
|---------|---------|
| `git help` | Display git help documentation |
| `git config credential.helper store` | Store credentials locally |
| `git config --global user.email <email>` | Set global email configuration |
| `git clone <url>` | Copy repository to local machine |
| `git status` | Check current branch and staging status |
| `git log` | View commit history |
| `git checkout -b <branch_name>` | Create and switch to new branch |
| `git checkout <branch_name>` | Switch between branches |
| `git switch <branch_name>` | Modern alternative to checkout |
| `git restore` | Revert changes in staging area |
| `git branch` | List and manage branches |
| `git pull` | Fetch and merge remote changes |
| `git merge <branch>` | Integrate branch into current branch |

## Branching Strategy

Create a new branch: `git checkout -b <my_branch_name>`

Remember to commit work before switching branches to avoid losing changes.

## Fork and Pull Request Workflow

1. Fork repository via GitHub interface
2. Clone your fork locally
3. Create feature branch on main branch
4. Make improvements and commit changes
5. Push to your fork
6. Submit pull request with description
7. Compare branches and review diff before creation

## Syncing Forked Repository

```bash
git remote add upstream <url-to-original-repo>
git fetch upstream
git checkout main
git merge upstream/main
```

## Merge Conflict Resolution

When conflicts occur during `git pull`, manually edit the conflicted file. Git marks sections with:
- `<<<<<<<` to `=======` (your local changes)
- `=======` to `>>>>>>>` (incoming changes)

Remove markers and reconcile code, then commit the merge.

## Pull Configuration Options

```bash
git config pull.rebase false  # merge strategy (default, recommended)
git config pull.rebase true   # rebase strategy for clean history
git config pull.ff only       # fast-forward only (strictest)
```

## Best Practices

- Write descriptive commit messages conveying meaningful intent
- Make each commit represent a logical unit of work
- Incorporate others' changes regularly
- Share changes frequently
- Coordinate with collaborators
- Avoid committing generated or temporary files
- Use `.gitignore` to exclude non-codebase files (data, API keys, environment files)

## Repository Verification

Check if directory is git repository:
```bash
ls -la .git  # Check for .git directory
git status   # Run git status
```

## In-Browser Editing

Change GitHub URL from `https://github.com/username/repository` to `https://github.dev/username/repository` for VS Code-like editing experience.
