"""
Direct Resumable Instagram Reel Uploader via Meta Graph API v21.0
With sleep/polling method for container processing.
"""
import os, sys, time, json, requests, pathlib, subprocess

def upload_to_instagram(video_path, caption=""):
    print("\n" + "=" * 60)
    print("INSTAGRAM REELS UPLOAD (Direct Resumable v21.0)")
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

    # Auto-compress if > 12MB
    upload_file = str(video_path_obj)
    file_size = video_path_obj.stat().st_size
    if file_size > 12 * 1024 * 1024:
        compressed = str(video_path_obj.parent / f"ig_opt_{video_path_obj.name}")
        try:
            subprocess.run(["ffmpeg", "-y", "-i", str(video_path_obj), "-fs", "11M",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
                "-movflags", "+faststart", compressed], capture_output=True, check=True)
            upload_file = compressed
            file_size = os.path.getsize(compressed)
        except:
            pass

    api_base = "https://graph.facebook.com/v21.0"
    try:
        print("[instagram] Step 1: Creating resumable container...")
        c_res = requests.post(f"{api_base}/{user_id}/media", params={
            'media_type': 'REELS', 'upload_type': 'resumable',
            'caption': caption[:2200], 'access_token': access_token
        }, timeout=30)
        if c_res.status_code not in (200, 201):
            raise Exception(f"Container creation failed: {c_res.text}")
        c_data = c_res.json()
        container_id = c_data.get('id')
        upload_uri = c_data.get('uri')
        print(f"[instagram] Container ID: {container_id}")

        print("[instagram] Step 2: Transferring video...")
        with open(upload_file, 'rb') as f:
            video_bytes = f.read()
        up_res = requests.post(upload_uri, headers={
            'Authorization': f'OAuth {access_token}', 'offset': '0',
            'file_size': str(file_size), 'Content-Type': 'video/mp4'
        }, data=video_bytes, timeout=120)
        if up_res.status_code not in (200, 201):
            raise Exception(f"Transfer failed: {up_res.text}")
        print("[instagram] Video transferred!")

        # Step 3: Sleep/poll method - wait for processing then publish
        print("[instagram] Step 3: Polling for processing (sleep method)...")
        max_wait = 180
        waited = 0
        while waited < max_wait:
            time.sleep(45 if waited == 0 else 30)
            waited += 45 if waited == 0 else 30
            print(f"[instagram] Publishing (waited {waited}s)...")
            pub_res = requests.post(f"{api_base}/{user_id}/media_publish",
                params={'creation_id': container_id, 'access_token': access_token}, timeout=60)
            if pub_res.status_code in (200, 201):
                media_id = pub_res.json().get('id', container_id)
                print(f"[instagram] SUCCESS! Media ID: {media_id}")
                return {'status': 'success', 'id': media_id, 'platform': 'instagram', 'link': f"https://www.instagram.com/reel/{media_id}/"}
            if waited >= max_wait:
                raise Exception(f"Publish failed after {max_wait}s")
            print("[instagram] Not ready, retrying...")

    except Exception as e:
        print(f"[instagram] Error: {e}")
        return {'status': 'failed', 'error': str(e), 'platform': 'instagram'}
