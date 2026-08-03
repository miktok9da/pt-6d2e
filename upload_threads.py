"""
Threads Upload Script - Enhanced Version

Uploads videos to Threads using Instagram Graph API.
Threads uses the same API as Instagram.

Requirements:
- Instagram Business or Creator account
- Facebook App with Instagram Graph API access
- THREADS_ACCESS_TOKEN and THREADS_USER_ID in environment
Uses temporary file hosting for improved compatibility.
"""

import os
import requests
from pathlib import Path
import time


def upload_file_to_tmpfiles(file_path):
    """Upload file to tmpfiles.org and return public URL"""
    print("[threads] Uploading video to temporary hosting...")
    
    with open(file_path, 'rb') as f:
        response = requests.post(
            'https://tmpfiles.org/api/v1/upload',
            files={'file': (Path(file_path).name, f, 'video/mp4')}
        )
    
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'success':
            url = data['data']['url']
            # Convert to direct download link and ensure HTTPS
            dl_url = url.replace('tmpfiles.org/', 'tmpfiles.org/dl/').replace('http://', 'https://')
            print(f"[threads] File uploaded: {dl_url}")
            return dl_url
        else:
            raise Exception(f"tmpfiles.org returned error status: {data}")
    else:
        raise Exception(f"Failed to upload to tmpfiles.org: {response.status_code} - {response.text}")


def check_threads_upload_status(container_id, access_token):
    """Check the status of Threads upload"""
    status_url = f"https://graph.threads.net/v1.0/{container_id}"
    status_params = {
        'fields': 'status_code',
        'access_token': access_token
    }
    
    response = requests.get(status_url, params=status_params)
    return response.json() if response.status_code == 200 else None


def upload_to_threads(video_file, caption):
    """Upload video to Threads using Instagram Graph API with improved error handling and status checking."""
    
    access_token = os.getenv('THREADS_ACCESS_TOKEN')
    user_id = os.getenv('THREADS_USER_ID')
    
    if not access_token or not user_id:
        raise ValueError(
            "Missing Threads credentials! Set these environment variables:\n"
            "  - THREADS_ACCESS_TOKEN\n"
            "  - THREADS_USER_ID"
        )
    
    video_file = Path(video_file)
    if not video_file.exists():
        raise FileNotFoundError(f"Video file not found: {video_file}")
    
    print(f"[threads] Preparing to upload: {video_file}")
    
    # Upload video to temporary hosting service
    try:
        video_url = upload_file_to_tmpfiles(video_file)
        print(f"[threads] Using temporary URL: {video_url}")
    except Exception as e:
        raise Exception(f"Failed to upload video to temporary hosting: {e}")
    
    # Step 1: Create media container using the temporary URL
    print("[threads] Creating media container...")
    
    container_url = f"https://graph.threads.net/v1.0/{user_id}/threads"
    
    params = {
        'media_type': 'VIDEO',
        'video_url': video_url,  # Now using public URL from tmpfiles
        'text': caption[:500],  # Threads has character limit
        'access_token': access_token
    }
    
    response = requests.post(container_url, params=params)
    
    if response.status_code != 200:
        error_data = response.json() if response.content else {}
        raise Exception(f"Failed to create container: {error_data}")
    
    container_response = response.json()
    if 'id' not in container_response:
        raise Exception(f"Unexpected response format: {container_response}")
    
    container_id = container_response['id']
    print(f"[threads] Container created: {container_id}")
    
    # Step 2: Wait for processing with status checks
    print("[threads] Waiting for video processing (this may take 1-2 minutes)...")
    max_wait_time = 120  # 2 minutes max wait
    wait_interval = 5
    elapsed = 0
    
    while elapsed < max_wait_time:
        status_response = check_threads_upload_status(container_id, access_token)
        if status_response and 'status_code' in status_response:
            status_code = status_response['status_code']
            print(f"[threads] Current status: {status_code}")
            
            if status_code == 'FINISHED':
                print("[threads] Processing complete!")
                break
            elif status_code == 'ERROR':
                raise Exception("Video processing failed")
        
        time.sleep(wait_interval)
        elapsed += wait_interval
    
    if elapsed >= max_wait_time:
        print("[threads] Warning: Max wait time reached, proceeding anyway...")
    
    # Step 3: Publish the post
    print("[threads] Publishing post...")
    
    publish_url = f"https://graph.threads.net/v1.0/{user_id}/threads_publish"
    publish_params = {
        'creation_id': container_id,
        'access_token': access_token
    }
    
    publish_response = requests.post(publish_url, params=publish_params)
    
    if publish_response.status_code != 200:
        error_data = publish_response.json() if publish_response.content else {}
        raise Exception(f"Failed to publish: {error_data}")
    
    result = publish_response.json()
    if 'id' not in result:
        raise Exception(f"Unexpected publish response: {result}")
    
    thread_id = result['id']
    thread_url = f"https://www.threads.net/@t/{thread_id}" if thread_id else None
    
    print(f"[threads] ✅ Published to Threads!")
    print(f"[threads] Thread ID: {thread_id}")
    print(f"[threads] Thread URL: {thread_url}")
    
    return {
        'id': thread_id,
        'url': thread_url,
        'platform': 'threads',
        'status': 'success'
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
        caption = "História das mulheres antigas 🏛️"  # Updated to Portuguese
    
    try:
        result = upload_to_threads(video_file, caption)
        print(f"[threads] Success: {result}")
    except Exception as e:
        print(f"[threads] ❌ Upload failed: {e}")
        raise

if __name__ == '__main__':
    main()
