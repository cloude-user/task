# Live Classroom Demo: Git Commands & Remote Management
> **Trainer:** Sundeep Hiremath  
> **GitHub Organization/User:** [`cloude-user`](https://github.com/cloude-user)  
> **Target Repository:** `https://github.com/cloude-user/task.git`  
> **Reference Guide:** `Git_and_GitHub_Mastery.pdf`

---

## 🎯 What We Are Demonstrating to the Class

1. How Git works locally (Working Directory ➔ Staging Area ➔ Local Repo).
2. How to set your repository author identity (`user.name` & `user.email`).
3. How to check, add, switch, or remove a GitHub Remote (`origin`).
4. How to push your local code and branch up to GitHub.

---

## 📋 Step-by-Step Command Playbook

### Step 1: Open Terminal in the Project Directory
```powershell
# Navigate to the project directory
cd "F:\Task( Telangana )\Nalgonda\Projects\task"
```

---

### Step 2: Configure Author Identity (Local to this Repo)
Demonstrate to students the difference between `--global` (all repos on computer) and local (this repository only):

```bash
# Set author identity for this specific repository
git config user.name "cloude-user"
git config user.email "sundeep@cloudexpert.io"

# Verify local repository settings
git config --local --list
```

---

### Step 3: Check Current Git Status & Commit History
```bash
# Check if working tree is clean
git status

# Inspect existing commits
git log --oneline --graph --decorate
```

---

### Step 4: Inspect & Manage the Remote URL

#### A. Check if any remote is already attached:
```bash
git remote -v
```
*(If empty, no remote has been added yet).*

#### B. Adding the Remote for the First Time:
```bash
git remote add origin https://github.com/cloude-user/task.git
```

#### C. How to Change / Update an Existing Remote URL:
Teach the students what to do if the URL was mistyped, or if switching accounts/repositories:
```bash
# Syntax: git remote set-url <remote-name> <new-url>
git remote set-url origin https://github.com/cloude-user/task.git

# Verify the updated remote URL
git remote -v
```

#### D. (Optional) How to rename or remove a remote:
```bash
# Remove a remote
git remote remove origin

# Rename a remote from origin to upstream
git remote rename origin upstream
```

---

### Step 5: Verify the Default Branch is `main`
```bash
# Ensure current branch is named 'main'
git branch -M main

# Check active branches
git branch
```

---

### Step 6: Staging & Committing Any New Updates
```bash
# Stage modified or newly added files
git add .

# Commit using Conventional Commits standard
git commit -m "docs(guide): add classroom git commands and remote demonstration guide"
```

---

### Step 7: Push to GitHub (`origin main`)
```bash
# First time push: -u sets upstream tracking
git push -u origin main
```

> **Classroom Note on GitHub Authentication:**
> When pushing for the first time on a machine:
> 1. A Git Credential Manager pop-up will appear asking to **Sign in with your browser**.
> 2. Alternatively, use a **GitHub Personal Access Token (PAT)** as your password (generated under GitHub Settings ➔ Developer Settings ➔ Personal Access Tokens ➔ Classic with `repo` scope).

---

### Step 8: Subsequent Daily Workflows
Once `-u origin main` is established, pushing and pulling becomes a single command:
```bash
# Send latest local commits to GitHub
git push

# Pull latest commits from GitHub to your laptop
git pull
```

---

## 💡 Quick Summary Table for Classroom Slides

| Action | Command | Purpose |
|---|---|---|
| **Check Remote** | `git remote -v` | See where code will be sent/fetched |
| **Add Remote** | `git remote add origin <URL>` | Connect local repo to GitHub |
| **Change Remote** | `git remote set-url origin <URL>` | Switch repository or update link |
| **Remove Remote** | `git remote remove origin` | Disconnect remote link |
| **Set Upstream & Push** | `git push -u origin main` | Upload code and remember default remote branch |
| **Daily Push** | `git push` | Quick push of new commits |

