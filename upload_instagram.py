"""
Instagram Reels Upload

Instagram Graph API for uploading Reels.
Requires: Business/Creator account + Facebook Page
"""

import os
import requests
import time
from pathlib import Path

def upload_to_instagram(video_file, caption):
    """Upload video to Instagram Reels."""
    
    access_token = os.getenv('IG_ACCESS_TOKEN')
    user_id = os.getenv('IG_USER_ID')
    
    if not access_token or not user_id:
        raise ValueError("Missing IG_ACCESS_TOKEN or IG_USER_ID")
    
    print(f"[instagram] Uploading: {video_file}")
    
    # Step 1: Create media container
    url = f"https://graph.facebook.com/v18.0/{user_id}/media"
    
    params = {
        'access_token': access_token,
        'media_type': 'REELS',
        'video_url': video_file,  # Must be publicly accessible URL
        'caption': caption,
        'share_to_feed': True
    }
    
    response = requests.post(url, params=params)
    response.raise_for_status()
    container_id = response.json()['id']
    
    print(f"[instagram] Container created: {container_id}")
    
    # Step 2: Wait for processing
    print("[instagram] Waiting for video processing...")
    time.sleep(30)  # Instagram needs time to process
    
    # Step 3: Publish
    publish_url = f"https://graph.facebook.com/v18.0/{user_id}/media_publish"
    publish_params = {
        'access_token': access_token,
        'creation_id': container_id
    }
    
    publish_response = requests.post(publish_url, params=publish_params)
    publish_response.raise_for_status()
    
    media_id = publish_response.json()['id']
    print(f"[instagram] ✅ Published! Media ID: {media_id}")
    
    return {'id': media_id}

# Note: Instagram requires the video to be hosted at a public URL
# You'll need to upload to a temporary hosting service first
# Or use Instagram's container upload API with local files
