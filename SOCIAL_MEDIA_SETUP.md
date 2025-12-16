# Social Media API Setup Guide

Complete guide to setting up API credentials for all supported platforms.

## 📋 Overview

This automation supports uploading to:
- ✅ **YouTube** (Free, requires OAuth)
- ✅ **Instagram Reels** (Free, requires Business account)
- ✅ **Facebook Reels** (Free, requires Page)
- ✅ **Threads** (Free, uses Instagram API)
- ✅ **TikTok** (Free, requires app approval)
- ⚠️ **Twitter/X** (Requires paid API ~$100/month)

---

## 🎥 YouTube (Already Set Up!)

You've already completed this! Your credentials are in GitHub Secrets:
- `YT_CLIENT_ID`
- `YT_CLIENT_SECRET`
- `YT_REFRESH_TOKEN`

---

## 📸 Instagram Reels

### Requirements:
- Instagram Business or Creator account
- Facebook Page linked to Instagram
- Facebook App with Instagram Graph API

### Steps:

1. **Convert to Business Account:**
   - Open Instagram app → Settings → Account → Switch to Professional Account
   - Choose "Business" or "Creator"

2. **Create Facebook Page:**
   - Go to: https://www.facebook.com/pages/create
   - Create a page (any category)
   - Link it to your Instagram account

3. **Create Facebook App:**
   - Go to: https://developers.facebook.com/apps
   - Click "Create App"
   - Choose "Business" type
   - Add "Instagram Graph API" product

4. **Get Access Token:**
   - In your app, go to Tools → Graph API Explorer
   - Select your Page
   - Add permissions: `instagram_basic`, `instagram_content_publish`, `pages_read_engagement`
   - Click "Generate Access Token"
   - Copy the token

5. **Get Instagram User ID:**
   - In Graph API Explorer, make this request:
     ```
     GET /me/accounts
     ```
   - Find your Instagram Business Account ID

6. **Add to GitHub Secrets:**
   - `IG_ACCESS_TOKEN` = Your access token
   - `IG_USER_ID` = Your Instagram Business Account ID

---

## 📘 Facebook Reels

### Requirements:
- Facebook Page
- Facebook App

### Steps:

