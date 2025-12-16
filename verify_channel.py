"""
Step 2 (Optional): Verify Which Channel This Token Belongs To

Run this AFTER getting your refresh token to confirm which channel it uploads to.
"""

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os

def verify_channel():
    print("=" * 70)
    print("Verify YouTube Channel")
    print("=" * 70)
    print()
    
    # Get credentials from environment or user input
    client_id = os.getenv("YT_CLIENT_ID") or input("Enter CLIENT_ID: ")
    client_secret = os.getenv("YT_CLIENT_SECRET") or input("Enter CLIENT_SECRET: ")
    refresh_token = os.getenv("YT_REFRESH_TOKEN") or input("Enter REFRESH_TOKEN: ")
    
    print()
    print("🔍 Checking which channel this token belongs to...")
    print()
    
    # Create credentials
    creds = Credentials(
        None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret
    )
    
    # Build YouTube service
    youtube = build("youtube", "v3", credentials=creds)
    
    # Get channel info
    response = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        mine=True
    ).execute()
    
    if response.get("items"):
        channel = response["items"][0]
        snippet = channel["snippet"]
        stats = channel.get("statistics", {})
        
        print("=" * 70)
        print("✅ Channel Found!")
        print("=" * 70)
        print()
        print(f"📺 Channel Name: {snippet['title']}")
        print(f"🔗 Channel ID: {channel['id']}")
        
        if "customUrl" in snippet:
            print(f"🌐 Custom URL: @{snippet['customUrl']}")
        
        print()
        print("📊 Statistics:")
        print(f"   Subscribers: {stats.get('subscriberCount', 'Hidden')}")
        print(f"   Total Views: {stats.get('viewCount', '0')}")
        print(f"   Total Videos: {stats.get('videoCount', '0')}")
        print()
        print("=" * 70)
        print()
        print("✅ This token will upload videos to the channel above!")
        print()
    else:
        print("❌ No channel found for this token")
        print("   Please re-run get_youtube_token.py")

if __name__ == "__main__":
    verify_channel()
