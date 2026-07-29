import os
import re
import datetime
import subprocess
import random
from pathlib import Path
from urllib.parse import quote
import requests
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ---------------- CONFIG ----------------

NUM_IMAGES = 8  # 8 unique scenes (faster generation)
IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 1920
IMAGE_MODEL = "flux"

STORY_MAX_WORDS = 130

TOPICS_FILE = "topics.txt"

IMAGES_DIR = Path("images")
OUTPUT_DIR = Path("output")
AUDIO_DIR = Path("audio")

MUSIC_FILE = AUDIO_DIR / "music.mp3"

NARRATION_FILE = OUTPUT_DIR / "narration.mp3"
STORY_FILE = OUTPUT_DIR / "story.txt"
SCENES_FILE = OUTPUT_DIR / "scenes.txt"
SUBS_FILE = OUTPUT_DIR / "subtitles.ass"
ANIMATED_VIDEO = OUTPUT_DIR / "animated.mp4"
VIDEO_WITH_SUBS = OUTPUT_DIR / "video_with_subs.mp4"
FINAL_VIDEO = OUTPUT_DIR / "final_video.mp4"

WHISPER_MODEL_NAME = "small"

# ----------------------------------------

def ensure_dirs():
    IMAGES_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)
    AUDIO_DIR.mkdir(exist_ok=True)
    # Clean old images
    for f in IMAGES_DIR.glob("*.jpg"):
        f.unlink()

def choose_topic_for_today():
    with open(TOPICS_FILE, "r", encoding="utf-8") as f:
        topics = [line.strip() for line in f if line.strip()]
    today = datetime.date.today()
    return topics[today.toordinal() % len(topics)]

def generate_story_with_pollinations(topic: str) -> str:
    """Generate a short Portuguese story about ancient women's history using paid Pollinations API."""
    api_key = os.getenv("POLLINATIONS_API_KEY")
    if not api_key:
        raise ValueError("POLLINATIONS_API_KEY environment variable is required for paid API")

    system = (
        "Você é um historiador especializado na história das mulheres nas civilizações antigas. "
        "Escreva uma história curta e interessante de 30 segundos (80-130 palavras) em português. "
        "Conte fatos históricos reais, leis, costumes ou tradições. "
        "Use um estilo vivo e cativante. Sem títulos."
    )
    prompt = f"Assunto: {topic}. Conte um fato histórico interessante."

    print(f"[story] Generating Portuguese story for topic: {topic}")
    
    payload = {
        "model": "openai",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        "temperature": 1.0,
        "jsonMode": False
    }
    
    url = "https://gen.pollinations.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}"}
    r = requests.post(url, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    text = r.json()['choices'][0]['message']['content'].strip()

    words = text.split()
    if len(words) > STORY_MAX_WORDS:
        text = " ".join(words[:STORY_MAX_WORDS])

    with open(STORY_FILE, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"[story] Portuguese story generated ({len(text.split())} words)")
    return text

def generate_scene_descriptions(story: str) -> list:
    """Extract distinct scene descriptions from the story sentences."""
    print(f"[scenes] Extracting {NUM_IMAGES} unique scene descriptions...")
    
    # Split story into sentences
    sentences = re.split(r'[.!?]+\s*', story.strip())
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
    
    # Create unique scenes from sentences
    scenes = []
    for i in range(NUM_IMAGES):
        if i < len(sentences):
            scene = sentences[i]
        else:
            # Cycle through sentences if we need more
            scene = sentences[i % len(sentences)]
        
        # Make each scene description more visual
        if i not in [j % len(sentences) for j in range(len(scenes))]:
            scenes.append(scene)
        else:
            # Add variation for repeated scenes
            variations = ["close-up view of", "wide shot of", "dramatic scene of", "peaceful moment of"]
            scenes.append(f"{variations[i % len(variations)]} {scene}")
    
    # Ensure uniqueness by adding index
    unique_scenes = []
    for i, scene in enumerate(scenes[:NUM_IMAGES]):
        unique_scenes.append(f"{scene}")
    
    # Save scenes
    with open(SCENES_FILE, "w", encoding="utf-8") as f:
        for i, scene in enumerate(unique_scenes):
            f.write(f"{i+1}. {scene}\n")
    
    print(f"[scenes] Created {len(unique_scenes)} unique scenes")
    return unique_scenes

def download_image_from_drive(idx: int) -> Path:
    import json
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    out = IMAGES_DIR / f"scene_{idx:02d}.jpg"
    service_key = os.environ.get("GOOGLE_SERVICE_ACCOUNT_KEY")
    folder_id = os.environ.get("GOOGLE_DRIVE_FOLDER_ID")
    if not folder_id: raise ValueError("GOOGLE_DRIVE_FOLDER_ID required")
    cred = service_account.Credentials.from_service_account_info(json.loads(service_key), scopes=["https://www.googleapis.com/auth/drive.readonly"])
    service = build("drive", "v3", credentials=cred)
    all_files = []; page_token = None
    while True:
        r = service.files().list(q=f"'{folder_id}' in parents and mimeType contains 'image/'", fields="files(id, name)", pageSize=200, pageToken=page_token).execute()
        all_files.extend(r.get("files", [])); page_token = r.get("nextPageToken")
        if not page_token: break
    used_log = Path("used_images.json"); usage = {}
    if used_log.exists(): usage = json.loads(used_log.read_text())
    for f in all_files:
        if f["name"] not in usage: usage[f["name"]] = 0
    min_u = min(usage.values())
    weights = [1.0 / (usage[f["name"]] - min_u + 1) for f in all_files]
    chosen = random.choices(all_files, weights=weights, k=1)[0]
    usage[chosen["name"]] += 1
    used_log.write_text(json.dumps(usage, indent=2))
    print(f"[image] Downloading {chosen['name']} from Drive...", flush=True)
    request = service.files().get_media(fileId=chosen["id"])
    from googleapiclient.http import MediaIoBaseDownload
    import io; fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request); done = False
    while not done: _, done = downloader.next_chunk()
    fh.seek(0); out.write_bytes(fh.read())
    print(f"  Saved: {out.name} ({out.stat().st_size // 1024} KB)", flush=True)
    return out


