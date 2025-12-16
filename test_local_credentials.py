"""
Test YouTube Credentials from youtube_credentials.json

This script tests credentials stored locally in youtube_credentials.json
(This is what you should have after running get_youtube_token.py)
"""

import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def main():
    print("\n" + "=" * 70)
    print("  🔍 Testing Local YouTube Credentials")
    print("=" * 70)
    
    # Check if youtube_credentials.json exists
    creds_file = Path("youtube_credentials.json")
    
    if not creds_file.exists():
        print("\n❌ File 'youtube_credentials.json' not found!")
        print("\nThis file should be created by running: python get_youtube_token.py")
        print("\nDo you want to:")
        print("  1. Run get_youtube_token.py to create credentials")
        print("  2. Check if client_secrets.json exists")
        
        # Check for client_secrets.json
        if Path("client_secrets.json").exists():
            print("\n✅ Found client_secrets.json")
            print("   You can run: python get_youtube_token.py")
        else:
            print("\n❌ client_secrets.json also not found!")
            print("   Follow instructions in GET_CLIENT_SECRETS.md")
        
        return
    
    # Load credentials
    print_section("Step 1: Loading Credentials from File")
    try:
        with open(creds_file, 'r') as f:
            creds_data = json.load(f)
        
        client_id = creds_data.get('client_id')
        client_secret = creds_data.get('client_secret')
        refresh_token = creds_data.get('refresh_token')
        
        print("✅ Successfully loaded credentials file")
        print(f"   CLIENT_ID: {client_id[:30]}...")
        print(f"   CLIENT_SECRET: {client_secret[:20]}...")
        print(f"   REFRESH_TOKEN: {refresh_token[:30]}...")
        
    except Exception as e:
        print(f"❌ Error reading credentials file: {e}")
        return
    
    # Test authentication
    print_section("Step 2: Testing Authentication")
    try:
        print("🔄 Creating credentials object...")
        creds = Credentials(
            None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret,
            scopes=["https://www.googleapis.com/auth/youtube"]
        )
        
        print("🔄 Refreshing access token...")
        creds.refresh(Request())
        
        print("✅ Successfully authenticated with Google!")
        
    except Exception as e:
        error_str = str(e)
        print(f"❌ Authentication FAILED!")
        print(f"\nError: {error_str}")
        
        if "invalid_client" in error_str.lower():
            print("\n⚠️  PROBLEM: OAuth client is invalid")
            print("\nYour client_secrets.json might be from:")
            print("  • A deleted OAuth client in Google Cloud Console")
            print("  • A different Google Cloud project")
            print("\nTO FIX:")
            print("  1. Go to GET_CLIENT_SECRETS.md")
            print("  2. Follow steps to create NEW OAuth client")
            print("  3. Download new client_secrets.json")
            print("  4. Run: python get_youtube_token.py")
            
        elif "invalid_grant" in error_str.lower():
            print("\n⚠️  PROBLEM: Refresh token is invalid")
            print("\nTO FIX:")
            print("  Run: python get_youtube_token.py")
        
        return
    
    # Test YouTube API
    print_section("Step 3: Testing YouTube API Access")
    try:
        print("🔄 Building YouTube API client...")
        youtube = build('youtube', 'v3', credentials=creds)
        
        print("🔄 Fetching your YouTube channel info...")
        request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            mine=True
        )
        response = request.execute()
        
        if 'items' in response and len(response['items']) > 0:
            channel = response['items'][0]
            print("✅ Successfully connected to YouTube!")
            print(f"\n📺 Your YouTube Channel:")
            print(f"   Name: {channel['snippet']['title']}")
            print(f"   ID: {channel['id']}")
            if 'statistics' in channel:
                stats = channel['statistics']
                print(f"   Subscribers: {stats.get('subscriberCount', 'Hidden')}")
                print(f"   Videos: {stats.get('videoCount', '0')}")
                print(f"   Views: {stats.get('viewCount', '0')}")
            
            print("\n✅ Videos will upload to THIS channel!")
            
        else:
            print("❌ No YouTube channel found")
            print("   Make sure the Google account has a YouTube channel")
            return
            
    except HttpError as e:
        print(f"❌ YouTube API Error: {e}")
        if e.resp.status == 403:
            print("\n⚠️  YouTube Data API v3 is not enabled")
            print("\nTO FIX:")
            print("  1. Go to: console.cloud.google.com")
            print("  2. Enable 'YouTube Data API v3'")
        return
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # All tests passed - show GitHub Secrets
    print_section("✅ ALL TESTS PASSED!")
    print("\n🎉 Your local credentials are working!")
    print("\n📋 Copy these to GitHub Secrets:")
    print("\nGo to: GitHub repo → Settings → Secrets → Actions")
    print("\nCreate these 3 secrets:\n")
    
    print("1. Name: YT_CLIENT_ID")
    print(f"   Value: {client_id}")
    print()
    
    print("2. Name: YT_CLIENT_SECRET")
    print(f"   Value: {client_secret}")
    print()
    
    print("3. Name: YT_REFRESH_TOKEN")
    print(f"   Value: {refresh_token}")
    print()
    
    print("=" * 70)
    print("After adding these secrets, your GitHub Actions will work!")
    print("=" * 70)

if __name__ == '__main__':
    main()
