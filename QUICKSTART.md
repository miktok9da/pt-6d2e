# Quick Start - YouTube Upload Setup

## 🎯 You Have: Client ID + Client Secret

## 🎯 You Need: Refresh Token

## ⚡ 3-Step Process

### Step 1: Get Refresh Token (5 minutes)

```bash
# Make sure client_secrets.json is in this folder
python get_youtube_token.py
```

**What happens:**
1. Browser opens
2. Login to Google
3. **SELECT which YouTube channel** to upload to
4. Script prints your credentials

**Copy these 3 values:**
- `CLIENT_ID`
- `CLIENT_SECRET`  
- `REFRESH_TOKEN`

---

### Step 2: Add to GitHub Secrets

1. Go to your repo → **Settings** → **Secrets** → **Actions**
2. Click **"New repository secret"** 3 times:

| Secret Name | Value |
|-------------|-------|
| `YT_CLIENT_ID` | (paste CLIENT_ID) |
| `YT_CLIENT_SECRET` | (paste CLIENT_SECRET) |
| `YT_REFRESH_TOKEN` | (paste REFRESH_TOKEN) |

---

### Step 3: Push & Run

```bash
git add .
git commit -m "Add YouTube automation"
git push origin main
```

Then:
1. Go to **Actions** tab
2. Click **"Daily Auto Shorts with YouTube Upload"**
3. Click **"Run workflow"**
4. Wait 6-8 minutes
5. **Check your YouTube channel!** 🎉

---

## ✅ Verify Which Channel (Optional)

```bash
# Set these first:
export YT_CLIENT_ID="your_client_id"
export YT_CLIENT_SECRET="your_client_secret"
export YT_REFRESH_TOKEN="your_refresh_token"

# Then run:
python verify_channel.py
```

This shows exactly which channel the token uploads to.

---

## 🔄 Multiple Channels?

Run `get_youtube_token.py` multiple times:
- Each time SELECT a different channel
- Save each refresh token separately
- Add as `YT_REFRESH_TOKEN_MAIN`, `YT_REFRESH_TOKEN_SHORTS`, etc.

---

## 📝 Files You Need

| File | Status | Where to Get |
|------|--------|--------------|
| `client_secrets.json` | ✅ You have | Downloaded from Google Cloud |
| Refresh Token | ❌ Need to get | Run `get_youtube_token.py` |

---

## 🚨 Troubleshooting

**"client_secrets.json not found"**
- Download it from Google Cloud Console
- Rename to exactly `client_secrets.json`
- Put in the same folder as the scripts

**"No module named google_auth_oauthlib"**
```bash
pip install -r requirements.txt
```

**"Which channel will it upload to?"**
- The channel you SELECT during OAuth login
- Run `verify_channel.py` to confirm

---

## ⏱️ How Long Does It Take?

- **Get refresh token**: 2 minutes
- **Add GitHub secrets**: 1 minute
- **First workflow run**: 8-10 minutes (downloads models)
- **Subsequent runs**: 6-8 minutes (cached)

---

## 🎯 That's It!

Once set up, videos auto-upload daily at 6 AM UTC.

Change schedule in `.github/workflows/daily-shorts.yml`
