"""
Facebook Reels Upload - Enhanced Version

Facebook Graph API for uploading Reels to Facebook Page.
Uses temporary file hosting for improved compatibility.
"""

import os
import requests
import time
from pathlib import Path


def upload_file_to_tmpfiles(file_path):
    """Upload file to tmpfiles.org and return public URL"""
    print("[facebook] Uploading video to temporary hosting...")
    
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
            print(f"[facebook] File uploaded: {dl_url}")
            return dl_url
        else:
            raise Exception(f"tmpfiles.org returned error status: {data}")
    else:
        raise Exception(f"Failed to upload to tmpfiles.org: {response.status_code} - {response.text}")


def upload_to_facebook(video_file, description):
    """Upload video to Facebook Reels with improved error handling and temporary hosting."""
    
    access_token = os.getenv('FB_ACCESS_TOKEN')
    page_id = os.getenv('FB_PAGE_ID')
    
    if not access_token or not page_id:
        raise ValueError("Missing FB_ACCESS_TOKEN or FB_PAGE_ID")
    
    video_file = Path(video_file)
    if not video_file.exists():
        raise FileNotFoundError(f"Video file not found: {video_file}")
    
    print(f"[facebook] Preparing to upload: {video_file}")
    
    # Upload video to temporary hosting service
    try:
        video_url = upload_file_to_tmpfiles(video_file)
        print(f"[facebook] Using temporary URL: {video_url}")
    except Exception as e:
        raise Exception(f"Failed to upload video to temporary hosting: {e}")
    
    # Upload video using the temporary URL
    url = f"https://graph.facebook.com/v24.0/{page_id}/videos"
    
    params = {
        'access_token': access_token,
        'description': description,
        'title': 'História das Mulheres Antigas',  # Updated to Portuguese
        'file_url': video_url,
        'is_explicit_share': True
    }
    
    print("[facebook] Initiating upload via URL...")
    response = requests.post(url, params=params)
    
    if response.status_code != 200:
        error_data = response.json() if response.content else {}
        raise Exception(f"Failed to initiate upload: {error_data}")
    
    result = response.json()
    if 'id' not in result:
        raise Exception(f"Unexpected response format: {result}")
    
    video_id = result['id']
    print(f"[facebook] Video created with ID: {video_id}")
    
    # Wait for processing
    print("[facebook] Waiting for video processing...")
    time.sleep(10)  # Give Facebook some time to process
    
    # Check if the video is ready
    check_url = f"https://graph.facebook.com/v24.0/{video_id}"
    check_params = {
        'access_token': access_token,
        'fields': 'status'
    }
    
    max_attempts = 12  # Wait up to 60 seconds
    for attempt in range(max_attempts):
        try:
            check_response = requests.get(check_url, params=check_params)
            if check_response.status_code == 200:
                check_data = check_response.json()
                if 'status' in check_data:
                    status = check_data['status']
                    if 'video_status' in status:
                        video_status = status['video_status']
                        print(f"[facebook] Video status: {video_status}")
                        
                        if video_status in ['ready', 'complete']:
                            print(f"[facebook] ✅ Upload completed successfully!")
                            
                            # Create a post with the video
                            post_url = f"https://graph.facebook.com/v24.0/{page_id}/feed"
                            post_params = {
                                'access_token': access_token,
                                'attached_media[0]': f'{{"media_fbid":"{video_id}"}}',
                                'message': description
                            }
                            
                            post_response = requests.post(post_url, params=post_params)
                            if post_response.status_code == 200:
                                post_result = post_response.json()
                                print(f"[facebook] Posted to feed: {post_result.get('id', 'unknown')}")
                            
                            return {
                                'id': video_id,
                                'status': 'published',
                                'post_url': f'https://www.facebook.com/{page_id}/posts/{post_result.get("id", "unknown")}' if post_response.status_code == 200 else None
                            }
                        elif video_status == 'error':
                            raise Exception(f"Video processing failed: {status}")
        except Exception as e:
            print(f"[facebook] Error checking status: {e}")
        
        time.sleep(5)  # Wait 5 seconds between checks
    
    print(f"[facebook] ⚠️ Max wait time reached, video may still be processing")
    return {
        'id': video_id,
        'status': 'processing',
        'warning': 'Max wait time reached, please check Facebook for final status'
    }


if __name__ == "__main__":
    # Test the function
    import sys
    if len(sys.argv) < 3:
        print("Usage: python upload_facebook.py <video_path> <description>")
        sys.exit(1)
    
    video_path = Path(sys.argv[1])
    description = sys.argv[2]
    
    try:
        result = upload_to_facebook(video_path, description)
        print(f"Success: {result}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
