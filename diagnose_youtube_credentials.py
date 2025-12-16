"""
YouTube Credentials Diagnostic Tool

This script tests your YouTube API credentials to identify issues.
It will check:
1. If environment variables are set
2. If credentials are valid format
3. If they can authenticate with Google
4. If they have YouTube upload permissions
"""

import os
import sys
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def check_env_variables():
    """Check if required environment variables are set."""
    print_section("Step 1: Checking Environment Variables")
    
    required_vars = ['YT_CLIENT_ID', 'YT_CLIENT_SECRET', 'YT_REFRESH_TOKEN']
    all_set = True
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Show first/last 10 chars for security
            masked = f"{value[:10]}...{value[-10:]}" if len(value) > 20 else "***"
            print(f"✅ {var}: {masked}")
        else:
            print(f"❌ {var}: NOT SET")
            all_set = False
    
    if not all_set:
        print("\n⚠️  PROBLEM FOUND: Missing environment variables!")
        print("\nTo fix:")
        print("1. Go to GitHub repo → Settings → Secrets → Actions")
        print("2. Make sure all 3 secrets are created:")
        print("   - YT_CLIENT_ID")
        print("   - YT_CLIENT_SECRET")
        print("   - YT_REFRESH_TOKEN")
        return False
    
    print("\n✅ All environment variables are set")
    return True

def check_credential_format():
    """Check if credentials have valid format."""
    print_section("Step 2: Checking Credential Format")
    
    client_id = os.getenv('YT_CLIENT_ID')
    client_secret = os.getenv('YT_CLIENT_SECRET')
    refresh_token = os.getenv('YT_REFRESH_TOKEN')
    
    issues = []
    
    # Check client_id format (should end with .apps.googleusercontent.com)
    if client_id:
        if not client_id.endswith('.apps.googleusercontent.com'):
            issues.append("❌ CLIENT_ID should end with '.apps.googleusercontent.com'")
            print(f"   Current: {client_id[:30]}...")
        else:
            print(f"✅ CLIENT_ID format looks correct")
    
    # Check client_secret format (should start with GOCSPX-)
    if client_secret:
        if not client_secret.startswith('GOCSPX-'):
            issues.append("❌ CLIENT_SECRET should start with 'GOCSPX-'")
            print(f"   Current: {client_secret[:20]}...")
        else:
            print(f"✅ CLIENT_SECRET format looks correct")
    
    # Check refresh_token format (should be long alphanumeric string)
    if refresh_token:
        if len(refresh_token) < 50:
            issues.append("❌ REFRESH_TOKEN seems too short (should be ~100+ chars)")
            print(f"   Current length: {len(refresh_token)}")
        else:
            print(f"✅ REFRESH_TOKEN length looks correct ({len(refresh_token)} chars)")
    
    if issues:
        print("\n⚠️  POTENTIAL PROBLEMS FOUND:")
        for issue in issues:
            print(f"   {issue}")
        print("\nThese credentials might be from an old or invalid OAuth client.")
        print("You may need to regenerate them using: python get_youtube_token.py")
        return False
    
    print("\n✅ All credentials have valid format")
    return True

def test_authentication():
    """Test if credentials can authenticate with Google."""
    print_section("Step 3: Testing Authentication with Google")
    
    client_id = os.getenv('YT_CLIENT_ID')
    client_secret = os.getenv('YT_CLIENT_SECRET')
    refresh_token = os.getenv('YT_REFRESH_TOKEN')
    
    try:
        print("🔄 Creating credentials object...")
        creds = Credentials(
            None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret,
            scopes=["https://www.googleapis.com/auth/youtube.upload"]
        )
        
        print("🔄 Attempting to refresh access token...")
        creds.refresh(Request())
        
        print("✅ Successfully authenticated with Google!")
        print(f"   Access token obtained (expires in ~1 hour)")
        return True
        
    except Exception as e:
        error_str = str(e)
        print(f"❌ Authentication FAILED!")
        print(f"\nError: {error_str}")
        
        # Provide specific guidance based on error
        if "invalid_client" in error_str.lower():
            print("\n⚠️  PROBLEM: OAuth client not found or invalid")
            print("\nThis means:")
            print("  • The CLIENT_ID/CLIENT_SECRET are from a deleted OAuth client")
            print("  • OR they're from a different Google Cloud project")
            print("  • OR they were never valid")
            print("\nTO FIX:")
            print("  1. Run: python get_youtube_token.py")
            print("  2. This will generate NEW valid credentials")
            print("  3. Copy the 3 values to GitHub Secrets")
            
        elif "invalid_grant" in error_str.lower():
            print("\n⚠️  PROBLEM: Refresh token is invalid or expired")
            print("\nThis means:")
            print("  • The REFRESH_TOKEN is old/revoked")
            print("  • OR you revoked access in Google account settings")
            print("\nTO FIX:")
            print("  1. Run: python get_youtube_token.py")
            print("  2. Re-authorize the app")
            print("  3. Copy the new REFRESH_TOKEN to GitHub Secrets")
            
        else:
            print("\n⚠️  Unknown authentication error")
            print("Try regenerating credentials: python get_youtube_token.py")
        
        return False

