# Push to Different GitHub Without Changing Credentials

## 🎯 Problem

You have multiple GitHub accounts, and your laptop is configured for one account, but you want to push to a different account.

## ✅ Solution: Use Personal Access Token (PAT)

This works **without changing** your laptop's git config!

### Step 1: Create Personal Access Token

1. **Login to your OTHER GitHub account** (the one you want to upload to)
2. Go to: **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
3. Click **"Generate new token (classic)"**
4. **Name:** "YouTube Automation"
5. **Expiration:** No expiration (or 1 year)
6. **Select scopes:**
   - ✅ `repo` (all)
   - ✅ `workflow`
7. Click **"Generate token"**
8. **COPY THE TOKEN** (you won't see it again!)

### Step 2: Create Repo on GitHub

1. **On your OTHER GitHub account**
2. Click **"+"** → **"New repository"**
3. **Name:** `russian-history-shorts`
4. **Private:** ✅ YES
5. **Don't** initialize with README
6. Click **"Create repository"**

### Step 3: Push Using Token (One-Time Setup)

Open PowerShell in your project folder:

```powershell
cd "c:\Users\kreg9\Downloads\kreggscode\Anti gravity\bots\Youtube automation"

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Russian women's history automation"

# Add remote with YOUR_USERNAME and YOUR_TOKEN
git remote add origin https://YOUR_TOKEN@github.com/YOUR_OTHER_USERNAME/russian-history-shorts.git

# Push
git push -u origin main
```

**Replace:**
- `YOUR_TOKEN` = The token you copied in Step 1
- `YOUR_OTHER_USERNAME` = Your other GitHub username

### Example:

```powershell
git remote add origin https://ghp_abc123xyz456@github.com/myotheraccount/russian-history-shorts.git
git push -u origin main
```

## ✅ This Works Because:

- The token is in the URL, so git uses it instead of your laptop's credentials
- Your laptop's git config stays unchanged
- No credential conflicts!

## 🔒 Security Note

The token gives full access to that account, so:
- Keep it private
- Don't share it
- You can revoke it anytime on GitHub

## 🎯 Alternative: GitHub CLI

Even easier:

```powershell
# Install GitHub CLI (if not installed)
winget install GitHub.cli

# Login to your OTHER account
gh auth login

# Create repo and push
gh repo create russian-history-shorts --private --source=. --remote=origin --push
```

This lets you switch between accounts easily!

## 📝 Summary

**Option 1:** Use Personal Access Token in git URL
**Option 2:** Use GitHub CLI (`gh`)
**Option 3:** Manual upload (drag & drop on GitHub.com)

All work without changing your laptop's git credentials!
