# YouTube Shorts Automation Bot 🎬

Automatically generate and upload AI-powered YouTube Shorts daily using GitHub Actions.

## ✨ Features

- 🤖 **AI Story Generation** - Pollinations AI creates unique stories
- 🎨 **8 Unique Scene Images** - Flux model with unique seeds per scene
- 🎬 **Ken Burns Animation** - Smooth zoom effects on each image
- 🗣️ **Natural Voice Narration** - Edge-TTS (Microsoft Neural voices)
- 📝 **Word-Level Subtitles** - UPPERCASE, centered, synchronized (Whisper AI)
- 🎵 **Background Music** - Automatic mixing with narration
- 📤 **Auto YouTube Upload** - Direct upload to your channel
- ⚡ **Optimized Pipeline** - 6-8 minutes per video with caching

## 🎯 Quick Start

### 1. Clone & Install

```bash
git clone <your-repo>
cd Youtube\ automation
pip install -r requirements.txt
```

### 2. Add Your Music

```bash
# Copy your background music to:
audio/music.mp3
```

### 3. Test Locally

```bash
python main.py
# Video will be in: output/final_video.mp4
```

### 4. Setup YouTube Upload

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions.

**Quick version:**
1. Get YouTube API credentials from Google Cloud Console
2. Run `python upload_to_youtube.py` to authenticate
3. Run `python get_youtube_token.py` to get token JSON
4. Add `YOUTUBE_TOKEN` to GitHub Secrets
5. Push to GitHub and enable Actions

## 📊 Performance

| Metric | Value |
|--------|-------|
| Generation Time | 6-8 minutes |
| Video Quality | 1080x1920, CRF 18 (high) |
| File Size | 8-12 MB |
| Monthly GitHub Actions | ~300 min (free tier: 2,000) |
| Images per Video | 8 unique scenes |
| YouTube Uploads/Day | ~6 (quota limit) |

## 🎨 Quality Features

- **Enhanced Image Prompts**: Detailed, cinematic descriptions
- **High Bitrate Encoding**: CRF 18 for excellent quality
- **Smooth Animations**: Ken Burns zoom effects
- **Professional Subtitles**: Arial Black 100pt, bold, centered
- **Audio Mixing**: Balanced narration + background music

## 📁 Project Structure

```
├── main.py                  # Main video generation pipeline
├── upload_to_youtube.py     # YouTube upload script
├── get_youtube_token.py     # Helper to extract OAuth token
├── requirements.txt         # Python dependencies
├── topics.txt               # Story topics (one per line)
├── SETUP_GUIDE.md          # Detailed setup instructions
├── audio/
│   └── music.mp3           # Your background music
├── .github/workflows/
│   └── daily-shorts.yml    # GitHub Actions workflow
└── output/                 # Generated videos (auto-created)
```

## ⚙️ Configuration

### Change Number of Images

Edit `main.py`:
```python
NUM_IMAGES = 8  # 6-10 recommended (8 is optimal)
```

### Change Upload Schedule

Edit `.github/workflows/daily-shorts.yml`:
```yaml
schedule:
  - cron: "0 6 * * *"  # 6 AM UTC daily
```

### Add More Topics

Edit `topics.txt`:
```
your topic 1
your topic 2
your topic 3
```

## 🔧 Troubleshooting

### Video Quality Issues
- Increase CRF value in `main.py` (lower = better quality, 18-23 recommended)
- Check image generation - each should have unique file size

### Upload Failures
- Verify `YOUTUBE_TOKEN` secret is set correctly
- Check GitHub Actions logs for errors
- Ensure YouTube API quota not exceeded

### Slow Generation
- Reduce `NUM_IMAGES` to 6-7
- Images are the slowest part (~20-30 sec each)

## 📝 How It Works

1. **Story Generation**: AI creates 30-40 second story from topic
2. **Scene Extraction**: Splits story into 8 distinct scenes
3. **Image Generation**: Creates unique image per scene (with unique seed)
4. **TTS Narration**: Converts story to natural speech
5. **Subtitle Generation**: Whisper creates word-level timestamps
6. **Animation**: Ken Burns zoom effects on each image
7. **Composition**: Merges images, subtitles, narration, music
8. **Upload**: Automatically uploads to YouTube as Short

## 🎯 Next Steps

1. ✅ Test video generation locally
2. ✅ Set up YouTube API credentials
3. ✅ Configure GitHub Secrets
4. ✅ Push to GitHub
5. ✅ Enable daily workflow
6. ✅ Monitor your channel growth!

## 📄 License

MIT License - Feel free to modify and use!

## 🙏 Credits

- **Pollinations AI** - Story & image generation
- **Whisper** - Subtitle generation
- **Edge-TTS** - Voice narration
- **FFmpeg** - Video processing
