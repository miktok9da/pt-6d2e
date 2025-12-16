"""
Display GitHub Secrets Values

Shows the exact values to copy to GitHub Secrets.
"""

import json

# Load credentials
with open('youtube_credentials.json', 'r') as f:
    creds = json.load(f)

print("=" * 70)
print("COPY THESE VALUES TO GITHUB SECRETS")
print("=" * 70)
print()
print("Go to: GitHub repo -> Settings -> Secrets -> Actions")
print()
print("Create or update these 3 secrets:")
print()
print("-" * 70)
print("1. Secret Name: YT_CLIENT_ID")
print("   Value:")
print(creds['client_id'])
print()
print("-" * 70)
print("2. Secret Name: YT_CLIENT_SECRET")
print("   Value:")
print(creds['client_secret'])
print()
print("-" * 70)
print("3. Secret Name: YT_REFRESH_TOKEN")
print("   Value:")
print(creds['refresh_token'])
print()
print("=" * 70)
print("After adding these, your GitHub Actions will upload to YouTube!")
print("=" * 70)
