# 🚀 Quick Start: What You Need for Each Platform

Simple guide showing exactly what credentials you need and where to get them.

---

## 📺 YouTube (✅ Already Done!)

**What You Need:**
- ✅ `YT_CLIENT_ID` - Already in GitHub Secrets
- ✅ `YT_CLIENT_SECRET` - Already in GitHub Secrets  
- ✅ `YT_REFRESH_TOKEN` - Already in GitHub Secrets

**Status:** Working! Nothing to do.

---

## 📸 Instagram Reels

**What You Need:**
- `IG_ACCESS_TOKEN` - A long text code from Facebook
- `IG_USER_ID` - Your Instagram Business account number

**Where to Get Them:**

### Step 1: Make Instagram a Business Account
1. Open Instagram app on your phone
2. Go to **Settings** → **Account**
3. Tap **Switch to Professional Account**
4. Choose **Business** (not Creator)

### Step 2: Create Facebook Page
1. Go to https://www.facebook.com/pages/create
2. Create any page (choose any category)
3. Link it to your Instagram

### Step 3: Get the Codes
1. Go to https://developers.facebook.com/tools/explorer
2. Click **"Get Token"** → **"Get User Access Token"**
3. Select these permissions:
   - `instagram_basic`
   - `instagram_content_publish`
   - `pages_read_engagement`
4. Copy the long code that appears = `IG_ACCESS_TOKEN`
5. In the same page, type: `me/accounts` and click Submit
6. Find your Instagram ID in the response = `IG_USER_ID`

### Step 4: Add to GitHub
1. Go to your GitHub repo → **Settings** → **Secrets** → **Actions**
2. Click **"New repository secret"**
3. Name: `IG_ACCESS_TOKEN`, Value: (paste the long code)
4. Click **"New repository secret"** again
5. Name: `IG_USER_ID`, Value: (paste your Instagram ID)

**Done!** ✅

---

## 🧵 Threads

**What You Need:**
- `THREADS_ACCESS_TOKEN` - Same as Instagram!
- `THREADS_USER_ID` - Same as Instagram!

**Where to Get Them:**

Use the **exact same codes** from Instagram above!

### Add to GitHub:
1. Go to GitHub → **Settings** → **Secrets** → **Actions**
2. Name: `THREADS_ACCESS_TOKEN`, Value: (same as `IG_ACCESS_TOKEN`)
3. Name: `THREADS_USER_ID`, Value: (same as `IG_USER_ID`)

**Done!** ✅

---

## 📘 Facebook Reels

**What You Need:**
- `FB_ACCESS_TOKEN` - A long text code from Facebook
- `FB_PAGE_ID` - Your Facebook Page number

**Where to Get Them:**

### Step 1: Create Facebook Page (if you don't have one)
1. Go to https://www.facebook.com/pages/create
2. Create a page (any category)

### Step 2: Get Page ID
1. Go to your Facebook Page
2. Click **"About"** on the left
3. Scroll down - you'll see **"Page ID"** with a number
4. Copy that number = `FB_PAGE_ID`

### Step 3: Get Access Token
1. Go to https://developers.facebook.com/tools/explorer
2. Click **"Get Token"** → **"Get Page Access Token"**
3. Select your page
4. Select these permissions:
   - `pages_manage_posts`
   - `pages_read_engagement`
5. Copy the long code = `FB_ACCESS_TOKEN`

### Step 4: Add to GitHub
1. Go to GitHub → **Settings** → **Secrets** → **Actions**
2. Name: `FB_ACCESS_TOKEN`, Value: (paste the code)
3. Name: `FB_PAGE_ID`, Value: (paste the page number)

**Done!** ✅

---

## 🎵 TikTok

**What You Need:**
- `TIKTOK_ACCESS_TOKEN` - A code from TikTok

**Where to Get It:**

### Step 1: Apply for TikTok Developer Account
1. Go to https://developers.tiktok.com/
2. Click **"Register"**
3. Sign in with your TikTok account
4. Fill out the application

### Step 2: Create App
1. After approval (takes 1-2 weeks), go to Dashboard
2. Click **"Create App"**
3. Add **"Content Posting API"**
4. Submit for review (another 1-2 weeks)

