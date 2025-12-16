"""
Verify Project Configuration

This checks if your client_secrets.json and the enabled APIs
are in the same Google Cloud project.
"""

import json
from pathlib import Path

def main():
    print("\n" + "=" * 70)
    print("  🔍 Project Configuration Check")
    print("=" * 70)
    
    # Read client_secrets.json
    secrets_file = Path("client_secrets.json")
    if not secrets_file.exists():
        print("\n❌ client_secrets.json not found")
        return
    
    with open(secrets_file, 'r') as f:
        secrets = json.load(f)
    
    project_id = secrets.get('installed', {}).get('project_id')
    client_id = secrets.get('installed', {}).get('client_id')
    
    print(f"\n📋 OAuth Client Configuration:")
    print(f"   Project ID: {project_id}")
    print(f"   Client ID: {client_id}")
    
    print(f"\n🔍 What to verify in Google Cloud Console:")
    print(f"\n1. Go to: https://console.cloud.google.com/")
    print(f"2. Make sure you select project: {project_id}")
    print(f"3. Go to: APIs & Services → Enabled APIs")
    print(f"4. Verify 'YouTube Data API v3' is in the list")
    print(f"\n5. Go to: APIs & Services → Credentials")
    print(f"6. Look for OAuth 2.0 Client ID: {client_id[:30]}...")
    print(f"7. Make sure it exists and is type 'Desktop app'")
    
    print(f"\n⚠️  IMPORTANT:")
    print(f"   If the YouTube Data API v3 is enabled in a DIFFERENT project,")
    print(f"   that's the problem! You need to either:")
    print(f"   A) Enable the API in project: {project_id}")
    print(f"   B) Create new OAuth credentials in the project where API is enabled")
    
    print("\n" + "=" * 70)
    print("  🔧 Quick Test: Try Publishing the App")
    print("=" * 70)
    
    print(f"\nSince your test user is already added, try this:")
    print(f"\n1. Go to: https://console.cloud.google.com/apis/credentials/consent")
    print(f"2. Select project: {project_id}")
    print(f"3. Click 'PUBLISH APP' button")
    print(f"4. Confirm the warning")
    print(f"5. Re-run: python get_youtube_token.py")
    
    print(f"\nPublishing removes some restrictions and might fix the issue.")
    print(f"It's safe for personal use - you'll just see a warning when authorizing.")

if __name__ == '__main__':
    main()
