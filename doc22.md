✅ FINAL & CORRECT TOOLCHAIN (ONLY THESE — NOTHING ELSE)

Below is your entire automation stack — clean, simple, correct.

🎯 1. Pollinations AI (FREE) — For Story + Images
Purpose:

Generate the 30–40 sec story

Generate 10–15 images from scene prompts

How it works:

No API key

Simple GET request

Text endpoint:
https://text.pollinations.ai/{PROMPT}

Image endpoint:
https://image.pollinations.ai/prompt/{PROMPT}?width=1080&height=1920&model=flux

Link (official docs):

https://pollinations.ai

Polinations image search documentation describes parameters like width, height, model, and style. No official API key is required for text or image generation.

🎯 2. Coqui TTS (FREE) — For Narration Voice
Purpose:

Convert story → human-like voice narration
(Offline, free, commercial-safe)

Install:
pip install TTS

Avoid other TTS packages.

Use ONLY this one.

Link:

https://github.com/coqui-ai/TTS

🎯 3. Whisper (FREE) — For Subtitle Generation
Purpose:

Convert narration audio → word-level timestamps
Used to create synchronized subtitles.

Install:
pip install openai-whisper

Link:

https://github.com/openai/whisper

🎯 4. FFmpeg (FREE) — For Slideshow Animation + Video Merge
Purpose:

Animate images (zoom-in/out motion effects)

Overlay subtitles

Merge audio + music

Export final MP4

Install (GitHub Actions):
sudo apt-get install ffmpeg

Link:

https://ffmpeg.org

🎯 5. Python (Main Script)

Your script does:

Pollinations → story

Pollinations → images

Coqui TTS → narration

Whisper → subtitles w/ timestamps

FFmpeg → animation + overlay subtitles

FFmpeg → merge music + voice

🎯 6. GitHub Actions (FREE)

Runs everything automatically each day.

🧱 FINAL, CLEAN PROJECT DEPENDENCIES

requirements.txt MUST contain ONLY these:

requests
TTS
openai-whisper
numpy


(Whisper needs numpy)

⭐ NOW — LET ME CLARIFY THE TWO PARTS YOU ASKED FOR:
📌 (A) ANIMATION — What exactly are we using?

We are using FFmpeg’s zoompan filter to create short animations for each image.

Example:

-vf "zoompan=z='zoom+0.001':d=60"


This creates Ken Burns motion effect:

slow zoom

small pan

cinematic movement

We also concatenate all clips into ~40 sec video.

This is stable, free, fast.

📌 (B) SUBTITLES — How they appear?

You want:

One word at a time

Synchronized with the narration audio

Big subtitles

Centered in the middle

We will generate word-level timestamps using Whisper:

Example output:

word	start	end
"Once"	0.10	0.50
"upon"	0.50	0.80
"a"	0.80	1.00
"time"	1.00	1.40

Then we convert it into ASS subtitle format (better than SRT for styling):

ASS supports:

✔ large font
✔ center alignment
✔ one word per time interval
✔ no background box unless you want
✔ smooth fading

An example ASS style:

Style: Default,Arial,72,&H00FFFFFF,&H000000FF,&H0,&H0,0,0,2,2,30,30,10,10,1

📌 (C) Subtitle Position (Middle of Screen)

ASS style includes:

Alignment=5   (center middle)

📌 (D) Audio Merge (No volume adjustments unless YOU want)

You said:

use default TTS volume, don't change it
we will pick music ourselves and adjust manually

So:

We merge narration + music with default mixing:

amix=inputs=2

📌 (E) What your final FFmpeg pipeline does:

Create 15 animated video clips (1–3 sec each)

Concatenate them into a 30–40 sec video

Overlay ASS subtitles

Mix narration + music

Output final MP4

🎁 NOW I WILL WRITE EVERYTHING IN ONE CLEAR LIST FOR YOUR IDE (Cursor)
🧰 THE COMPLETE TOOL LIST (FINAL)
1. Pollinations AI

✔ Story generation
✔ Image generation
✔ No API key
✔ Simple GET requests
✔ Free forever

2. Coqui TTS

✔ Converts story → narration
✔ Free, open-source
✔ High-quality
✔ Works offline
✔ Commercial safe

Install:

pip install TTS

3. Whisper (local)

✔ Generates subtitles
✔ Word-level timestamps
✔ Free
✔ Works offline
✔ Good accuracy

Install:

pip install openai-whisper

4. FFmpeg

✔ Image animation
✔ Subtitle overlay (ASS format)
✔ Audio mixing
✔ Final MP4 output

Install:

sudo apt-get install ffmpeg

5. GitHub Actions

✔ Automates everything
✔ CPU only
✔ Free (2,000–3,000 minutes/month)

📌 Now tell me this:



