# YouTube API Fix - Quick Guide

## 🔍 Problem Found

Your credentials are valid, but **YouTube Data API v3 is NOT enabled** in your Google Cloud project.

## ✅ How to Fix (5 minutes)

### Step 1: Go to Google Cloud Console
Open: https://console.cloud.google.com/

### Step 2: Select Your Project
- Click the project dropdown at the top
- Select the project you used for `client_secrets.json`

### Step 3: Enable YouTube Data API v3
1. Click the **☰ menu** (top left)
2. Go to: **APIs & Services** → **Library**
3. Search for: **"YouTube Data API v3"**
4. Click on it
5. Click the **"Enable"** button
6. Wait 30 seconds for it to activate

### Step 4: Re-run the Test
```bash
python test_local_credentials.py
```

This should now show:
- ✅ Authentication successful
- ✅ YouTube channel info
- The 3 values to copy to GitHub Secrets

### Step 5: Update GitHub Secrets
1. Go to your GitHub repo
2. **Settings** → **Secrets and variables** → **Actions**
3. Update or create these 3 secrets:
   - `YT_CLIENT_ID`
   - `YT_CLIENT_SECRET`
   - `YT_REFRESH_TOKEN`

## 🎯 After This

Your GitHub Actions workflow will be able to upload to YouTube!

## ⚠️ If You Still Get Errors

If the API is already enabled but you still get errors, you may need to:
1. Delete the old OAuth client in Google Cloud Console
2. Create a new one (follow GET_CLIENT_SECRETS.md)
3. Run `python get_youtube_token.py` again
4. Copy the new credentials to GitHub Secrets
