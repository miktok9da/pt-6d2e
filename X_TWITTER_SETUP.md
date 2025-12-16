# 🐦 X (Twitter) Setup Guide

## What You Need from X Developer Portal

You're looking at the right page! Here's exactly what to copy:

### 1. API Key and Secret (Consumer Keys)

On the page you're viewing, you should see:

```
Consumer Keys
API Key and Secret
[Reveal API Key] [Regenerate]
```

**Click "Reveal API Key"** and you'll see:
- **API Key** (looks like: `xxxxxxxxxxxxxxxxxxx`)
- **API Key Secret** (looks like: `xxxxxxxxxxxxxxxxxxxxxxxxxx`)

Copy these:
- API Key = `TWITTER_API_KEY` (for GitHub Secrets)
- API Key Secret = `TWITTER_API_SECRET` (for GitHub Secrets)

---

### 2. Access Token and Secret

On the same page, scroll down to:

```
Access Token and Secret
For @thriveruswave
[Generate]
```

**Click "Generate"** and you'll see:
- **Access Token** (looks like: `xxxxxxxxxx-xxxxxxxxxxxxxxxxx`)
- **Access Token Secret** (looks like: `xxxxxxxxxxxxxxxxxxxxxxxxxx`)

Copy these:
- Access Token = `TWITTER_ACCESS_TOKEN` (for GitHub Secrets)
- Access Token Secret = `TWITTER_ACCESS_SECRET` (for GitHub Secrets)

---

## Summary: 4 Things You Need

| What X Shows | What to Copy to GitHub Secrets |
|--------------|-------------------------------|
| API Key | `TWITTER_API_KEY` |
| API Key Secret | `TWITTER_API_SECRET` |
| Access Token | `TWITTER_ACCESS_TOKEN` |
| Access Token Secret | `TWITTER_ACCESS_SECRET` |

---

## How to Add to GitHub

1. Go to your GitHub repo
2. **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"** 4 times and add:

**Secret 1:**
- Name: `TWITTER_API_KEY`
- Value: (paste your API Key)

**Secret 2:**
- Name: `TWITTER_API_SECRET`
- Value: (paste your API Key Secret)

**Secret 3:**
- Name: `TWITTER_ACCESS_TOKEN`
- Value: (paste your Access Token)

**Secret 4:**
- Name: `TWITTER_ACCESS_SECRET`
- Value: (paste your Access Token Secret)

---

## ⚠️ Important Notes

### About X API Pricing

X (formerly Twitter) has different pricing tiers:

- **Free**: Can't upload videos
- **Basic ($100/month)**: Can upload videos ✅
- **Pro ($5,000/month)**: Higher limits

**You need at least Basic ($100/month) to upload videos!**

### App Permissions

Make sure your app has **"Read and Write"** permissions:
1. In X Developer Portal, go to your app
2. Click **"Settings"**
3. Under **"User authentication settings"**
4. Make sure **"Read and Write"** is selected

---

## Testing Your Credentials

Before adding to GitHub, test locally:

```bash
# Windows PowerShell
$env:TWITTER_API_KEY="your_api_key"
$env:TWITTER_API_SECRET="your_api_secret"
$env:TWITTER_ACCESS_TOKEN="your_access_token"
$env:TWITTER_ACCESS_SECRET="your_access_secret"

# Test upload
python upload_twitter.py
```

If it works, add the same values to GitHub Secrets!

---

## What the Script Does

The `upload_twitter.py` script will:
1. Use your 4 credentials to authenticate
2. Upload your video to X
3. Post a tweet with the video
4. Return the tweet URL

---

## Troubleshooting

**"Could not authenticate you"**
- Double-check all 4 credentials are correct
- Make sure you clicked "Reveal" to see the full keys
- No extra spaces when copying

**"Your client app is not configured"**
- Make sure app has "Read and Write" permissions
- Regenerate Access Token after changing permissions

**"This request requires a participating developer account"**
- You need to upgrade to Basic plan ($100/month)
- Free tier doesn't support video uploads

---

**You're all set!** Once you add these 4 secrets to GitHub, your videos will automatically post to X daily at 9 PM! 🚀
