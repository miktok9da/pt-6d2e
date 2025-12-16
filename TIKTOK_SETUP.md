# 🎵 TikTok Setup Guide - Complete Walkthrough

## Overview

TikTok requires **developer approval** before you can upload videos via API. This process takes **2-4 weeks** total.

---

## ⚠️ Important: TikTok Requires Approval

Unlike Instagram or Facebook, TikTok has a strict approval process:
- ✅ Free to use (no monthly fees)
- ❌ Requires app approval (1-2 weeks)
- ❌ Requires API access approval (another 1-2 weeks)
- 📝 Need to explain your use case

---

## 🎯 What You Need for TikTok

Only **1 credential** is needed:
- `TIKTOK_ACCESS_TOKEN` - Your access token from TikTok

(Optional: `TIKTOK_CLIENT_KEY` and `TIKTOK_CLIENT_SECRET` - but not required for basic uploads)

---

## 📋 Step-by-Step Setup

### Step 1: Create TikTok Developer Account

1. **Go to TikTok for Developers:**
   - Visit: https://developers.tiktok.com/

2. **Sign Up:**
   - Click **"Register"** or **"Get Started"**
   - Sign in with your TikTok account (@thriveruswave)

3. **Complete Registration:**
   - Fill in your details
   - Verify your email
   - Accept terms and conditions

---

### Step 2: Create an App

1. **Go to Developer Portal:**
   - After registration, go to: https://developers.tiktok.com/apps

2. **Click "Create an App":**
   - App Name: `YouTube Automation Bot` (or any name)
   - App Description: `Automated content posting for educational videos about ancient women's history`

3. **Select Use Case:**
   - Choose: **"Content Posting"**
   - Or: **"Video Publishing"**

4. **Fill in App Details:**
   - **App Icon**: Upload any icon (can be simple)
   - **Category**: Education or Entertainment
   - **Website**: Your GitHub repo URL or any website
   - **Privacy Policy URL**: Can use a simple one or GitHub repo

5. **Submit for Review:**
   - Click **"Submit"**
   - Wait **1-2 weeks** for approval

---

### Step 3: Request Content Posting API Access

After your app is approved:

1. **Go to Your App Dashboard:**
   - Find your approved app
   - Click on it

2. **Add Products:**
   - Look for **"Products"** or **"Add Products"**
   - Find **"Content Posting API"** or **"Login Kit"**
   - Click **"Add"**

3. **Request Access:**
   - Fill out the form explaining your use case:
     ```
     I'm creating educational content about ancient women's history.
     I want to automatically post daily short videos (30-60 seconds)
     to share historical facts and stories.
     ```

4. **Submit Request:**
   - Wait another **1-2 weeks** for approval

---

### Step 4: Get Access Token (After Approval)

Once both approvals are granted:

1. **Go to App Dashboard:**
   - Click on your app

2. **Find OAuth/Authentication Section:**
   - Look for **"OAuth"** or **"Authentication"**

3. **Get Client Key and Secret:**
   - You'll see:
     - **Client Key** (also called App ID)
     - **Client Secret**
   - Copy these (optional, but good to save)

4. **Generate Access Token:**
   
   **Option A: Use TikTok's OAuth Flow**
   - TikTok will provide an OAuth URL
   - Visit the URL and authorize your account
   - You'll get an access token
   
   **Option B: Use Test Token (for development)**
   - Some apps provide a test token
   - Look for "Test Token" or "Developer Token"
   - This works for testing but may expire quickly

5. **Copy the Access Token:**
   - It looks like: `act.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - This is your `TIKTOK_ACCESS_TOKEN`

---

### Step 5: Add to GitHub Secrets

1. **Go to GitHub:**
   - Your repo → **Settings** → **Secrets** → **Actions**

2. **Add Secret:**
   - Click **"New repository secret"**
   - Name: `TIKTOK_ACCESS_TOKEN`
   - Value: (paste your access token)

3. **Optional - Add Client Credentials:**
   - Name: `TIKTOK_CLIENT_KEY`, Value: (your client key)
   - Name: `TIKTOK_CLIENT_SECRET`, Value: (your client secret)

---

## 🎯 Quick Summary

| What You Need | Where to Get It | GitHub Secret Name |
|---------------|-----------------|-------------------|
| Access Token | TikTok Developer Portal → OAuth | `TIKTOK_ACCESS_TOKEN` |
| Client Key (optional) | App Dashboard → Credentials | `TIKTOK_CLIENT_KEY` |
| Client Secret (optional) | App Dashboard → Credentials | `TIKTOK_CLIENT_SECRET` |

---

## ⏱️ Timeline

- **Day 1**: Register developer account ✅
- **Day 1**: Create app and submit for review 📝
- **Week 1-2**: Wait for app approval ⏳
- **Week 2**: Request Content Posting API access 📝
- **Week 3-4**: Wait for API approval ⏳
- **Week 4**: Get access token and start posting! 🎉

**Total Time: 2-4 weeks**

---

## 💡 Tips for Faster Approval

1. **Clear Use Case:**
   - Explain you're posting educational content
   - Mention it's automated but original content

2. **Professional App:**
   - Use a proper app name and icon
   - Provide a real website/privacy policy

3. **Follow Guidelines:**
   - Read TikTok's developer guidelines
   - Make sure your content complies with their policies

4. **Be Patient:**
   - TikTok reviews manually
   - Don't spam them with multiple applications

---

## 🔧 Testing Your Setup

Once you have the access token:

```bash
# Windows PowerShell
$env:TIKTOK_ACCESS_TOKEN="your_access_token"

# Test upload
python upload_tiktok.py
```

If it works, add the token to GitHub Secrets!

---

## ❓ Common Issues

### "App not approved yet"
- **Solution**: Wait for TikTok's email confirmation
- Check spam folder for approval emails

### "Content Posting API not available"
- **Solution**: Make sure you requested this specific API
- Some apps only get Login Kit by default

### "Access token expired"
- **Solution**: Tokens expire! Generate a new one
- Long-lived tokens last 1-2 months

### "Invalid credentials"
- **Solution**: Double-check you copied the full token
- Make sure no extra spaces

---

## 📞 TikTok Support

- **Developer Portal**: https://developers.tiktok.com/
- **Documentation**: https://developers.tiktok.com/doc/content-posting-api-get-started
- **Support**: Use the "Contact Us" form in developer portal

---

## 🎯 Alternative: Skip TikTok for Now

**Recommendation**: Start with easier platforms first!

✅ **Easy & Free (No Approval):**
- Instagram Reels (30 min setup)
- Facebook Reels (20 min setup)
- Threads (5 min setup)

⏳ **Takes Time:**
- TikTok (2-4 weeks approval)

💰 **Costs Money:**
- X/Twitter ($100/month)

**You can add TikTok later** once you get approval!

---

**Bottom Line**: TikTok is free but requires patience. Apply now and use other platforms while you wait for approval! 🚀
