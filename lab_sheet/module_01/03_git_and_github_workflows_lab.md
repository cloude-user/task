# Lab Sheet 1.3: Git & GitHub Collaborative Workflows
> **Module 1:** Programming Foundations  
> **Topic 1.c:** Version Control, Branching, Pull Requests & Code Reviews  
> **Target:** Cloud Software Developer Trainees  

---

## 🎯 Lab Objectives
1. Initialize and configure local Git repositories.
2. Track code changes with `git status`, `git add`, and `git commit`.
3. Link local repositories to remote GitHub accounts.
4. Practice branching, merging, and submitting Pull Requests (PRs).

---

## 🛠️ Step-by-Step Hands-On Exercises

### Exercise 1: Git Configuration & Local Initialization
```bash
# 1. Configure global developer identity
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 2. Verify settings
git config --list

# 3. Create a project and initialize Git
mkdir git_practice && cd git_practice
git init

# 4. Create your first code file
echo "# My Cloud Developer Portfolio" > README.md

# 5. Check repository status
git status

# 6. Stage and commit the file
git add README.md
git commit -m "feat: initial commit with README"
```

---

### Exercise 2: Connecting to Remote GitHub
```bash
# 1. Rename default branch to main
git branch -M main

# 2. Add your GitHub repository as remote origin (replace URL with your own repo)
git remote add origin https://github.com/<your-username>/my-cloud-portfolio.git

# 3. Push code to GitHub
git push -u origin main
```

---

### Exercise 3: Branching & Feature Workflow
```bash
# 1. Create and switch to a new feature branch
git checkout -b feature/add-about-page

# 2. Create the new file
echo "## About Me: Aspiring AWS Cloud Software Developer" >> README.md

# 3. Stage and commit changes on the branch
git add README.md
git commit -m "feat: add about section in README"

# 4. Switch back to main and merge
git checkout main
git merge feature/add-about-page

# 5. Push updated main branch to GitHub
git push origin main
```

---

### ✅ Verification Checklist
- [ ] Git username and email configured.
- [ ] Local commit history visible via `git log --oneline`.
- [ ] Code successfully pushed and visible on personal GitHub profile.
