"""
Twitter/X Upload Script

Uploads videos to Twitter/X using Twitter API v2.

Requirements:
- Twitter Developer Account with Elevated access ($100/month for video uploads)
- TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET
"""

import os
from pathlib import Path
import tweepy

def upload_to_twitter(video_file, caption):
    """Upload video to Twitter/X using API v2."""
    
    api_key = os.getenv('TWITTER_API_KEY')
    api_secret = os.getenv('TWITTER_API_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_secret = os.getenv('TWITTER_ACCESS_SECRET')
    
    if not all([api_key, api_secret, access_token, access_secret]):
        raise ValueError(
            "Missing Twitter credentials! Set these environment variables:\n"
            "  - TWITTER_API_KEY\n"
            "  - TWITTER_API_SECRET\n"
            "  - TWITTER_ACCESS_TOKEN\n"
            "  - TWITTER_ACCESS_SECRET\n"
            "\nNote: Requires Twitter API Elevated access (~$100/month) for video uploads"
        )
    
    print("[twitter] Uploading to Twitter/X...")
    
    # Authenticate with Twitter API v1.1 for media upload
    auth = tweepy.OAuth1UserHandler(
        api_key, api_secret,
        access_token, access_secret
    )
    api_v1 = tweepy.API(auth)
    
    # Authenticate with Twitter API v2 for posting
    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_secret
    )
    
    # Upload video (uses v1.1 API)
    print("[twitter] Uploading video...")
    media = api_v1.media_upload(
        filename=str(video_file),
        media_category='tweet_video'
    )
    
    print(f"[twitter] Video uploaded, media_id: {media.media_id}")
    
    # Create tweet with video (uses v2 API)
    print("[twitter] Posting tweet...")
    
    # Twitter has 280 character limit
    tweet_text = caption[:280] if len(caption) > 280 else caption
    
    response = client.create_tweet(
        text=tweet_text,
        media_ids=[media.media_id]
    )
    
    tweet_id = response.data['id']
    
    print(f"[twitter] ✅ Posted to Twitter! Tweet ID: {tweet_id}")
    print(f"[twitter] URL: https://twitter.com/i/web/status/{tweet_id}")
    
    return {
        'id': tweet_id,
        'url': f"https://twitter.com/i/web/status/{tweet_id}",
        'platform': 'twitter'
    }

def main():
    """Test upload to Twitter."""
    video_file = Path('output/final_video.mp4')
    
    if not video_file.exists():
        print("[twitter] ❌ No video found at output/final_video.mp4")
        return
    
    # Read story for caption
    story_file = Path('output/story.txt')
    if story_file.exists():
        story = story_file.read_text(encoding='utf-8')
        # Create short caption for Twitter
        first_sentence = story.split('.')[0] if '.' in story else story[:200]
        caption = f"{first_sentence}... 🏛️\n\n#История #ДревниеЖенщины"
    else:
        caption = "История древних женщин 🏛️ #История #ДревниеЖенщины"
    
    try:
        upload_to_twitter(video_file, caption)
    except Exception as e:
        print(f"[twitter] ❌ Upload failed: {e}")
        raise

if __name__ == '__main__':
    main()
