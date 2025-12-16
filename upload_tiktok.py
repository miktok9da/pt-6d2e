"""
TikTok Upload

TikTok Content Posting API for uploading videos.
Requires: TikTok Developer account + OAuth
"""

import os
import requests

def upload_to_tiktok(video_file, title, description):
    """Upload video to TikTok."""
    
    access_token = os.getenv('TIKTOK_ACCESS_TOKEN')
    
    if not access_token:
        raise ValueError("Missing TIKTOK_ACCESS_TOKEN")
    
    print(f"[tiktok] Uploading: {video_file}")
    
    # TikTok Content Posting API
    url = "https://open.tiktokapis.com/v2/post/publish/video/init/"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'post_info': {
            'title': title,
            'description': description,
            'privacy_level': 'PUBLIC_TO_EVERYONE',
            'disable_duet': False,
            'disable_comment': False,
            'disable_stitch': False,
            'video_cover_timestamp_ms': 1000
        },
        'source_info': {
            'source': 'FILE_UPLOAD',
            'video_size': os.path.getsize(video_file),
            'chunk_size': 10000000,
            'total_chunk_count': 1
        }
    }
    
    # Initialize upload
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    
    result = response.json()
    publish_id = result['data']['publish_id']
    upload_url = result['data']['upload_url']
    
    print(f"[tiktok] Upload initialized: {publish_id}")
    
    # Upload video file
    with open(video_file, 'rb') as f:
        video_data = f.read()
        
    upload_response = requests.put(
        upload_url,
        headers={'Content-Type': 'video/mp4'},
        data=video_data
    )
    upload_response.raise_for_status()
    
    print(f"[tiktok] ✅ Uploaded! Publish ID: {publish_id}")
    
    return {'id': publish_id}
