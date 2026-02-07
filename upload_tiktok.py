"""
TikTok Upload - Enhanced Version

TikTok Content Posting API for uploading videos.
Requires: TikTok Developer account + OAuth
Supports both file upload and URL-based methods
"""

import os
import requests
import time
from pathlib import Path
import tempfile


def upload_file_to_tmpfiles(file_path):
    """Upload file to tmpfiles.org and return public URL"""
    print("[tiktok] Uploading video to temporary hosting...")
    
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
            print(f"[tiktok] File uploaded: {dl_url}")
            return dl_url
        else:
            raise Exception(f"tmpfiles.org returned error status: {data}")
    else:
        raise Exception(f"Failed to upload to tmpfiles.org: {response.status_code} - {response.text}")


def check_tiktok_upload_status(publish_id, access_token):
    """Check the status of TikTok upload"""
    url = f"https://open.tiktokapis.com/v2/post/status/fetch/?publish_id={publish_id}"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else None


def upload_to_tiktok(video_file, title, description):
    """Upload video to TikTok with improved error handling and status checking."""
    
    access_token = os.getenv('TIKTOK_ACCESS_TOKEN')
    
    if not access_token:
        raise ValueError("Missing TIKTOK_ACCESS_TOKEN")
    
    video_file = Path(video_file)
    if not video_file.exists():
        raise FileNotFoundError(f"Video file not found: {video_file}")
    
    print(f"[tiktok] Preparing to upload: {video_file}")
    print(f"[tiktok] Title: {title}")
    print(f"[tiktok] Description: {description}")
    
    # Method 1: Try direct file upload (primary method)
    try:
        print("[tiktok] Attempting direct file upload...")
        result = upload_via_file(video_file, title, description, access_token)
        return result
    except Exception as e:
        print(f"[tiktok] Direct file upload failed: {e}")
        print("[tiktok] Falling back to URL-based upload...")
        
        # Method 2: Upload via URL (fallback)
        try:
            video_url = upload_file_to_tmpfiles(video_file)
            return upload_via_url(video_url, title, description, access_token)
        except Exception as e2:
            print(f"[tiktok] Both upload methods failed:")
            print(f"  Direct upload: {e}")
            print(f"  URL upload: {e2}")
            raise e2


def upload_via_file(video_file, title, description, access_token):
    """Upload video file directly to TikTok"""
    url = "https://open.tiktokapis.com/v2/post/publish/video/init/"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'post_info': {
            'title': title[:150],  # TikTok title limit
            'description': description[:2200],  # TikTok description limit
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
    print("[tiktok] Initializing upload...")
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code != 200:
        error_data = response.json() if response.content else {}
        raise Exception(f"Failed to initialize upload: {error_data}")
    
    result = response.json()
    if 'data' not in result or 'publish_id' not in result['data']:
        raise Exception(f"Unexpected response format: {result}")
    
    publish_id = result['data']['publish_id']
    upload_url = result['data']['upload_url']
    
    print(f"[tiktok] Upload initialized: {publish_id}")
    print(f"[tiktok] Uploading video file...")
    
    # Upload video file
    with open(video_file, 'rb') as f:
        video_data = f.read()
        
    upload_response = requests.put(
        upload_url,
        headers={'Content-Type': 'video/mp4'},
        data=video_data
    )
    
    if upload_response.status_code != 200:
        error_data = upload_response.json() if upload_response.content else {}
        raise Exception(f"Failed to upload video: {error_data}")
    
    print(f"[tiktok] Video uploaded successfully!")
    
    # Check status with retries
    print("[tiktok] Checking upload status (this may take 1-2 minutes)...")
    max_wait_time = 120  # 2 minutes max wait
    wait_interval = 5
    elapsed = 0
    
    while elapsed < max_wait_time:
        status_response = check_tiktok_upload_status(publish_id, access_token)
        if status_response and 'data' in status_response and 'status' in status_response['data']:
            status = status_response['data']['status']
            print(f"[tiktok] Current status: {status}")
            
            if status == 'SUCCESS':
                print(f"[tiktok] ✅ Upload completed successfully!")
                return {'id': publish_id, 'status': 'published'}
            elif status == 'PROCESSING':
                print(f"[tiktok] Still processing...")
            elif status == 'FAILED':
                raise Exception(f"Upload failed: {status_response}")
        
        time.sleep(wait_interval)
        elapsed += wait_interval
    
    # If we reach here, max time was reached
    print(f"[tiktok] ⚠️ Max wait time reached, upload may still be processing")
    return {
        'id': publish_id,
        'status': 'processing',
        'warning': 'Max wait time reached, please check TikTok for final status'
    }


def upload_via_url(video_url, title, description, access_token):
    """Upload video via URL to TikTok"""
    url = "https://open.tiktokapis.com/v2/post/publish/video/init/"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'post_info': {
            'title': title[:150],  # TikTok title limit
            'description': description[:2200],  # TikTok description limit
            'privacy_level': 'PUBLIC_TO_EVERYONE',
            'disable_duet': False,
            'disable_comment': False,
            'disable_stitch': False,
            'video_cover_timestamp_ms': 1000
        },
        'source_info': {
            'source': 'PULL_FROM_URL',
            'video_url': video_url
        }
    }
    
    print("[tiktok] Initializing URL-based upload...")
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code != 200:
        error_data = response.json() if response.content else {}
        raise Exception(f"Failed to initialize URL upload: {error_data}")
    
    result = response.json()
    if 'data' not in result or 'publish_id' not in result['data']:
        raise Exception(f"Unexpected response format: {result}")
    
    publish_id = result['data']['publish_id']
    
    print(f"[tiktok] Upload initialized: {publish_id}")
    print(f"[tiktok] TikTok will pull video from URL...")
    
    # Check status with retries
    print("[tiktok] Checking upload status (this may take 1-2 minutes)...")
    max_wait_time = 120  # 2 minutes max wait
    wait_interval = 5
    elapsed = 0
    
    while elapsed < max_wait_time:
        status_response = check_tiktok_upload_status(publish_id, access_token)
        if status_response and 'data' in status_response and 'status' in status_response['data']:
            status = status_response['data']['status']
            print(f"[tiktok] Current status: {status}")
            
            if status == 'SUCCESS':
                print(f"[tiktok] ✅ Upload completed successfully!")
                return {'id': publish_id, 'status': 'published'}
            elif status == 'PROCESSING':
                print(f"[tiktok] Still processing...")
            elif status == 'FAILED':
                raise Exception(f"Upload failed: {status_response}")
        
        time.sleep(wait_interval)
        elapsed += wait_interval
    
    # If we reach here, max time was reached
    print(f"[tiktok] ⚠️ Max wait time reached, upload may still be processing")
    return {
        'id': publish_id,
        'status': 'processing',
        'warning': 'Max wait time reached, please check TikTok for final status'
    }


if __name__ == "__main__":
    # Test the function
    import sys
    if len(sys.argv) < 4:
        print("Usage: python upload_tiktok.py <video_path> <title> <description>")
        sys.exit(1)
    
    video_path = Path(sys.argv[1])
    title = sys.argv[2]
    description = sys.argv[3]
    
    try:
        result = upload_to_tiktok(video_path, title, description)
        print(f"Success: {result}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
