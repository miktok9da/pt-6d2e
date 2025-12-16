# 🐦 X (Twitter) - Which Key Goes Where?

## What You See on X Developer Portal → Where to Paste in GitHub

Looking at your X Developer Portal, here's the exact mapping:

---

## 1️⃣ Consumer Keys Section

### What You See:
```
Consumer Keys
API Key and Secret
[Reveal API Key]
```

### Click "Reveal API Key" and you'll see TWO things:

**First one (API Key):**
```
API Key: xxxxxxxxxxxxxxxxxxxxxxxxxxx
```
→ Copy this to GitHub Secret: **`TWITTER_API_KEY`**

**Second one (API Key Secret):**
```
API Key Secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
→ Copy this to GitHub Secret: **`TWITTER_API_SECRET`**

---

## 2️⃣ Access Token and Secret Section

### What You See:
```
Access Token and Secret
For @thriveruswave
[Generate]
```

### Click "Generate" and you'll see TWO things:

**First one (Access Token):**
```
Access Token: xxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
→ Copy this to GitHub Secret: **`TWITTER_ACCESS_TOKEN`**

**Second one (Access Token Secret):**
```
Access Token Secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
→ Copy this to GitHub Secret: **`TWITTER_ACCESS_SECRET`**

---

## 📋 Quick Reference Table

| What X Shows | GitHub Secret Name | Where to Find |
|--------------|-------------------|---------------|
| API Key | `TWITTER_API_KEY` | Consumer Keys → Reveal API Key (first one) |
| API Key Secret | `TWITTER_API_SECRET` | Consumer Keys → Reveal API Key (second one) |
| Access Token | `TWITTER_ACCESS_TOKEN` | Access Token → Generate (first one) |
| Access Token Secret | `TWITTER_ACCESS_SECRET` | Access Token → Generate (second one) |

---

## 🎯 Step-by-Step Instructions

### Step 1: Get Consumer Keys
1. On X Developer Portal, find **"Consumer Keys"** section
2. Click **"Reveal API Key"**
3. You'll see 2 values:
   - Copy the **API Key** (first one)
   - Copy the **API Key Secret** (second one)

### Step 2: Get Access Tokens
1. Scroll down to **"Access Token and Secret"** section
2. Click **"Generate"** button
3. You'll see 2 values:
   - Copy the **Access Token** (first one)
   - Copy the **Access Token Secret** (second one)

### Step 3: Add to GitHub
1. Go to your GitHub repo
2. **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"** and add each one:

**Secret #1:**
- Name: `TWITTER_API_KEY`
- Value: (paste the API Key from Step 1)

**Secret #2:**
- Name: `TWITTER_API_SECRET`
- Value: (paste the API Key Secret from Step 1)

**Secret #3:**
- Name: `TWITTER_ACCESS_TOKEN`
- Value: (paste the Access Token from Step 2)

**Secret #4:**
- Name: `TWITTER_ACCESS_SECRET`
- Value: (paste the Access Token Secret from Step 2)

---

## ⚠️ Important Notes

### Don't Use Bearer Token
You see a **"Bearer Token"** on the page - **IGNORE IT!** We don't need it for video uploads.

### The 4 Keys You Need:
✅ API Key (from Consumer Keys)  
✅ API Key Secret (from Consumer Keys)  
✅ Access Token (from Access Token section)  
✅ Access Token Secret (from Access Token section)  

❌ Bearer Token (NOT needed)

---

## 🔍 How to Tell Them Apart

**API Key:**
- Shorter
- Looks like: `xxxxxxxxxxxxxxxxxxxxxxxxxxx`

**API Key Secret:**
- Longer
- Looks like: `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

**Access Token:**
- Has a dash in the middle
- Looks like: `xxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

**Access Token Secret:**
- Similar length to API Key Secret
- Looks like: `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

---

## ✅ Checklist

Before you finish, make sure you have:

- [ ] Clicked "Reveal API Key" in Consumer Keys section
- [ ] Copied both API Key and API Key Secret
- [ ] Clicked "Generate" in Access Token section
- [ ] Copied both Access Token and Access Token Secret
- [ ] Added all 4 secrets to GitHub with correct names
- [ ] Double-checked no typos in secret names

---

**You're ready!** Once all 4 secrets are in GitHub, your videos will automatically post to X (Twitter) daily! 🚀