1. **Create Facebook Page** (if you don't have one):
   - Go to: https://www.facebook.com/pages/create
   - Choose category and create

2. **Create Facebook App** (same as Instagram):
   - Go to: https://developers.facebook.com/apps
   - Create app → Add "Pages API" product

3. **Get Page Access Token:**
   - Graph API Explorer: https://developers.facebook.com/tools/explorer
   - Select your app
   - Select your Page
   - Add permissions: `pages_manage_posts`, `pages_read_engagement`
   - Generate Access Token

4. **Get Page ID:**
   - Go to your Facebook Page
   - Click "About"
   - Scroll down to find Page ID

5. **Add to GitHub Secrets:**
   - `FB_ACCESS_TOKEN` = Your page access token
   - `FB_PAGE_ID` = Your page ID

---

## 🧵 Threads

### Requirements:
- Same as Instagram (Threads uses Instagram API)

### Steps:

Threads uses the **exact same credentials** as Instagram!

1. **Use Instagram credentials:**
   - `THREADS_ACCESS_TOKEN` = Same as `IG_ACCESS_TOKEN`
   - `THREADS_USER_ID` = Same as `IG_USER_ID`

2. **Add to GitHub Secrets:**
   - `THREADS_ACCESS_TOKEN` = Your Instagram access token
   - `THREADS_USER_ID` = Your Instagram user ID

---

## 🎵 TikTok

### Requirements:
- TikTok account
- TikTok Developer account
- App approval from TikTok

### Steps:

1. **Create TikTok Developer Account:**
   - Go to: https://developers.tiktok.com/
   - Sign up with your TikTok account

2. **Create App:**
   - Dashboard → Create App
   - Fill in app details
   - Add "Content Posting API" product
   - **Submit for review** (takes 1-2 weeks)

3. **Get Credentials (after approval):**
   - Go to your app dashboard
   - Copy Client Key and Client Secret

4. **Get Access Token:**
   - Follow TikTok's OAuth flow
   - Or use their test token for development

5. **Add to GitHub Secrets:**
   - `TIKTOK_ACCESS_TOKEN` = Your access token
   - `TIKTOK_CLIENT_KEY` = Your client key (optional)
   - `TIKTOK_CLIENT_SECRET` = Your client secret (optional)

---

## 🐦 Twitter/X (Optional - Paid)

### Requirements:
- Twitter Developer Account
- **Elevated API access (~$100/month)** for video uploads
- Twitter app

### Steps:

1. **Create Developer Account:**
   - Go to: https://developer.twitter.com/
   - Apply for developer account
   - **Upgrade to Elevated access** ($100/month)

2. **Create App:**
   - Developer Portal → Create Project → Create App
   - Note down API Key and API Secret

3. **Generate Access Tokens:**
   - In your app settings
   - Generate Access Token and Secret
   - Set permissions to "Read and Write"

4. **Add to GitHub Secrets:**
   - `TWITTER_API_KEY` = Your API key
   - `TWITTER_API_SECRET` = Your API secret
   - `TWITTER_ACCESS_TOKEN` = Your access token
   - `TWITTER_ACCESS_SECRET` = Your access token secret

---

## 🔧 Adding Secrets to GitHub

For each platform you want to enable:

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"**
4. Enter the secret name (e.g., `IG_ACCESS_TOKEN`)
5. Paste the value
6. Click **"Add secret"**

Repeat for all credentials.

---

## ✅ Testing

Test each platform locally before pushing to GitHub:

```bash
# Set environment variables
export IG_ACCESS_TOKEN="your_token"
export IG_USER_ID="your_id"
# ... (set others)

# Test individual platforms
python upload_instagram.py
python upload_facebook.py
python upload_threads.py
python upload_tiktok.py
python upload_twitter.py

# Test all platforms
python upload_all_platforms.py
```

---

## 📊 Platform Comparison

| Platform | Cost | Setup Difficulty | Approval Required |
|----------|------|------------------|-------------------|
| YouTube | Free | Medium | No |
| Instagram | Free | Medium | No |
| Facebook | Free | Medium | No |
| Threads | Free | Easy (uses Instagram) | No |
| TikTok | Free | Hard | Yes (1-2 weeks) |
| Twitter/X | $100/month | Medium | No |

---

## 🎯 Recommended Setup Order

1. **Start with free platforms:**
   - ✅ YouTube (already done!)
   - ✅ Instagram Reels
   - ✅ Threads (same as Instagram)
   - ✅ Facebook Reels

2. **Skip expensive platforms:**
   - ⏭️ Twitter/X (unless you need it)

3. **Apply for TikTok last:**
   - ⏭️ TikTok (requires approval, takes time)

---

## 🆘 Troubleshooting

### "Access token expired"
- Tokens expire! Generate new ones every 60 days
- Use long-lived tokens when possible

### "Insufficient permissions"
- Make sure you added all required permissions when generating tokens
- Re-generate token with correct permissions

### "Video format not supported"
- All platforms require:
  - 9:16 aspect ratio (vertical)
  - MP4 format
  - <60 seconds duration
  - Your videos already meet these requirements!

### "API quota exceeded"
- Each platform has daily limits
- YouTube: 10,000 units/day (1 upload = ~1600 units)
- Instagram/Facebook: Varies by account
- TikTok: Varies by app

---

## 📞 Support

- **YouTube API**: https://developers.google.com/youtube
- **Instagram/Facebook**: https://developers.facebook.com/docs/instagram-api
- **TikTok**: https://developers.tiktok.com/doc
- **Twitter**: https://developer.twitter.com/en/docs

---

**You're all set!** Start with Instagram and Facebook (free and easy), then expand to other platforms as needed.
