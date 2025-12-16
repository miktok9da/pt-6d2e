"""
Step 1: Get YouTube Refresh Token

This script will:
1. Open your browser
2. Ask you to login to Google
3. Ask you to SELECT which YouTube channel to upload to
4. Generate a refresh token for THAT specific channel

IMPORTANT: The channel you select here is where ALL videos will upload!

Run this script ONCE per YouTube channel you want to upload to.
"""

from google_auth_oauthlib.flow import InstalledAppFlow
import json

# YouTube full scope (includes upload + read channel info)
SCOPES = ["https://www.googleapis.com/auth/youtube"]

def main():
    print("=" * 70)
    print("YouTube Authentication - Get Refresh Token")
    print("=" * 70)
    print()
    print("📋 Before running:")
    print("   1. Make sure you have 'client_secrets.json' in this folder")
    print("   2. This will open your browser")
    print("   3. You'll login to Google")
    print("   4. You'll SELECT which YouTube channel to use")
    print()
    print("⚠️  IMPORTANT: The channel you select = where videos upload!")
    print()
    input("Press ENTER to continue...")
    print()
    
    # Start OAuth flow
    print("🌐 Opening browser for authentication...")
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secrets.json",
        SCOPES
    )
    
    # This opens the browser and waits for user to authenticate
    creds = flow.run_local_server(port=8080)
    
    print()
    print("=" * 70)
    print("✅ SUCCESS! Authentication complete")
    print("=" * 70)
    print()
    print("📝 Your credentials (copy these to GitHub Secrets):")
    print()
    print(f"CLIENT_ID: {creds.client_id}")
    print(f"CLIENT_SECRET: {creds.client_secret}")
    print(f"REFRESH_TOKEN: {creds.refresh_token}")
    print()
    print("=" * 70)
    print("📋 Next Steps:")
    print("=" * 70)
    print()
    print("1. Go to your GitHub repo → Settings → Secrets → Actions")
    print()
    print("2. Create these 3 secrets:")
    print()
    print("   Name: YT_CLIENT_ID")
    print(f"   Value: {creds.client_id}")
    print()
    print("   Name: YT_CLIENT_SECRET")
    print(f"   Value: {creds.client_secret}")
    print()
    print("   Name: YT_REFRESH_TOKEN")
    print(f"   Value: {creds.refresh_token}")
    print()
    print("3. Push your code to GitHub")
    print()
    print("4. The workflow will automatically upload to the channel you selected!")
    print()
    print("=" * 70)
    
    # Also save to a file for reference
    token_data = {
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "refresh_token": creds.refresh_token
    }
    
    with open("youtube_credentials.json", "w") as f:
        json.dump(token_data, f, indent=2)
    
    print()
    print("💾 Credentials also saved to: youtube_credentials.json")
    print("   (Keep this file PRIVATE - don't commit to GitHub!)")
    print()

if __name__ == "__main__":
    main()
