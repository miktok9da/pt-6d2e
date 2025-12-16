"""
Alternative: Manual OAuth Flow (No Local Server)

Use this if get_youtube_token.py doesn't work due to port/firewall issues.
"""

from google_auth_oauthlib.flow import InstalledAppFlow
import json

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def main():
    print("=" * 70)
    print("YouTube Authentication - Manual Method")
    print("=" * 70)
    print()
    print("This method doesn't require a local server.")
    print()
    
    # Create flow
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secrets.json",
        SCOPES
    )
    
    # Get authorization URL
    auth_url, _ = flow.authorization_url(prompt='consent')
    
    print("=" * 70)
    print("STEP 1: Open this URL in your browser:")
    print("=" * 70)
    print()
    print(auth_url)
    print()
    print("=" * 70)
    print("STEP 2: After you authorize:")
    print("=" * 70)
    print()
    print("1. You'll be redirected to a URL that starts with:")
    print("   http://localhost/?state=...")
    print()
    print("2. The page will show an error (that's OK!)")
    print()
    print("3. COPY THE ENTIRE URL from your browser address bar")
    print()
    print("=" * 70)
    
    # Get the authorization response
    redirect_url = input("\nPaste the FULL redirect URL here: ").strip()
    
    # Exchange code for credentials
    flow.fetch_token(authorization_response=redirect_url)
    creds = flow.credentials
    
    print()
    print("=" * 70)
    print("✅ SUCCESS! Here are your credentials:")
    print("=" * 70)
    print()
    print(f"YT_CLIENT_ID: {creds.client_id}")
    print()
    print(f"YT_CLIENT_SECRET: {creds.client_secret}")
    print()
    print(f"YT_REFRESH_TOKEN: {creds.refresh_token}")
    print()
    print("=" * 70)
    print("Add these 3 values to GitHub Secrets!")
    print("=" * 70)
    
    # Save to file
    token_data = {
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "refresh_token": creds.refresh_token
    }
    
    with open("youtube_credentials.json", "w") as f:
        json.dump(token_data, f, indent=2)
    
    print()
    print("💾 Also saved to: youtube_credentials.json")
    print()

if __name__ == "__main__":
    main()
