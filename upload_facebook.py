"""
Facebook Reels Upload

Facebook Graph API for uploading Reels to Facebook Page.
"""

import os
import requests

def upload_to_facebook(video_file, description):
    """Upload video to Facebook Reels."""
    
    access_token = os.getenv('FB_ACCESS_TOKEN')
    page_id = os.getenv('FB_PAGE_ID')
    
    if not access_token or not page_id:
        raise ValueError("Missing FB_ACCESS_TOKEN or FB_PAGE_ID")
    
    print(f"[facebook] Uploading: {video_file}")
    
    # Upload video
    url = f"https://graph.facebook.com/v18.0/{page_id}/videos"
    
    with open(video_file, 'rb') as f:
        files = {'file': f}
        data = {
            'access_token': access_token,
            'description': description,
            'title': 'История древних женщин',
            'is_explicit_share': True
        }
        
        response = requests.post(url, files=files, data=data)
        response.raise_for_status()
    
    video_id = response.json()['id']
    print(f"[facebook] ✅ Uploaded! Video ID: {video_id}")
    
    return {'id': video_id}