def test_youtube_api():
    """Test if credentials can access YouTube API."""
    print_section("Step 4: Testing YouTube API Access")
    
    client_id = os.getenv('YT_CLIENT_ID')
    client_secret = os.getenv('YT_CLIENT_SECRET')
    refresh_token = os.getenv('YT_REFRESH_TOKEN')
    
    try:
        print("🔄 Creating YouTube API client...")
        creds = Credentials(
            None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret,
            scopes=["https://www.googleapis.com/auth/youtube.upload"]
        )
        
        creds.refresh(Request())
        youtube = build('youtube', 'v3', credentials=creds)
        
        print("🔄 Testing API access (fetching channel info)...")
        request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            mine=True
        )
        response = request.execute()
        
        if 'items' in response and len(response['items']) > 0:
            channel = response['items'][0]
            print("✅ Successfully connected to YouTube API!")
            print(f"\n📺 Channel Information:")
            print(f"   Name: {channel['snippet']['title']}")
            print(f"   ID: {channel['id']}")
            if 'statistics' in channel:
                print(f"   Subscribers: {channel['statistics'].get('subscriberCount', 'Hidden')}")
                print(f"   Videos: {channel['statistics'].get('videoCount', '0')}")
            print("\n✅ This is the channel where videos will be uploaded!")
            return True
        else:
            print("❌ No channel found for these credentials")
            print("   The account may not have a YouTube channel")
            return False
            
    except HttpError as e:
        print(f"❌ YouTube API Error: {e}")
        if e.resp.status == 403:
            print("\n⚠️  PROBLEM: YouTube Data API not enabled")
            print("\nTO FIX:")
            print("  1. Go to: console.cloud.google.com")
            print("  2. Select your project")
            print("  3. Enable 'YouTube Data API v3'")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Run all diagnostic checks."""
    print("\n" + "=" * 70)
    print("  🔍 YouTube Credentials Diagnostic Tool")
    print("=" * 70)
    print("\nThis will test your YouTube API credentials step-by-step.")
    print("If any step fails, you'll get specific instructions to fix it.")
    
    # Run checks in sequence
    step1 = check_env_variables()
    if not step1:
        print("\n❌ DIAGNOSIS FAILED: Fix environment variables first")
        sys.exit(1)
    
    step2 = check_credential_format()
    # Continue even if format looks wrong - might still work
    
    step3 = test_authentication()
    if not step3:
        print("\n❌ DIAGNOSIS FAILED: Cannot authenticate with Google")
        print("\n🔧 RECOMMENDED ACTION:")
        print("   Run: python get_youtube_token.py")
        print("   Then update your GitHub Secrets with the new values")
        sys.exit(1)
    
    step4 = test_youtube_api()
    if not step4:
        print("\n❌ DIAGNOSIS FAILED: Cannot access YouTube API")
        sys.exit(1)
    
    # All checks passed!
    print_section("✅ ALL CHECKS PASSED!")
    print("\n🎉 Your YouTube credentials are working correctly!")
    print("\nYour setup is ready to upload videos to YouTube.")
    print("The upload script should work now.")
    print("\n" + "=" * 70)

if __name__ == '__main__':
    main()
