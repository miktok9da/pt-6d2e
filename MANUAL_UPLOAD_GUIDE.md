# Manual GitHub Upload Guide

## 📦 What to Upload

Upload these files/folders to your GitHub repo:

### ✅ Required Files
```
main.py
upload_to_youtube.py
upload_all_platforms.py
upload_instagram.py
upload_tiktok.py
upload_facebook.py
get_youtube_token.py
verify_channel.py
requirements.txt
topics.txt
README.md
QUICKSTART.md
MULTIPLATFORM_SETUP.md
.gitignore
```

### ✅ Required Folders
```
.github/
  workflows/
    daily-shorts.yml
audio/
  music.mp3
  README.md
```

### ❌ DO NOT Upload
```
client_secrets.json  ← NEVER upload this!
youtube_credentials.json  ← NEVER upload this!
token.pickle
output/
images/
*.mp4
*.jpg
*.png
```

## 🌐 Manual Upload Steps

### Option 1: GitHub Web Interface (Easiest)

1. **Create New Repo**
   - Go to github.com
   - Click "+" → "New repository"
   - Name: `russian-history-shorts`
   - **Private:** ✅ YES
   - Don't initialize with README
   - Click "Create repository"

2. **Upload Files**
   - Click "uploading an existing file"
   - Drag and drop ALL files from the list above
   - **Important:** Also upload the `.github` folder
   - Commit message: "Initial commit"
   - Click "Commit changes"

3. **Upload Folders**
   - Create `.github/workflows/` folder structure
   - Upload `daily-shorts.yml` to `.github/workflows/`
   - Create `audio/` folder
   - Upload `music.mp3` and `README.md` to `audio/`

### Option 2: GitHub Desktop (If Available)

1. Download GitHub Desktop
2. Login with your other GitHub account
3. Add this folder as repository
4. Publish to GitHub (private)

### Option 3: ZIP Upload

1. **Create ZIP file** with all required files
2. **Upload to GitHub:**
   - Create new repo (private)
   - Use "Upload files" button
   - Extract ZIP and upload contents

## 🔐 After Upload - Add Secrets

1. **Go to your repo** on GitHub
2. **Settings** → **Secrets and variables** → **Actions**
3. **Click "New repository secret"** (3 times)

Add these 3 secrets:

| Secret Name | Where to Get Value |
|-------------|-------------------|
| `YT_CLIENT_ID` | From `client_secrets.json` → `installed.client_id` |
| `YT_CLIENT_SECRET` | From `client_secrets.json` → `installed.client_secret` |
| `YT_REFRESH_TOKEN` | Run `get_youtube_token.py` locally first |

## 📋 Getting the Secrets

### Step 1: Get client_secrets.json

1. Go to [console.cloud.google.com](https://console.cloud.google.com/)
2. Create project (or select existing)
3. Enable "YouTube Data API v3"
4. Create OAuth credentials:
   - Type: **Desktop app**
   - Download JSON
   - Save as `client_secrets.json` in project folder

### Step 2: Get Refresh Token (Run Locally)

```bash
# Make sure client_secrets.json is in the folder
python get_youtube_token.py
```

This will:
- Open browser
- Ask you to login
- **SELECT your Russian YouTube channel**
- Print 3 values

**Copy these values** - you'll add them as GitHub Secrets!

### Step 3: Extract Values from client_secrets.json

Open `client_secrets.json` in notepad:

```json
{
  "installed": {
    "client_id": "YOUR_CLIENT_ID_HERE",
    "client_secret": "YOUR_CLIENT_SECRET_HERE",
    ...
  }
}
```

Copy `client_id` and `client_secret`.

## ✅ Final Checklist

Before uploading to GitHub:

- [ ] Remove `client_secrets.json` from folder
- [ ] Remove `output/` folder
- [ ] Remove `images/` folder
- [ ] Keep `audio/music.mp3`
- [ ] Keep all `.py` files
- [ ] Keep all `.md` files
- [ ] Keep `.github/workflows/daily-shorts.yml`
- [ ] Keep `requirements.txt`
- [ ] Keep `topics.txt`

## 🚀 After Upload

1. ✅ Repo is uploaded (private)
2. ✅ 3 secrets added
3. ✅ Go to **Actions** tab
4. ✅ Click "Daily Auto Shorts with YouTube Upload"
5. ✅ Click "Run workflow"
6. ✅ Wait 6-8 minutes
7. ✅ Check your YouTube channel!

## 📝 Repository Settings

**Recommended settings:**

- **Visibility:** Private ✅
- **Actions:** Enabled ✅
- **Workflow permissions:** Read and write ✅

## ⚠️ Important Notes

1. **Never upload `client_secrets.json`** to GitHub
2. **Private repo** keeps everything secure
3. **Run `get_youtube_token.py` locally** before uploading
4. **Add secrets** before running workflow
5. **Test workflow manually** first

## 🎯 Quick Summary

1. Get `client_secrets.json` from Google Cloud
2. Run `get_youtube_token.py` locally
3. Upload project files to GitHub (private repo)
4. Add 3 secrets to GitHub
5. Run workflow
6. Videos auto-upload daily!