### Step 3: Get Token
1. After approval, go to your app
2. Follow TikTok's OAuth flow to get access token
3. Copy the token = `TIKTOK_ACCESS_TOKEN`

### Step 4: Add to GitHub
1. Go to GitHub → **Settings** → **Secrets** → **Actions**
2. Name: `TIKTOK_ACCESS_TOKEN`, Value: (paste the token)

**Note:** TikTok takes 2-4 weeks total (waiting for approvals)

---

## 🐦 X (formerly Twitter)

**What You Need:**
- `TWITTER_API_KEY` - From X Developer Portal
- `TWITTER_API_SECRET` - From X Developer Portal
- `TWITTER_ACCESS_TOKEN` - From X Developer Portal
- `TWITTER_ACCESS_SECRET` - From X Developer Portal

**⚠️ IMPORTANT:** X charges **$100/month** for video uploads!

**Where to Get Them:**

### Step 1: Get X Developer Account
1. Go to https://developer.twitter.com/
2. Click **"Sign up"**
3. Apply for developer account
4. **Upgrade to "Basic" plan ($100/month)** - Required for video!

### Step 2: Create App
1. Go to Developer Portal
2. Click **"Create Project"** → **"Create App"**
3. Give it a name

### Step 3: Get API Keys
1. In your app, go to **"Keys and tokens"**
2. You'll see:
   - **API Key** = `TWITTER_API_KEY`
   - **API Secret Key** = `TWITTER_API_SECRET`
3. Click **"Generate"** under Access Token
4. You'll get:
   - **Access Token** = `TWITTER_ACCESS_TOKEN`
   - **Access Token Secret** = `TWITTER_ACCESS_SECRET`

### Step 4: Add to GitHub
1. Go to GitHub → **Settings** → **Secrets** → **Actions**
2. Add all 4 secrets:
   - `TWITTER_API_KEY`
   - `TWITTER_API_SECRET`
   - `TWITTER_ACCESS_TOKEN`
   - `TWITTER_ACCESS_SECRET`

**Note:** Only do this if you're willing to pay $100/month!

---

## 📊 Quick Summary

| Platform | What You Need | Cost | Time to Setup |
|----------|---------------|------|---------------|
| YouTube | ✅ Already done! | Free | 0 min |
| Instagram | 2 codes | Free | 30 min |
| Threads | Same as Instagram | Free | 5 min |
| Facebook | 2 codes | Free | 20 min |
| TikTok | 1 code | Free | 2-4 weeks (approval) |
| X (Twitter) | 4 codes | $100/month | 15 min |

---

## 🎯 Recommended Order

**Start Here (Free & Easy):**
1. ✅ YouTube - Already working!
2. 📸 Instagram - 30 minutes
3. 🧵 Threads - 5 minutes (uses Instagram codes)
4. 📘 Facebook - 20 minutes

**Skip These:**
- ⏭️ TikTok - Takes 2-4 weeks (approval process)
- ⏭️ X - Costs $100/month

---

## ❓ Common Questions

**Q: Do I need all platforms?**
A: No! Start with Instagram and Facebook (free and easy).

**Q: What if I don't have a Facebook Page?**
A: Create one in 2 minutes at facebook.com/pages/create

**Q: Why does X cost money?**
A: X (Twitter) charges for API access. Video uploads require the $100/month plan.

**Q: How long do tokens last?**
A: Usually 60 days. You'll need to regenerate them when they expire.

**Q: Can I test before adding to GitHub?**
A: Yes! Set the codes as environment variables and run `python upload_all_platforms.py`

---

## 🆘 Need Help?

**Can't find something?**
- Instagram/Facebook: All done at https://developers.facebook.com/tools/explorer
- TikTok: https://developers.tiktok.com/
- X: https://developer.twitter.com/

**Tokens expired?**
- Just go back to the same page and generate new ones
- Update GitHub Secrets with new values

---

**You're ready!** Start with Instagram + Threads (easiest), then add Facebook. Your videos will automatically post to all platforms daily at 9 PM! 🚀
