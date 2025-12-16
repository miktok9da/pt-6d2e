# Push to Different GitHub Account - Quick Guide

## ✅ Private Repo is PERFECT for This!

**GitHub Actions works the same for private and public repos.**

Benefits of private repo:
- ✅ Your credentials stay private
- ✅ Your topics/content stay private
- ✅ GitHub Actions still runs (2,000 free minutes/month)
- ✅ Nobody can see your code or videos

## 🔄 Push to Different GitHub Account

### Option 1: Use GitHub CLI (Easiest)

```bash
# Login to your other GitHub account
gh auth login

# Create new private repo
gh repo create youtube-shorts-bot --private

# Push
git remote add origin https://github.com/YOUR_OTHER_USERNAME/youtube-shorts-bot.git
git branch -M main
git add .
git commit -m "Initial commit"
git push -u origin main
```

### Option 2: Use Git with Token

```bash
# 1. Go to GitHub (your other account)
#    Settings → Developer settings → Personal access tokens → Generate new token
#    Select: repo (all), workflow

# 2. Create repo on GitHub (click + → New repository)
#    Name: youtube-shorts-bot
#    Private: ✅ YES
#    Don't initialize with README

# 3. Push from command line
git init
git remote add origin https://github.com/YOUR_OTHER_USERNAME/youtube-shorts-bot.git
git branch -M main
git add .
git commit -m "YouTube Shorts automation bot"
git push -u origin main

# If it asks for credentials:
# Username: YOUR_OTHER_USERNAME
# Password: YOUR_PERSONAL_ACCESS_TOKEN (not your password!)
```

### Option 3: Change Git Config Temporarily

```bash
# Set different user for this repo only
git config user.name "Your Other Name"
git config user.email "your.other.email@gmail.com"

# Then push normally
git remote add origin https://github.com/YOUR_OTHER_USERNAME/youtube-shorts-bot.git
git push -u origin main
```

## 🔐 GitHub Actions with Private Repo

**Everything works exactly the same!**

1. Add your 3 secrets (Settings → Secrets → Actions):
   - `YT_CLIENT_ID`
   - `YT_CLIENT_SECRET`
   - `YT_REFRESH_TOKEN`

2. GitHub Actions runs automatically
3. Videos upload to YouTube
4. Nobody can see your repo or code

## 💰 Free Tier Limits

| Account Type | Actions Minutes/Month | Private Repos |
|--------------|----------------------|---------------|
| Free | 2,000 minutes | Unlimited |
| Pro | 3,000 minutes | Unlimited |

**Your bot uses ~300 min/month** = Well within free tier! ✅

## 🚨 Important: Don't Commit Secrets!

The `.gitignore` file already protects:
- ✅ `client_secrets.json`
- ✅ `youtube_credentials.json`
- ✅ `token.pickle`

These will NOT be pushed to GitHub.

## ✅ Recommended Setup

1. **Make repo PRIVATE** ✅
2. **Add secrets to GitHub** (not in code)
3. **Push to your other account**
4. **Enable Actions** (should be auto-enabled)
5. **Run workflow manually** to test

## 🎯 After Pushing

1. Go to repo → **Actions** tab
2. Click **"Daily Auto Shorts with YouTube Upload"**
3. Click **"Run workflow"**
4. Wait 6-8 minutes
5. Check your YouTube channel!

---

**Bottom line:** Private repo is actually BETTER for this project! ✅
