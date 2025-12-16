# 🚀 Quick Start Checklist

## ✅ Step 1: Get client_secrets.json (10 min)

See **GET_CLIENT_SECRETS.md** for detailed guide.

**Quick version:**
1. Go to [console.cloud.google.com](https://console.cloud.google.com/)
2. Create project
3. Enable "YouTube Data API v3"
4. Create OAuth credentials (Desktop app)
5. Download JSON → rename to `client_secrets.json`
6. Put in project folder

## ✅ Step 2: Get Refresh Token (2 min)

```bash
python get_youtube_token.py
```

- Opens browser
- Login to Google
- **SELECT your Russian YouTube channel**
- Copy the 3 printed values:
  - `CLIENT_ID`
  - `CLIENT_SECRET`
  - `REFRESH_TOKEN`

## ✅ Step 3: Upload to GitHub (5 min)

See **MANUAL_UPLOAD_GUIDE.md** for detailed guide.

**Quick version:**
1. Go to github.com
2. Create new **private** repository
3. Upload these files (drag & drop):
   - All `.py` files
   - All `.md` files
   - `requirements.txt`
   - `topics.txt`
   - `.gitignore`
   - `.github/workflows/daily-shorts.yml`
   - `audio/music.mp3`

**DO NOT upload:**
- `client_secrets.json` ❌
- `output/` folder ❌
- `images/` folder ❌

## ✅ Step 4: Add GitHub Secrets (2 min)

In your GitHub repo:
1. Settings → Secrets → Actions
2. Click "New repository secret" (3 times)

Add these:

| Name | Value |
|------|-------|
| `YT_CLIENT_ID` | (from step 2) |
| `YT_CLIENT_SECRET` | (from step 2) |
| `YT_REFRESH_TOKEN` | (from step 2) |

## ✅ Step 5: Run Workflow (1 min)

1. Go to **Actions** tab
2. Click "Daily Auto Shorts with YouTube Upload"
3. Click "Run workflow"
4. Select branch: `main`
5. Click green "Run workflow" button

## ⏱️ Step 6: Wait (6-8 min)

Watch the workflow run:
- ✅ Setup Python
- ✅ Install dependencies
- ✅ Generate Russian story
- ✅ Generate 8 beautiful images
- ✅ Create narration
- ✅ Create subtitles
- ✅ Create video with animation
- ✅ Upload to YouTube

## 🎉 Step 7: Check YouTube!

Go to your YouTube channel → Check for new Short!

## 🔄 Daily Automation

After first successful run:
- Videos auto-generate daily at 6 AM UTC (11:30 AM India)
- No manual action needed
- Check your channel to see new videos!

## 📝 Files You Need

**On your computer:**
- ✅ `client_secrets.json` (keep private, don't upload)

**On GitHub:**
- ✅ All project files (except client_secrets.json)
- ✅ 3 secrets configured

## ⚠️ Common Issues

**"client_secrets.json not found"**
→ Follow GET_CLIENT_SECRETS.md to get it

**"Invalid credentials"**
→ Re-run `get_youtube_token.py` and update secrets

**"Workflow failed"**
→ Check Actions logs for error details

**"Video not on YouTube"**
→ Check if secrets are set correctly
→ Verify you selected correct channel in step 2

## 🎯 That's It!

Total time: ~20 minutes
Then: Automatic daily videos forever! 🚀
