# YouTube Shorts Automation Bot - Setup Guide

## 🎯 Quick Start

### 1. Get YouTube API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable **YouTube Data API v3**:
   - Go to "APIs & Services" → "Library"
   - Search for "YouTube Data API v3"
   - Click "Enable"
4. Create OAuth 2.0 credentials:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Application type: "Desktop app"
   - Name it: "YouTube Shorts Bot"
   - Download the JSON file

### 2. Local Setup (First Time)

```bash
# Install dependencies
pip install -r requirements.txt

# Copy your downloaded OAuth file
# Rename it to: client_secrets.json

# Run authentication (opens browser)
python upload_to_youtube.py
```

This will:
- Open your browser for Google login
- Ask for YouTube upload permission
- Save `token.pickle` for future use

### 3. GitHub Setup

#### Add Secrets:
1. Go to your GitHub repo → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add `YOUTUBE_TOKEN`:
   - Name: `YOUTUBE_TOKEN`
   - Value: Copy content from `token.pickle` (convert to JSON):

```python
# Run this to get your token as JSON:
import pickle
import json

with open('token.pickle', 'rb') as f:
    creds = pickle.load(f)
    
token_data = {
    'token': creds.token,
    'refresh_token': creds.refresh_token,
    'token_uri': creds.token_uri,
    'client_id': creds.client_id,
    'client_secret': creds.client_secret,
    'scopes': creds.scopes
}

print(json.dumps(token_data))
```

Copy the output and paste as the secret value.

#### Push to GitHub:
```bash
git add .
git commit -m "Add YouTube automation bot"
git push origin main
```

### 4. Test the Workflow

1. Go to Actions tab in GitHub
2. Click "Daily Auto Shorts with YouTube Upload"
3. Click "Run workflow"
4. Wait ~6-8 minutes
5. Check your YouTube channel!

## ⚙️ Configuration

### Change Upload Schedule

Edit `.github/workflows/daily-shorts.yml`:
```yaml
schedule:
  - cron: "0 6 * * *"  # 6 AM UTC daily
  # Change to your preferred time
```

### Customize Video Settings

Edit `main.py`:
```python
NUM_IMAGES = 8  # Number of scenes (6-10 recommended)
IMAGE_MODEL = "flux"  # AI model for images
```

### Privacy Settings

Edit `upload_to_youtube.py`:
```python
'privacyStatus': 'public'  # or 'private', 'unlisted'
```

## 📊 Performance

- **Generation time**: ~6-8 minutes
- **Monthly usage**: ~300 minutes (well within 2,000 free limit)
- **Video quality**: 1080x1920, CRF 18 (high quality)
- **File size**: ~8-12 MB per video

## 🎨 Quality Improvements

The bot includes:
- ✅ High-quality image prompts (detailed, cinematic)
- ✅ Ken Burns animation (zoom effects)
- ✅ CRF 18 encoding (high quality)
- ✅ UPPERCASE subtitles (Arial Black, 100pt)
- ✅ Background music mixing
- ✅ Word-level synchronized subtitles

## 🔧 Troubleshooting

### "Invalid credentials" error
- Re-run authentication locally
- Update `YOUTUBE_TOKEN` secret

### "Quota exceeded" error
- YouTube API has daily quotas
- Default quota: 10,000 units/day
- Each upload: ~1,600 units
- Max ~6 uploads/day

### Video not uploading
- Check GitHub Actions logs
- Verify `YOUTUBE_TOKEN` secret is set
- Ensure video file exists in `output/`

## 📝 Adding More Topics

Edit `topics.txt`:
```
your new topic 1
your new topic 2
your new topic 3
```

The bot cycles through topics daily.

## 🎯 Next Steps

1. ✅ Test locally first
2. ✅ Set up GitHub secrets
3. ✅ Run workflow manually to test
4. ✅ Enable daily schedule
5. ✅ Monitor your YouTube channel!
