"""
Facebook Reels Upload - RarityBrilliance
"""

import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def _post_pinned_comment(video_id, description, access_token, page_id):
    import time
    print(f"[facebook] Posting description as pinned comment...")
    max_retries = 5
    comment_id = None
    for attempt in range(max_retries):
        try:
            comment_url = f"https://graph.facebook.com/v21.0/{video_id}/comments"
            comment_data = {'access_token': access_token, 'message': description}
            res_comment = requests.post(comment_url, data=comment_data, timeout=30)
            if res_comment.status_code == 200:
                resp = res_comment.json()
                comment_id = resp.get('id')
                if comment_id:
                    print(f"[facebook] Comment posted! ID: {comment_id}")
                    break
            elif res_comment.status_code == 404 and attempt < max_retries - 1:
                wait = (attempt + 1) * 10
                time.sleep(wait)
        except Exception as e:
            print(f"[facebook] Comment post error: {e}")
            break
    if comment_id:
        try:
            pin_url = f"https://graph.facebook.com/v21.0/{comment_id}"
            pin_data = {'access_token': access_token, 'is_pinned': 'true'}
            requests.post(pin_url, data=pin_data, timeout=15)
        except Exception as e:
            print(f"[facebook] Pin error: {e}")

def upload_to_facebook(video_path, description, title="RarityBrilliance"):
    print("\n" + "=" * 60)
    print("FACEBOOK UPLOAD")
    print("=" * 60)
    access_token = os.getenv('FACEBOOK_ACCESS_TOKEN') or os.getenv('FB_ACCESS_TOKEN')
    page_id = os.getenv('FACEBOOK_PAGE_ID') or os.getenv('FB_PAGE_ID')
    if not access_token: raise ValueError("FACEBOOK_ACCESS_TOKEN not set")
    if not page_id: raise ValueError("FACEBOOK_PAGE_ID not set")
    video_path_obj = Path(video_path)
    if not video_path_obj.exists(): raise FileNotFoundError(f"Video not found: {video_path}")
    try:
        file_size = video_path_obj.stat().st_size
        start_url = f"https://graph.facebook.com/v21.0/{page_id}/video_reels"
        start_data = {'access_token': access_token, 'upload_phase': 'start', 'file_size': file_size}
        res_start = requests.post(start_url, data=start_data, timeout=30)
        if res_start.status_code != 200: raise Exception(f"Start failed: {res_start.text}")
        start_json = res_start.json()
        video_id = start_json.get('video_id')
        upload_url = start_json.get('upload_url')
        if not video_id: raise Exception(f"No video_id: {start_json}")
        headers = {'Authorization': f'OAuth {access_token}', 'offset': '0', 'file_size': str(file_size)}
        with open(video_path, 'rb') as f:
            res_transfer = requests.post(upload_url, headers=headers, data=f, timeout=600)
        if res_transfer.status_code != 200: raise Exception(f"Transfer failed: {res_transfer.text}")
        finish_url = f"https://graph.facebook.com/v21.0/{page_id}/video_reels"
        finish_data = {'access_token': access_token, 'upload_phase': 'finish', 'video_id': video_id, 'description': description, 'video_state': 'PUBLISHED'}
        res_finish = requests.post(finish_url, data=finish_data, timeout=60)
        if res_finish.status_code == 200 and res_finish.json().get('success'):
            _post_pinned_comment(video_id, description, access_token, page_id)
            return {'id': video_id, 'platform': 'facebook', 'status': 'success', 'url': f"https://facebook.com/{video_id}"}
        else: raise Exception(f"Finish failed: {res_finish.text}")
    except Exception as e: print(f"[facebook] ERROR: {e}"); raise

if __name__ == '__main__':
    video_file = Path('final_video.mp4')
    if video_file.exists():
        try: upload_to_facebook(str(video_file), "Test")
        except Exception as e: print(f"Failed: {e}")

