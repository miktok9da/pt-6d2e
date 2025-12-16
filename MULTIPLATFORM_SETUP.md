# Multi-Platform Upload Setup Guide

## 🎯 Platforms Supported

✅ **YouTube Shorts**
✅ **Instagram Reels**  
✅ **TikTok**
✅ **Facebook Reels**

## 📋 What You Need

### For YouTube (Required)
- Google Cloud Project
- OAuth Client ID + Secret
- Refresh Token

### For Instagram (Optional)
- Business/Creator Instagram account
- Connected Facebook Page
- Instagram Access Token + User ID

### For TikTok (Optional)
- TikTok Developer account
- OAuth Access Token

### For Facebook (Optional)
- Facebook Page
- Page Access Token + Page ID

## ⚡ Quick Start - YouTube Only

If you only want YouTube (easiest):

1. **Get `client_secrets.json`** from Google Cloud Console
2. **Run:** `python get_youtube_token.py`
3. **Add 3 GitHub Secrets:**
   - `YT_CLIENT_ID`
   - `YT_CLIENT_SECRET`
   - `YT_REFRESH_TOKEN`
4. **Push to GitHub** → Done!

## 🔧 Full Multi-Platform Setup

### 1. YouTube Setup

See `QUICKSTART.md` for detailed YouTube setup.

**GitHub Secrets needed:**
```
YT_CLIENT_ID
YT_CLIENT_SECRET
YT_REFRESH_TOKEN
```

### 2. Instagram Setup

**Requirements:**
- Instagram Business or Creator account
- Facebook Page connected to Instagram
- Facebook Developer App

**Steps:**
1. Create Facebook App at developers.facebook.com
2. Add Instagram Graph API product
3. Get User Access Token (long-lived)
4. Get Instagram Business Account ID

**GitHub Secrets needed:**
```
IG_ACCESS_TOKEN
IG_USER_ID
```

**Note:** Instagram requires video to be at a public URL. You may need to:
- Upload to temporary hosting (e.g., AWS S3, Cloudinary)
- Or use GitHub Actions artifacts URL

### 3. TikTok Setup

**Requirements:**
- TikTok Developer account
- Approved app for Content Posting API

**Steps:**
1. Register at developers.tiktok.com
2. Create app and request Content Posting API access
3. Complete OAuth flow to get access token

**GitHub Secrets needed:**
```
TIKTOK_ACCESS_TOKEN
```

### 4. Facebook Setup

**Requirements:**
- Facebook Page
- Facebook Developer App

**Steps:**
1. Create Facebook App
2. Add Pages API product
3. Get Page Access Token (long-lived)
4. Get Page ID

**GitHub Secrets needed:**
```
FB_ACCESS_TOKEN
FB_PAGE_ID
```

## 🚀 Usage

### Upload to YouTube Only
```bash
python upload_to_youtube.py
```

### Upload to All Platforms
```bash
python upload_all_platforms.py
```

The script automatically skips platforms without credentials.

## 📊 Platform Comparison

| Platform | Setup Difficulty | API Limits | Best For |
|----------|-----------------|------------|----------|
| YouTube | ⭐⭐ Easy | 10,000 units/day (~6 uploads) | Long-term growth |
| Instagram | ⭐⭐⭐ Medium | Rate limited | Visual content |
| TikTok | ⭐⭐⭐⭐ Hard | Approval required | Viral reach |
| Facebook | ⭐⭐⭐ Medium | Standard limits | Older audience |

## 💡 Recommendations

**Start with YouTube only:**
- Easiest setup
- Best for automation
- Good monetization potential

**Add Instagram next:**
- Good for discovery
- Younger audience
- Requires public video URL

**TikTok & Facebook:**
- More complex setup
- TikTok requires API approval
- Consider after YouTube is working

## 🔐 Security

**Never commit:**
- Access tokens
- Client secrets
- Refresh tokens

All credentials go in **GitHub Secrets** only!

## 📝 GitHub Actions Integration

Update `.github/workflows/daily-shorts.yml`:

```yaml
- name: Upload to all platforms
  env:
    # YouTube
    YT_CLIENT_ID: ${{ secrets.YT_CLIENT_ID }}
    YT_CLIENT_SECRET: ${{ secrets.YT_CLIENT_SECRET }}
    YT_REFRESH_TOKEN: ${{ secrets.YT_REFRESH_TOKEN }}
    # Instagram (optional)
    IG_ACCESS_TOKEN: ${{ secrets.IG_ACCESS_TOKEN }}
    IG_USER_ID: ${{ secrets.IG_USER_ID }}
    # TikTok (optional)
    TIKTOK_ACCESS_TOKEN: ${{ secrets.TIKTOK_ACCESS_TOKEN }}
    # Facebook (optional)
    FB_ACCESS_TOKEN: ${{ secrets.FB_ACCESS_TOKEN }}
    FB_PAGE_ID: ${{ secrets.FB_PAGE_ID }}
  run: |
    python upload_all_platforms.py
```

## ⚠️ Important Notes

1. **Instagram** requires video at public URL (not local file)
2. **TikTok** API access requires approval (can take weeks)
3. **YouTube** is the easiest and most reliable
4. **Facebook** works similar to Instagram

## 🎯 Recommended Approach

1. ✅ Start with **YouTube only**
2. ✅ Test for 1 week
3. ✅ Add **Instagram** if needed
4. ✅ Consider **TikTok/Facebook** later

**YouTube alone is enough for most use cases!**
