"""
Facebook Reels Upload - Direct Resumable Upload via Meta Graph API
"""
import os, requests, time
from pathlib import Path

def upload_to_facebook(video_path, description):
    print("\n" + "=" * 60)
    print("FACEBOOK REELS UPLOAD")
    print("=" * 60)

    access_token = os.getenv('FB_ACCESS_TOKEN') or os.getenv('FACEBOOK_ACCESS_TOKEN')
    page_id = os.getenv('FB_PAGE_ID') or os.getenv('FACEBOOK_PAGE_ID')
    if not access_token or not page_id:
        print("[facebook] Skipping - missing credentials")
        return {'status': 'skipped', 'platform': 'facebook'}

    video_path_obj = Path(video_path)
    if not video_path_obj.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")

    file_size = video_path_obj.stat().st_size
    print(f"[facebook] Video: {video_path} ({file_size//1024//1024} MB)")

    try:
        # Step 1: Start upload session
        print("[facebook] Step 1: Initiating upload...")
        start_res = requests.post(f"https://graph.facebook.com/v21.0/{page_id}/video_reels", data={
            'access_token': access_token, 'upload_phase': 'start', 'file_size': file_size
        }, timeout=30)
        if start_res.status_code != 200:
            raise Exception(f"Start failed: {start_res.text}")
        j = start_res.json()
        video_id = j.get('video_id')
        upload_url = j.get('upload_url')
        if not video_id:
            raise Exception(f"No video_id: {j}")

        # Step 2: Transfer video
        print("[facebook] Step 2: Transferring video...")
        with open(video_path, 'rb') as f:
            xfer = requests.post(upload_url, headers={
                'Authorization': f'OAuth {access_token}', 'offset': '0',
                'file_size': str(file_size)
            }, data=f, timeout=600)
        if xfer.status_code != 200:
            raise Exception(f"Transfer failed: {xfer.text}")

        # Step 3: Publish
        print("[facebook] Step 3: Publishing...")
        finish = requests.post(f"https://graph.facebook.com/v21.0/{page_id}/video_reels", data={
            'access_token': access_token, 'upload_phase': 'finish',
            'video_id': video_id, 'description': description, 'video_state': 'PUBLISHED'
        }, timeout=60)
        if finish.status_code == 200 and finish.json().get('success'):
            print(f"[facebook] SUCCESS! ID: {video_id}")
            # Post pinned comment
            _post_pinned_comment(video_id, description, access_token, page_id)
            return {'id': video_id, 'platform': 'facebook', 'status': 'success'}
        else:
            raise Exception(f"Publish failed: {finish.text}")

    except Exception as e:
        print(f"[facebook] Error: {e}")
        return {'status': 'failed', 'error': str(e), 'platform': 'facebook'}

def _post_pinned_comment(video_id, description, access_token, page_id):
    print("[facebook] Posting pinned comment...")
    for attempt in range(5):
        try:
            c = requests.post(f"https://graph.facebook.com/v21.0/{video_id}/comments", data={
                'access_token': access_token, 'message': description[:1000]
            }, timeout=30)
            if c.status_code == 200:
                cid = c.json().get('id')
                if cid:
                    requests.post(f"https://graph.facebook.com/v21.0/{cid}", data={
                        'access_token': access_token, 'is_pinned': 'true'
                    }, timeout=15)
                    print("[facebook] Comment pinned!")
                    return
            elif c.status_code == 404 and attempt < 4:
                time.sleep((attempt + 1) * 10)
        except:
            break
