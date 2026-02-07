"""
Instagram Reels Upload - Enhanced Version

Instagram Graph API for uploading Reels.
Requires: Business/Creator account + Facebook Page
"""

import os
import requests
import time
from pathlib import Path
import tempfile
import subprocess


def upload_file_to_tmpfiles(file_path):
    """Upload file to tmpfiles.org and return public URL"""
    print("[instagram] Uploading video to temporary hosting...")
    
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
            print(f"[instagram] File uploaded: {dl_url}")
            return dl_url
        else:
            raise Exception(f"tmpfiles.org returned error status: {data}")
    else:
        raise Exception(f"Failed to upload to tmpfiles.org: {response.status_code} - {response.text}")


def check_upload_status(external_id):
    """Check the status of Instagram upload"""
    access_token = os.getenv('IG_ACCESS_TOKEN')
    user_id = os.getenv('IG_USER_ID')
    
    url = f"https://graph.facebook.com/v18.0/{user_id}/media/{external_id}"
    params = {
        'access_token': access_token
    }
    
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else None


def upload_to_instagram(video_file, caption):
    """Upload video to Instagram Reels with improved error handling and status checking."""
    
    access_token = os.getenv('IG_ACCESS_TOKEN')
    user_id = os.getenv('IG_USER_ID')
    
    if not access_token or not user_id:
        raise ValueError("Missing IG_ACCESS_TOKEN or IG_USER_ID")
    
    print(f"[instagram] Preparing to upload: {video_file}")
    
    # Upload video to temporary hosting service
    try:
        video_url = upload_file_to_tmpfiles(video_file)
        print(f"[instagram] Using temporary URL: {video_url}")
    except Exception as e:
        raise Exception(f"Failed to upload video to temporary hosting: {e}")
    
    # Step 1: Create media container
    url = f"https://graph.facebook.com/v18.0/{user_id}/media"
    
    params = {
        'access_token': access_token,
        'media_type': 'REELS',
        'video_url': video_url,
        'caption': caption,
        'share_to_feed': True
    }
    
    print("[instagram] Creating media container...")
    response = requests.post(url, params=params)
    
    if response.status_code != 200:
        error_data = response.json() if response.content else {}
        raise Exception(f"Failed to create media container: {error_data}")
    
    container_data = response.json()
    if 'id' not in container_data:
        raise Exception(f"Unexpected response format: {container_data}")
    
    container_id = container_data['id']
    print(f"[instagram] Container created: {container_id}")
    
    # Step 2: Wait for container processing with status checks
    print("[instagram] Waiting for video processing (this may take 1-2 minutes)...")
    max_wait_time = 120  # 2 minutes max wait
    wait_interval = 5
    elapsed = 0
    
    while elapsed < max_wait_time:
        status_response = check_upload_status(container_id)
        if status_response and 'status' in status_response:
            status = status_response['status']
            print(f"[instagram] Current status: {status}")
            
            if status == 'FINISHED':
                print("[instagram] Processing complete!")
                break
            elif status == 'ERROR':
                raise Exception(f"Upload failed with status: {status}")
        
        time.sleep(wait_interval)
        elapsed += wait_interval
    
    if elapsed >= max_wait_time:
        print("[instagram] Warning: Max wait time reached, proceeding anyway...")
    
    # Step 3: Publish
    publish_url = f"https://graph.facebook.com/v18.0/{user_id}/media_publish"
    publish_params = {
        'access_token': access_token,
        'creation_id': container_id
    }
    
    print("[instagram] Publishing reel...")
    publish_response = requests.post(publish_url, params=publish_params)
    
    if publish_response.status_code != 200:
        error_data = publish_response.json() if publish_response.content else {}
        raise Exception(f"Failed to publish: {error_data}")
    
    result = publish_response.json()
    if 'id' not in result:
        raise Exception(f"Unexpected publish response: {result}")
    
    media_id = result['id']
    post_url = f"https://www.instagram.com/p/{get_shortcode_from_media_id(media_id)}" if get_shortcode_from_media_id(media_id) else f"https://www.instagram.com/reel/{media_id}/"
    
    print(f"[instagram] ✅ Successfully published!")
    print(f"[instagram] Media ID: {media_id}")
    print(f"[instagram] Post URL: {post_url}")
    
    return {
        'id': media_id,
        'url': post_url,
        'status': 'published'
    }


def get_shortcode_from_media_id(media_id):
    """Convert media ID to Instagram shortcode for URL"""
    try:
        # Instagram media IDs are in a specific format, try to convert
        # This is a simplified conversion - in practice, you'd need to use another API call
        return None  # Return None for now since direct conversion is complex
    except:
        return None


if __name__ == "__main__":
    # Test the function
    import sys
    if len(sys.argv) < 3:
        print("Usage: python upload_instagram.py <video_path> <caption>")
        sys.exit(1)
    
    video_path = Path(sys.argv[1])
    caption = sys.argv[2]
    
    try:
        result = upload_to_instagram(video_path, caption)
        print(f"Success: {result}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
