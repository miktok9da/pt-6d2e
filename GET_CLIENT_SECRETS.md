# How to Get client_secrets.json

## 🎯 What You Need

`client_secrets.json` from Google Cloud Console

## 📋 Step-by-Step Guide

### 1. Go to Google Cloud Console

Open: [console.cloud.google.com](https://console.cloud.google.com/)

### 2. Create a Project (or Select Existing)

- Click project dropdown at top
- Click "New Project"
- Name: "YouTube Automation" (or any name)
- Click "Create"
- Wait for project to be created
- **Select the project** from dropdown

### 3. Enable YouTube Data API v3

- Click "☰" menu → "APIs & Services" → "Library"
- Search: "YouTube Data API v3"
- Click on it
- Click "Enable"
- Wait for it to enable

### 4. Configure OAuth Consent Screen

- Click "☰" menu → "APIs & Services" → "OAuth consent screen"
- Select: **External** (unless you have Google Workspace)
- Click "Create"

**Fill in:**
- App name: "YouTube Shorts Bot"
- User support email: Your email
- Developer contact: Your email
- Click "Save and Continue"

**Scopes:**
- Click "Save and Continue" (skip this - scopes are requested automatically)

**Test users:**
- Click "+ Add Users"
- Add your Gmail (the one with YouTube channel)
- Click "Save and Continue"

- Click "Back to Dashboard"

### 5. Create OAuth Client ID

- Click "☰" menu → "APIs & Services" → "Credentials"
- Click "+ Create Credentials" → "OAuth client ID"

**Select:**
- Application type: **Desktop app**
- Name: "YouTube Automation Desktop"
- Click "Create"

### 6. Download JSON

- A popup appears with Client ID and Secret
- Click "Download JSON"
- **Save the file**
- **Rename it to:** `client_secrets.json`
- **Move it to your project folder**

## ✅ You Should Have

A file named `client_secrets.json` that looks like:

```json
{
  "installed": {
    "client_id": "123456789-abcdefg.apps.googleusercontent.com",
    "project_id": "your-project",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "GOCSPX-xxxxxxxxxxxxx",
    "redirect_uris": ["http://localhost"]
  }
}
```

## 🚀 Next Step

Now run:
```bash
python get_youtube_token.py
```

This will:
1. Open your browser
2. Ask you to login to Google
3. **SELECT which YouTube channel** to use
4. Generate refresh token
5. Print 3 values to copy

## ⚠️ Important

- **Keep `client_secrets.json` private** - never share or upload to GitHub
- The `.gitignore` file already blocks it from being uploaded
- You only need to do this once per YouTube channel

## 🔧 Troubleshooting

**"API not enabled"**
- Make sure you enabled "YouTube Data API v3" in step 3

**"OAuth consent screen not configured"**
- Complete step 4 first

**"Redirect URI mismatch"**
- Make sure you selected "Desktop app" not "Web app"

**"Access blocked"**
- Add your email as test user in OAuth consent screen
- Make sure you're using the same Google account

## 📝 Summary

1. ✅ Create Google Cloud project
2. ✅ Enable YouTube Data API v3
3. ✅ Configure OAuth consent screen
4. ✅ Create Desktop app credentials
5. ✅ Download JSON as `client_secrets.json`
6. ✅ Run `get_youtube_token.py`
