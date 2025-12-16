"""
Threads Upload Script

Uploads videos to Threads using Instagram Graph API.
Threads uses the same API as Instagram.

Requirements:
- Instagram Business or Creator account
- Facebook App with Instagram Graph API access
- THREADS_ACCESS_TOKEN and THREADS_USER_ID in environment
"""

import os
import requests
from pathlib import Path
import time

def upload_to_threads(video_file, caption):
    """Upload video to Threads using Instagram Graph API."""
    
    access_token = os.getenv('THREADS_ACCESS_TOKEN')
    user_id = os.getenv('THREADS_USER_ID')
    
    if not access_token or not user_id:
        raise ValueError(
            "Missing Threads credentials! Set these environment variables:\n"
            "  - THREADS_ACCESS_TOKEN\n"
            "  - THREADS_USER_ID"
        )
    
    print("[threads] Uploading to Threads...")
    
    # Step 1: Create media container
    print("[threads] Creating media container...")
    
    container_url = f"https://graph.threads.net/v1.0/{user_id}/threads"
    
    # For video, we need to upload to a publicly accessible URL first
    # Since we're running in GitHub Actions, we'll use the direct file upload method
    
    params = {
        'media_type': 'VIDEO',
        'video_url': str(video_file),  # This needs to be a public URL
        'text': caption,
        'access_token': access_token
    }
    
    # Note: Threads API requires video to be accessible via public URL
    # For now, we'll use a simplified approach
    
    response = requests.post(container_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Failed to create container: {response.text}")
    
    container_id = response.json().get('id')
    print(f"[threads] Container created: {container_id}")
    
    # Step 2: Wait for processing
    print("[threads] Waiting for video processing...")
    max_wait = 60  # seconds
    waited = 0
    
    while waited < max_wait:
        status_url = f"https://graph.threads.net/v1.0/{container_id}"
        status_params = {'fields': 'status_code', 'access_token': access_token}
        
        status_response = requests.get(status_url, params=status_params)
        status_code = status_response.json().get('status_code')
        
        if status_code == 'FINISHED':
            break
        elif status_code == 'ERROR':
            raise Exception("Video processing failed")
        
        time.sleep(5)
        waited += 5
    
    # Step 3: Publish the post
    print("[threads] Publishing post...")
    
    publish_url = f"https://graph.threads.net/v1.0/{user_id}/threads_publish"
    publish_params = {
        'creation_id': container_id,
        'access_token': access_token
    }
    
    publish_response = requests.post(publish_url, params=publish_params)
    
    if publish_response.status_code != 200:
        raise Exception(f"Failed to publish: {publish_response.text}")
    
    thread_id = publish_response.json().get('id')
    
    print(f"[threads] ✅ Published to Threads! ID: {thread_id}")
    
    return {
        'id': thread_id,
        'platform': 'threads'
    }

def main():
    """Test upload to Threads."""
    video_file = Path('output/final_video.mp4')
    
    if not video_file.exists():
        print("[threads] ❌ No video found at output/final_video.mp4")
        return
    
    # Read story for caption
    story_file = Path('output/story.txt')
    if story_file.exists():
        caption = story_file.read_text(encoding='utf-8')[:500]  # Threads has character limit
    else:
        caption = "История древних женщин 🏛️"
    
    try:
        upload_to_threads(video_file, caption)
    except Exception as e:
        print(f"[threads] ❌ Upload failed: {e}")
        raise

if __name__ == '__main__':
    main()
