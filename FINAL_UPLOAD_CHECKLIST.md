# Final Upload Checklist

## 📦 What to Upload to GitHub

### ✅ Upload These Files

**Python Scripts:**
- `main.py`
- `upload_to_youtube.py`
- `upload_all_platforms.py`
- `upload_instagram.py`
- `upload_tiktok.py`
- `upload_facebook.py`
- `get_youtube_token.py`
- `verify_channel.py`
- `generate_topics.py`

**Config Files:**
- `requirements.txt`
- `topics.txt` (365 topics)
- `.gitignore`

**Folders:**
- `.github/workflows/daily-shorts.yml`
- `audio/music.mp3`

**Documentation:**
- All `.md` files (START_HERE.md, etc.)

### ❌ DO NOT Upload

- `client_secrets.json` ← Keep this on your computer ONLY!
- `output/` folder
- `images/` folder
- `__pycache__/` folder
- Any `.mp4`, `.jpg`, `.png` files

## 🔐 About client_secrets.json

**Where to put it:** 
```
c:\Users\kreg9\Downloads\kreggscode\Anti gravity\bots\Youtube automation\client_secrets.json
```

**What it's for:**
- You use it LOCALLY to run `get_youtube_token.py`
- It generates the refresh token
- You add the refresh token to GitHub Secrets
- You NEVER upload `client_secrets.json` to GitHub!

**The `.gitignore` file already blocks it from being uploaded.**

## 🚀 Upload Steps

### 1. Test Video Generation (Do This Now)

```bash
python main.py
```

Check `output/final_video.mp4` - should have:
- Russian narration
- 8 beautiful women images
- UPPERCASE Russian subtitles
- Background music

### 2. Get YouTube Credentials

**You said you have `client_secrets.json` - put it here:**
```
c:\Users\kreg9\Downloads\kreggscode\Anti gravity\bots\Youtube automation\client_secrets.json
```

**Then run:**
```bash
python get_youtube_token.py
```

This will:
- Open browser
- Ask you to login
- SELECT your Russian YouTube channel
- Print 3 values:
  - `CLIENT_ID`
  - `CLIENT_SECRET`
  - `REFRESH_TOKEN`

**COPY THESE 3 VALUES!**

### 3. Upload to GitHub (Manual)

**On GitHub.com:**
1. Create new **private** repository
2. Name: `russian-history-shorts`
3. **Don't** initialize with README
4. Click "uploading an existing file"
5. **Drag and drop ALL files** from your project folder
   - Except `client_secrets.json`!
   - Except `output/` and `images/` folders
6. Commit

### 4. Add GitHub Secrets

**In your repo on GitHub:**
1. Settings → Secrets → Actions
2. Click "New repository secret" (3 times)

**Add these:**

| Secret Name | Value |
|-------------|-------|
| `YT_CLIENT_ID` | (paste from step 2) |
| `YT_CLIENT_SECRET` | (paste from step 2) |
| `YT_REFRESH_TOKEN` | (paste from step 2) |

### 5. Run Workflow

1. Go to **Actions** tab
2. Click "Daily Auto Shorts with YouTube Upload"
3. Click "Run workflow"
4. Wait 6-8 minutes
5. Check your YouTube channel!

## 📊 What Happens

**Daily at 9 PM India time:**
1. Picks today's topic (from 365 topics)
2. Generates Russian story
3. Generates 8 beautiful women images
4. Creates Russian narration
5. Creates UPPERCASE subtitles
6. Animates with Ken Burns effect
7. Adds background music
8. Uploads to YouTube (+ Instagram/TikTok/Facebook if configured)

## 🎯 Summary

**client_secrets.json location:**
```
c:\Users\kreg9\Downloads\kreggscode\Anti gravity\bots\Youtube automation\client_secrets.json
```

**Use it for:**
- Running `get_youtube_token.py` locally
- Getting the 3 secrets

**Never upload it to GitHub!**

**Upload everything else to GitHub (private repo)**
