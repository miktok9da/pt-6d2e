"""
Direct Resumable Instagram Reel Uploader via Meta Graph API v21.0
Robust: creates a resumable container, uploads the video, polls the
container status until FINISHED, then publishes. Publishes to REELS only.
Keeps API calls to a minimum (create + upload + status poll + publish).
"""
import os, time, requests, pathlib, subprocess, json

API_BASE = "https://graph.facebook.com/v21.0"


def _compress(video_path_obj, max_bytes=8 * 1024 * 1024):
    """Return a path to a version of the video under max_bytes (best effort)."""
    if video_path_obj.stat().st_size <= max_bytes:
        return str(video_path_obj)
    compressed = str(video_path_obj.parent / f"ig_opt_{video_path_obj.name}")
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(video_path_obj), "-fs", f"{max_bytes // (1024 * 1024)}M",
             "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "96k",
             "-movflags", "+faststart", compressed],
            capture_output=True, check=True, timeout=300)
        if os.path.getsize(compressed) < video_path_obj.stat().st_size:
            return compressed
    except Exception:
        pass
    return str(video_path_obj)


def upload_to_instagram(video_path, caption=""):
    print("\n" + "=" * 60)
    print("INSTAGRAM REELS UPLOAD (Resumable + Status Poll)")
    print("=" * 60)

    access_token = os.getenv('IG_ACCESS_TOKEN') or os.getenv('INSTAGRAM_ACCESS_TOKEN') or os.getenv('FACEBOOK_ACCESS_TOKEN')
    user_id = os.getenv('IG_USER_ID') or os.getenv('INSTAGRAM_ACCOUNT_ID')

    if not access_token or not user_id:
        print("[instagram] Skipping - missing credentials")
        return {'status': 'skipped', 'platform': 'instagram'}

    video_path_obj = pathlib.Path(video_path)
    if not video_path_obj.exists():
        print(f"[instagram] Video not found: {video_path}")
        return {'status': 'failed', 'error': 'Video not found', 'platform': 'instagram'}

    upload_file = _compress(video_path_obj)
    file_size = os.path.getsize(upload_file)
    print(f"[instagram] Uploading file: {upload_file} ({file_size} bytes)")

    try:
        # Step 1: Create resumable container (1 API call)
        print("[instagram] Step 1: Creating resumable container...")
        c_res = requests.post(f"{API_BASE}/{user_id}/media", params={
            'media_type': 'REELS', 'upload_type': 'resumable',
            'caption': caption[:2200], 'access_token': access_token
        }, timeout=30)
        if c_res.status_code not in (200, 201):
            raise Exception(f"Container creation failed: {c_res.text}")
        c_data = c_res.json()
        container_id = c_data.get('id')
        upload_uri = c_data.get('uri')
        print(f"[instagram] Container ID: {container_id}")

        # Step 2: Transfer the video to the upload URI (1 API call)
        print("[instagram] Step 2: Transferring video...")
        with open(upload_file, 'rb') as f:
            video_bytes = f.read()
        up_res = requests.post(upload_uri, headers={
            'Authorization': f'OAuth {access_token}',
            'offset': '0',
            'file_size': str(file_size),
            'Content-Type': 'video/mp4'
        }, data=video_bytes, timeout=180)
        if up_res.status_code not in (200, 201):
            raise Exception(f"Transfer failed: {up_res.text}")
        print("[instagram] Video transferred!")

        # Step 3: Poll container status until FINISHED (status polls)
        print("[instagram] Step 3: Polling container status...")
        max_wait = 300
        waited = 0
        step = 30
        while waited < max_wait:
            time.sleep(step)
            waited += step
            st_res = requests.get(f"{API_BASE}/{container_id}",
                params={'fields': 'status_code', 'access_token': access_token}, timeout=30)
            if st_res.status_code not in (200, 201):
                print(f"[instagram] Status check returned {st_res.status_code}, retrying...")
                continue
            status_code = st_res.json().get('status_code')
            print(f"[instagram] Container status: {status_code} (waited {waited}s)")
            if status_code == 'FINISHED':
                break
            if status_code in ('ERROR', 'EXPIRED', 'FAILED'):
                raise Exception(f"Container status error: {status_code} - {st_res.text}")
        else:
            raise Exception(f"Container never finished after {max_wait}s")

        # Step 4: Publish (1 API call)
        print("[instagram] Step 4: Publishing reel...")
        pub_res = requests.post(f"{API_BASE}/{user_id}/media_publish",
            params={'creation_id': container_id, 'access_token': access_token}, timeout=60)
        if pub_res.status_code not in (200, 201):
            raise Exception(f"Publish failed: {pub_res.text}")
        media_id = pub_res.json().get('id', container_id)
        print(f"[instagram] SUCCESS! Media ID: {media_id}")
        print(f"[instagram] Reel URL: https://www.instagram.com/reel/{media_id}/")
        return {'status': 'success', 'id': media_id, 'platform': 'instagram',
                'link': f"https://www.instagram.com/reel/{media_id}/"}

    except Exception as e:
        print(f"[instagram] Error: {e}")
        return {'status': 'failed', 'error': str(e), 'platform': 'instagram'}
