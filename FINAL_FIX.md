# 🔧 FINAL FIX: Add Test User to OAuth Consent Screen

## 🎯 The Real Problem

You're getting `403 insufficientPermissions` because:

**Your Gmail account is NOT added as a Test User in the OAuth consent screen.**

Even though:
- ✅ YouTube Data API v3 is enabled
- ✅ OAuth client exists
- ✅ Credentials are valid

Google is blocking API access because your app is in "Testing" mode and your email isn't on the allowed test users list.

## ✅ How to Fix (2 minutes)

### Step 1: Go to OAuth Consent Screen
1. Open: https://console.cloud.google.com/
2. **Select project**: `youtube-automation-481003`
3. Click **☰ menu** → **APIs & Services** → **OAuth consent screen**

### Step 2: Add Test Users
1. Scroll down to **"Test users"** section
2. Click **"+ ADD USERS"**
3. Enter your Gmail address (the one with your YouTube channel)
4. Click **"Save"**

### Step 3: Regenerate Credentials
After adding yourself as a test user, run:

```bash
python get_youtube_token.py
```

This will re-authorize with the correct permissions.

### Step 4: Test the Credentials
```bash
python test_local_credentials.py
```

This should now show:
- ✅ Authentication successful
- ✅ Your YouTube channel info
- The 3 values to copy to GitHub Secrets

### Step 5: Update GitHub Secrets
1. Go to your GitHub repo
2. **Settings** → **Secrets and variables** → **Actions**
3. Update these 3 secrets:
   - `YT_CLIENT_ID`
   - `YT_CLIENT_SECRET`
   - `YT_REFRESH_TOKEN`

## 🎯 Why This Happens

When your OAuth consent screen is in "Testing" mode (not verified), Google only allows:
- Users explicitly added to the "Test users" list
- The developer account that created the project

If you try to authenticate with any other account, or if the test users list is empty, you get `403 insufficientPermissions`.

## 📋 Quick Checklist

- [ ] Go to Google Cloud Console
- [ ] Select project: `youtube-automation-481003`
- [ ] Go to: APIs & Services → OAuth consent screen
- [ ] Add your Gmail to "Test users"
- [ ] Run: `python get_youtube_token.py`
- [ ] Run: `python test_local_credentials.py` (should work now!)
- [ ] Copy the 3 values to GitHub Secrets

## 🚨 Alternative: Publish the App

If you don't want to manage test users, you can publish your OAuth consent screen:

1. Go to OAuth consent screen
2. Click **"PUBLISH APP"**
3. Confirm the warning (it's safe for personal use)

This removes the test user restriction, but you'll still see a warning when authorizing (which is fine).

## ✅ After This

Your YouTube upload automation will work perfectly!
