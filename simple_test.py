"""
Simple YouTube Upload Test

This will attempt a minimal YouTube API call to see the exact error.
"""

import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Load credentials
with open('youtube_credentials.json', 'r') as f:
    creds_data = json.load(f)

# Create credentials
creds = Credentials(
    None,
    refresh_token=creds_data['refresh_token'],
    token_uri="https://oauth2.googleapis.com/token",
    client_id=creds_data['client_id'],
    client_secret=creds_data['client_secret'],
    scopes=["https://www.googleapis.com/auth/youtube"]
)

print("Refreshing token...")
creds.refresh(Request())
print("✅ Token refreshed successfully")
print(f"Access token: {creds.token[:50]}...")

print("\nBuilding YouTube client...")
youtube = build('youtube', 'v3', credentials=creds)

print("\nAttempting API call...")
try:
    request = youtube.channels().list(
        part="snippet",
        mine=True
    )
    response = request.execute()
    print("✅ SUCCESS!")
    print(f"Response: {json.dumps(response, indent=2)}")
    
except HttpError as e:
    print(f"\n❌ HTTP Error {e.resp.status}")
    print(f"Error details: {e.error_details}")
    print(f"\nFull error:")
    print(e)
    
except Exception as e:
    print(f"\n❌ Error: {type(e).__name__}")
    print(f"Message: {e}")
