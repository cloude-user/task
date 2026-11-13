# Git & GitHub Mastery Cheat Sheet
> **Trainer:** Sundeep Hiremat  
> **Program:** TASK Telangana · Cloud Software Developer  
> **Reference:** `Git_and_GitHub_Mastery.pdf`

---

## 1. The 3 Areas of Git + Remote Highway

```
 [ Working Directory ]  ---> git add <file> --->  [ Staging Area (Index) ]
          |                                               |
          |                                          git commit -m
          |                                               v
 [ Remote (GitHub) ]   <--- git push origin main <--- [ Local Repository (.git) ]
```

| Area | Purpose | Key Commands |
|---|---|---|
| **Working Directory** | Your local folder with untracked/modified files | `git status`, `git diff` |
| **Staging Area (Index)**| Preparing changes ready to be snapshotted | `git add <file>`, `git restore --staged <file>` |
| **Local Repo (`.git`)** | Immutable DAG snapshots (commits) on disk | `git commit -m "..."`, `git log --oneline` |
| **Remote (GitHub)** | Central collaborative cloud repository | `git push`, `git fetch`, `git pull` |

---

## 2. Essential Commands Quick Reference

### Setup & Configuration
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global init.defaultBranch main
```

### Initializing & Cloning
```bash
# Initialize brand new repository
git init
git branch -M main

# Clone existing repository from GitHub
git clone https://github.com/cloude-user/task.git
```

### Daily Development Loop
```bash
# 1. Check status
git status

# 2. Stage changes
git add .                     # Stage all tracked & untracked changes
git add path/to/file.py       # Stage specific file

# 3. Commit with Conventional Commits
git commit -m "feat(python): add variables and data structures notebooks"

# 4. View commit history
git log --oneline --graph --decorate -n 10
```

---

## 3. Conventional Commits Standard

Write commit messages that machines and teams can easily read:

```
<type>[optional scope]: <description in imperative mood>

[optional body]

[optional footer(s)]
```

### Common Types:
- `feat`: A new feature or notebook added (e.g., `feat(aws): add IAM policy creation notebook`)
- `fix`: A bug fix in existing code (e.g., `fix(boto3): correct ec2 instance filter tag`)
- `docs`: Documentation updates only (e.g., `docs(readme): add day 1 architecture diagram`)
- `style`: Formatting, missing semi-colons, no code logic change
- `refactor`: Refactoring code without changing functionality or fixing bugs
- `chore`: Maintenance, updating `.gitignore`, repo configurations

---

## 4. Branching & Team Collaboration

```bash
# Create and switch to a new branch
git switch -c feature/day-02-ec2
# (Classic equivalent: git checkout -b feature/day-02-ec2)

# List all branches
git branch -a

# Switch back to main
git switch main

# Merge feature branch into main
git merge feature/day-02-ec2

# Delete merged branch
git branch -d feature/day-02-ec2
```

---

## 5. Connecting with GitHub Remote

```bash
# 1. Link your local repo to GitHub
git remote add origin https://github.com/cloude-user/task.git

# If origin already exists and you need to switch/update its URL:
git remote set-url origin https://github.com/cloude-user/task.git

# 2. Verify remote URL
git remote -v

# 3. Push main branch and set upstream tracking
git push -u origin main

# 4. Subsequent pushes
git push

# 5. Pull latest changes from team
git pull origin main
```

---

## 6. The Undo Safety Net

| Scenario | Recommended Command |
|---|---|
| Discard uncommitted changes in working file | `git restore <file>` |
| Unstage a file (keep local modifications) | `git restore --staged <file>` |
| Amend the last commit message | `git commit --amend -m "new message"` |
| Revert a pushed commit safely | `git revert <commit-hash>` |
| Soft reset (keep staging & working tree) | `git reset --soft HEAD~1` |

---

## 7. The Golden Security Rule

> ⚠️ **NEVER COMMIT CLOUD SECRETS**
> - Always add `.env`, `*.pem`, `*.key`, `aws_credentials`, and `credentials.csv` to `.gitignore`.
> - Always provide a dummy `.env.example` for students and teammates.
