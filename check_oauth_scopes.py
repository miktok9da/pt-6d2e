"""
Advanced OAuth Diagnostic - Check Scopes and Permissions

This script will show exactly what scopes your credentials have
and what permissions are missing.
"""

import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import requests

def main():
    print("\n" + "=" * 70)
    print("  🔍 Advanced OAuth Diagnostic")
    print("=" * 70)
    
    # Load credentials
    creds_file = Path("youtube_credentials.json")
    if not creds_file.exists():
        print("\n❌ youtube_credentials.json not found")
        return
    
    with open(creds_file, 'r') as f:
        creds_data = json.load(f)
    
    client_id = creds_data['client_id']
    client_secret = creds_data['client_secret']
    refresh_token = creds_data['refresh_token']
    
    print("\n📋 Loaded Credentials:")
    print(f"   Client ID: {client_id[:40]}...")
    print(f"   Refresh Token: {refresh_token[:40]}...")
    
    # Create credentials and refresh
    print("\n🔄 Refreshing access token...")
    creds = Credentials(
        None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=["https://www.googleapis.com/auth/youtube.upload"]
    )
    
    try:
        creds.refresh(Request())
        access_token = creds.token
        print("✅ Got access token!")
        
        # Check what scopes this token actually has
        print("\n🔍 Checking token scopes...")
        token_info_url = f"https://oauth2.googleapis.com/tokeninfo?access_token={access_token}"
        response = requests.get(token_info_url)
        
        if response.status_code == 200:
            token_info = response.json()
            print("\n📊 Token Information:")
            print(f"   Issued to: {token_info.get('email', 'N/A')}")
            print(f"   Expires in: {token_info.get('expires_in', 'N/A')} seconds")
            
            scopes = token_info.get('scope', '').split()
            print(f"\n🔐 Granted Scopes ({len(scopes)}):")
            for scope in scopes:
                print(f"   ✓ {scope}")
            
            # Check if we have the YouTube upload scope
            required_scope = "https://www.googleapis.com/auth/youtube.upload"
            if required_scope in scopes:
                print(f"\n✅ Has required scope: {required_scope}")
            else:
                print(f"\n❌ MISSING required scope: {required_scope}")
                print("\n⚠️  PROBLEM: The OAuth consent didn't grant YouTube upload permission!")
                print("\nPossible causes:")
                print("  1. You clicked 'Deny' for YouTube access during authorization")
                print("  2. The OAuth consent screen doesn't have YouTube scopes enabled")
                print("  3. Your Google account doesn't have a YouTube channel")
                
            # Check if we have YouTube readonly (which would indicate partial auth)
            if "https://www.googleapis.com/auth/youtube.readonly" in scopes:
                print("\n⚠️  You have readonly access but not upload access")
                print("   Re-run authorization and make sure to grant ALL permissions")
                
        else:
            print(f"❌ Failed to get token info: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Try to make a simple API call
    print("\n" + "=" * 70)
    print("  Testing YouTube API Call")
    print("=" * 70)
    
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    
    try:
        youtube = build('youtube', 'v3', credentials=creds)
        
        # Try to get channel info
        print("\n🔄 Attempting to fetch channel info...")
        request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            mine=True
        )
        response = request.execute()
        
        if 'items' in response and len(response['items']) > 0:
            channel = response['items'][0]
            print("✅ SUCCESS! API call worked!")
            print(f"\n📺 Channel: {channel['snippet']['title']}")
            print(f"   ID: {channel['id']}")
        else:
            print("❌ No channel found")
            
    except HttpError as e:
        print(f"❌ API Error: {e}")
        print(f"\n🔍 Error Details:")
        print(f"   Status: {e.resp.status}")
        print(f"   Reason: {e.error_details}")
        
        if e.resp.status == 403:
            print("\n⚠️  403 Forbidden - Possible Issues:")
            print("   1. YouTube Data API v3 not enabled in the CORRECT project")
            print("   2. OAuth client is from a DIFFERENT project than where API is enabled")
            print("   3. Quota exceeded (unlikely for first use)")
            print("   4. OAuth consent screen needs test users added")
            
            print("\n🔧 SOLUTION:")
            print("   1. Go to: https://console.cloud.google.com/")
            print("   2. Make sure you're in project: youtube-automation-481003")
            print("   3. Go to: APIs & Services → OAuth consent screen")
            print("   4. Add your Gmail to 'Test users'")
            print("   5. Go to: APIs & Services → Enabled APIs")
            print("   6. Verify 'YouTube Data API v3' is enabled")
            print("   7. Re-run: python get_youtube_token.py")

if __name__ == '__main__':
    main()