def generate_image(scene: str, idx: int) -> Path:
    return download_image_from_drive(idx)


def generate_images(scenes: list):
    """Generate unique images for each scene SEQUENTIALLY (avoids rate limits)"""
    print(f"[image] Generating {NUM_IMAGES} images sequentially (avoiding rate limits)...")
    return [generate_image(scene, i) for i, scene in enumerate(scenes)]

def generate_tts(story: str):
    """Generate narration using edge-tts (free Microsoft TTS)."""
    import asyncio
    try:
        import edge_tts
    except ImportError:
        subprocess.run(["pip", "install", "edge-tts"], check=True)
        import edge_tts
    
    print("[tts] Generating Portuguese narration with edge-tts...")
    
    VOICE = "pt-BR-AntonioNeural"  # Brazilian Portuguese male voice (or use "pt-BR-FranciscaNeural" for female)
    
    async def generate():
        communicate = edge_tts.Communicate(story, VOICE)
        await communicate.save(str(NARRATION_FILE))
    
    asyncio.run(generate())
    print(f"[tts] Narration saved to {NARRATION_FILE}")

def generate_word_subtitles():
    """Generate WORD-BY-WORD subtitles using Vosk (lightweight!)."""
    print("[subs] Generating word-level Portuguese subtitles with Vosk...")
    
    import json
    import wave
    from vosk import Model, KaldiRecognizer
    import os
    
    # Download Vosk model if not exists
    model_path = "vosk-model-small-pt-0.3"
    if not os.path.exists(model_path):
        print("[subs] Downloading Vosk Portuguese model (~31 MB)...")
        import urllib.request
        import zipfile
        
        url = "https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip"
        zip_path = "vosk-model.zip"
        
        urllib.request.urlretrieve(url, zip_path)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(".")
        
        os.remove(zip_path)
        print("[subs] Model downloaded!")
    
    # Convert MP3 to WAV for Vosk
    wav_file = "output/narration.wav"
    os.system(f'ffmpeg -y -i {NARRATION_FILE} -ar 16000 -ac 1 {wav_file}')
    
    # Load Vosk model
    model = Model(model_path)
    
    # Open WAV file
    wf = wave.open(wav_file, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)  # Enable word-level timestamps
    
    # Process audio
    words = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            if 'result' in result:
                for word_info in result['result']:
                    words.append({
                        'word': word_info['word'].upper(),
                        'start': word_info['start'],
                        'end': word_info['end']
                    })
    
    # Final result
    final_result = json.loads(rec.FinalResult())
    if 'result' in final_result:
        for word_info in final_result['result']:
            words.append({
                'word': word_info['word'].upper(),
                'start': word_info['start'],
                'end': word_info['end']
            })
    
    # Create ASS subtitle file
    ass_content = """[Script Info]
Title: História Portuguesa
ScriptType: v4.00+

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial Black,16,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,2,1,5,10,10,50,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    
    for word in words:
        start = word['start']
        end = word['end']
        text = word['word']
        
        start_time = f"{int(start//3600)}:{int((start%3600)//60):02d}:{start%60:.2f}"
        end_time = f"{int(end//3600)}:{int((end%3600)//60):02d}:{end%60:.2f}"
        
        ass_content += f"Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{text}\n"
    
    # Save ASS file
    with open(SUBS_FILE, "w", encoding="utf-8") as f:
        f.write(ass_content)
    
    print(f"[subs] WORD-BY-WORD subtitles saved ({len(words)} words)")

def get_audio_duration(audio_file):
    """Get duration of audio file using ffprobe."""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(audio_file)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip())

def create_animated_slideshow(image_paths):
    """Create animated slideshow with Ken Burns zoom effect."""
    print("[video] Creating animated slideshow with Ken Burns effect...")
    
    # Get audio duration to match video length
    duration = get_audio_duration(NARRATION_FILE)
    per_image = duration / len(image_paths)
    
    # Create individual animated clips with zoom effect
    clips = []
    for i, img_path in enumerate(image_paths):
        clip_file = OUTPUT_DIR / f"clip_{i:02d}.mp4"
        clips.append(clip_file)
        
        # Calculate frames (30 fps)
        frames = max(int(per_image * 30), 60)
        
        # Alternate between zoom in and zoom out for variety
        if i % 2 == 0:
            # Zoom in effect
            zoom_start = 1.0
            zoom_end = 1.3
        else:
            # Zoom out effect  
            zoom_start = 1.3
            zoom_end = 1.0
        
        # Simple zoom with scale filter (more reliable on Windows)
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", str(img_path),
            "-vf", (
                f"scale=8000:-1,"
                f"zoompan=z='if(lte(on,1),{zoom_start},{zoom_start}+(({zoom_end}-{zoom_start})/{frames})*on)':"
                f"d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={IMAGE_WIDTH}x{IMAGE_HEIGHT}:fps=30"
            ),
            "-t", str(per_image),
            "-c:v", "libx264",
            "-preset", "slow",  # Better quality
            "-crf", "18",  # High quality (lower = better, 18-23 is good)
            "-pix_fmt", "yuv420p",
            str(clip_file)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[video] Zoom failed for clip {i+1}, using fallback...")
            # Fallback: simple static with slight movement
            cmd_fallback = [
                "ffmpeg", "-y",
                "-loop", "1",
                "-i", str(img_path),
                "-vf", f"scale={IMAGE_WIDTH}:{IMAGE_HEIGHT}:force_original_aspect_ratio=increase,crop={IMAGE_WIDTH}:{IMAGE_HEIGHT},fps=30",
                "-t", str(per_image),
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                str(clip_file)
            ]
            subprocess.run(cmd_fallback, check=True, capture_output=True)
        
        print(f"[video] Animated clip {i+1}/{len(image_paths)}")
    
    # Create concat list
    concat_file = OUTPUT_DIR / "concat.txt"
    with open(concat_file, "w") as f:
        for clip in clips:
            f.write(f"file '{clip.resolve()}'\n")
    
    # Concatenate all clips
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-c", "copy",
        str(ANIMATED_VIDEO)
    ]
    subprocess.run(cmd, check=True)
    print(f"[video] Animated slideshow saved to {ANIMATED_VIDEO}")
    
    # Cleanup individual clips
    for clip in clips:
        if clip.exists():
            clip.unlink()

def add_subtitles():
    """Overlay ASS subtitles on video."""
    print("[video] Adding UPPERCASE subtitles...")
    
    # Windows path needs special handling for FFmpeg filter
    subs_path = str(SUBS_FILE.resolve()).replace("\\", "/").replace(":", "\\:")
    
    cmd = [
        "ffmpeg", "-y",
        "-i", str(ANIMATED_VIDEO),
        "-vf", f"ass='{subs_path}'",
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        str(VIDEO_WITH_SUBS)
    ]
    subprocess.run(cmd, check=True)
    print(f"[video] Video with subtitles saved to {VIDEO_WITH_SUBS}")

def merge_audio():
    """Merge video with narration and background music."""
    print("[merge] Merging audio with background music...")
    
    if MUSIC_FILE.exists():
        # Merge narration + background music (music at lower volume)
        cmd = [
            "ffmpeg", "-y",
            "-i", str(VIDEO_WITH_SUBS),
            "-i", str(NARRATION_FILE),
            "-i", str(MUSIC_FILE),
            "-filter_complex", "[2:a]volume=0.25[bg];[1:a][bg]amix=inputs=2:duration=first[a]",
            "-map", "0:v",
            "-map", "[a]",
            "-shortest",
            "-c:v", "copy",
            str(FINAL_VIDEO)
        ]
    else:
        print("[merge] No music.mp3 found, using narration only")
        cmd = [
            "ffmpeg", "-y",
            "-i", str(VIDEO_WITH_SUBS),
            "-i", str(NARRATION_FILE),
            "-map", "0:v",
            "-map", "1:a",
            "-shortest",
            "-c:v", "copy",
            str(FINAL_VIDEO)
        ]
    
    subprocess.run(cmd, check=True)
    print(f"[merge] Final video saved to {FINAL_VIDEO}")

def main():
    ensure_dirs()

    topic = choose_topic_for_today()
    print("=" * 60)
    print(f"=== Topic: {topic}")
    print("=" * 60)

    # 1. Generate story with Pollinations AI
    story = generate_story_with_pollinations(topic)
    
    # 2. Generate unique scene descriptions from the story
    scenes = generate_scene_descriptions(story)
    
    # 3. Generate unique images for each scene
    images = generate_images(scenes)

    # 4. Generate narration with TTS
    generate_tts(story)
    
    # 5. Generate word-level UPPERCASE subtitles with Whisper
    generate_word_subtitles()
    
    # 6. Create animated slideshow with Ken Burns effect
    create_animated_slideshow(images)
    
    # 7. Add subtitles overlay
    add_subtitles()
    
    # 8. Merge audio (narration + background music)
    merge_audio()

    print("=" * 60)
    print(f"✅ DONE. Video ready: {FINAL_VIDEO}")
    print("=" * 60)

if __name__ == "__main__":
    main()
