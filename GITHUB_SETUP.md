# 🚀 GitHub Setup Guide

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `transparency-platform` (or your choice)
3. Description: `National Strategy Transparency Platform for Namibia`
4. Choose **Public** or **Private**
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click **Create repository**

## Step 2: Configure Git (First Time Only)

Set your name and email:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Step 3: Connect to GitHub

Copy the commands from GitHub's quick setup page, or use these:

```bash
# Navigate to project directory
cd /Users/angula/Desktop/transparencyplatform

# Add remote repository (replace with your GitHub URL)
git remote add origin https://github.com/yourusername/transparency-platform.git

# Verify remote
git remote -v

# Push to GitHub
git push -u origin main
```

## Step 4: Verify

Visit your GitHub repository URL to confirm all files are uploaded.

## 🔒 Important Security Notes

Before pushing, ensure:

1. ✅ `.env` files are NOT committed (they're in .gitignore)
2. ✅ Database files are NOT committed
3. ✅ `node_modules/` is NOT committed
4. ✅ No sensitive credentials in code

## 📝 Next Steps After Push

1. **Add Repository Description** on GitHub
2. **Add Topics**: `namibia`, `transparency`, `government`, `fastapi`, `react`, `typescript`
3. **Enable GitHub Pages** (optional - for documentation)
4. **Set up Branch Protection** for main branch
5. **Add Collaborators** if working in a team

## 🌟 Making Changes

After initial push, workflow:

```bash
# Make your changes
git add .
git commit -m "feat: Your feature description"
git push origin main
```

## 🔄 Working with Branches

Create feature branches for new work:

```bash
# Create and switch to new branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "feat: Add new feature"

# Push branch
git push origin feature/new-feature

# Create Pull Request on GitHub
```

## 📊 Repository Settings Recommendations

### General
- ✅ Enable Issues
- ✅ Enable Discussions
- ✅ Enable Projects (for task management)

### Branches
- ✅ Protect main branch
- ✅ Require pull request reviews
- ✅ Require status checks to pass

### Security
- ✅ Enable Dependabot alerts
- ✅ Enable security updates
- ✅ Set up code scanning (optional)

## 🆘 Troubleshooting

### Authentication Issues

If you get authentication errors:

1. Use Personal Access Token (PAT):
   - Go to GitHub Settings → Developer settings → Personal access tokens
   - Generate new token with `repo` scope
   - Use token as password when prompted

2. Or set up SSH keys:
   ```bash
   ssh-keygen -t ed25519 -C "your.email@example.com"
   # Add key to GitHub: Settings → SSH and GPG keys
   ```

### Large Files

If you have files >100MB:
```bash
# Use Git LFS
git lfs install
git lfs track "*.large_file_extension"
git add .gitattributes
```

## 📞 Need Help?

- GitHub Docs: https://docs.github.com
- Git Guide: https://git-scm.com/doc
- Create an issue in the repository

---

Good luck with your project! 🇳🇦
