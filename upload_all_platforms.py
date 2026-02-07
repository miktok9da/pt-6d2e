"""
Multi-Platform Upload Script

Uploads videos to:
- YouTube Shorts
- Instagram Reels
- TikTok
- Facebook Reels

Each platform requires its own API credentials.
"""

import os
from pathlib import Path
import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import platform-specific uploaders
from upload_to_youtube import upload_to_youtube
from upload_instagram import upload_to_instagram
from upload_tiktok import upload_to_tiktok
from upload_facebook import upload_to_facebook
from upload_threads import upload_to_threads
from upload_twitter import upload_to_twitter
from upload_vk import upload_to_vk
from upload_telegram import upload_to_telegram

def main():
    """Upload video to all configured platforms."""
    video_file = Path('output/final_video.mp4')
    
    if not video_file.exists():
        print("[upload] ❌ No video found at output/final_video.mp4")
        return
    
    # Read story for metadata
    story_file = Path('output/story.txt')
    if story_file.exists():
        story = story_file.read_text(encoding='utf-8')
        # Use first sentence as title
        title_parts = story.split('.')
        title = title_parts[0][:100] if title_parts else "História das mulheres antigas"
    else:
        title = f"História das mulheres antigas - {datetime.date.today()}"
    
    # Portuguese description - topic-relevant, no AI mentions
    description = f"""Descubra a história fascinante das mulheres nas civilizações antigas.

Explore as leis, os costumes, as tradições e as figuras emblemáticas que marcaram a história.

#Shorts #HistóriaDasMulheres #HistóriaAntiga #Educação"""
    
    tags = [
        'História', 'Mulheres antigas', 'Fatos históricos',
        'Shorts', 'Reels', 'Educação', 'Cultura'
    ]
    
    # Debug: Show which credentials are detected
    print("\n" + "="*60)
    print("🔍 CREDENTIAL DETECTION STATUS")
    print("="*60)
    print(f"YouTube: {'✅' if all([os.getenv('YT_CLIENT_ID'), os.getenv('YT_CLIENT_SECRET'), os.getenv('YT_REFRESH_TOKEN')]) else '❌'}")
    print(f"Instagram: {'✅' if (all([os.getenv('IG_ACCESS_TOKEN'), os.getenv('IG_USER_ID')]) or all([os.getenv('INSTAGRAM_ACCESS_TOKEN'), os.getenv('INSTAGRAM_ACCOUNT_ID')])) else '❌'}")
    print(f"Facebook: {'✅' if all([os.getenv('FB_ACCESS_TOKEN'), os.getenv('FB_PAGE_ID')]) or all([os.getenv('FACEBOOK_ACCESS_TOKEN'), os.getenv('FACEBOOK_PAGE_ID')]) else '❌'}")
    print(f"Threads: {'✅' if all([os.getenv('THREADS_ACCESS_TOKEN'), os.getenv('THREADS_USER_ID')]) else '❌'}")
    print(f"TikTok: {'✅' if os.getenv('TIKTOK_ACCESS_TOKEN') else '❌'}")
    print(f"Twitter: {'✅' if all([os.getenv('TWITTER_API_KEY'), os.getenv('TWITTER_API_SECRET'), os.getenv('TWITTER_ACCESS_TOKEN')]) else '❌'}")
    print(f"VK: {'✅' if (os.getenv('VK_ACCESS_TOKEN') and os.getenv('VK_GROUP_ID')) else '❌'}")
    print(f"Telegram: {'✅' if (os.getenv('TELEGRAM_BOT_TOKEN') and os.getenv('TELEGRAM_CHANNEL_ID')) else '❌'}")
    print("="*60)
    
    results = {}
    
    # Upload to YouTube
    if all([
        os.getenv('YT_CLIENT_ID'),
        os.getenv('YT_CLIENT_SECRET'),
        os.getenv('YT_REFRESH_TOKEN')
    ]):
        print("\n" + "="*60)
        print("📺 Uploading to YouTube...")
        print("="*60)
        try:
            result = upload_to_youtube(video_file, title, description, tags)
            results['youtube'] = result
            print(f"✅ YouTube: https://youtube.com/shorts/{result['id']}")
        except Exception as e:
            print(f"❌ YouTube failed: {e}")
            results['youtube'] = None
    else:
        print("⏭️  Skipping YouTube (credentials not set)")
    
    # Upload to Instagram
    if (os.getenv('IG_ACCESS_TOKEN') and os.getenv('IG_USER_ID')) or \
       (os.getenv('INSTAGRAM_ACCESS_TOKEN') and os.getenv('INSTAGRAM_ACCOUNT_ID')):
        print("\n" + "="*60)
        print("📸 Uploading to Instagram...")
        print("="*60)
        try:
            result = upload_to_instagram(video_file, description)
            results['instagram'] = result
            if result:
                print(f"✅ Instagram: Uploaded successfully")
        except Exception as e:
            print(f"❌ Instagram failed: {e}")
            results['instagram'] = None
    else:
        print("⏭️  Skipping Instagram (credentials not set)")
    
    # Upload to TikTok
    if os.getenv('TIKTOK_ACCESS_TOKEN'):
        print("\n" + "="*60)
        print("🎵 Uploading to TikTok...")
        print("="*60)
        try:
            result = upload_to_tiktok(video_file, title, description)
            results['tiktok'] = result
            if result:
                print(f"✅ TikTok: Uploaded successfully")
        except Exception as e:
            print(f"❌ TikTok failed: {e}")
            results['tiktok'] = None
    else:
        print("⏭️  Skipping TikTok (credentials not set)")
    
    # Upload to Facebook
    if (os.getenv('FB_ACCESS_TOKEN') and os.getenv('FB_PAGE_ID')) or \
       (os.getenv('FACEBOOK_ACCESS_TOKEN') and os.getenv('FACEBOOK_PAGE_ID')):
        print("\n" + "="*60)
        print("📘 Uploading to Facebook...")
        print("="*60)
        try:
            result = upload_to_facebook(video_file, description)
            results['facebook'] = result
            if result:
                print(f"✅ Facebook: Uploaded successfully")
        except Exception as e:
            print(f"❌ Facebook failed: {e}")
            results['facebook'] = None
    else:
        print("⏭️  Skipping Facebook (credentials not set)")
    
    # Upload to Threads
    if all([
        os.getenv('THREADS_ACCESS_TOKEN'),
        os.getenv('THREADS_USER_ID')
    ]):
        print("\n" + "="*60)
        print("🧵 Uploading to Threads...")
        print("="*60)
        try:
            result = upload_to_threads(video_file, description)
            results['threads'] = result
            if result:
                print(f"✅ Threads: Uploaded successfully")
        except Exception as e:
            print(f"❌ Threads failed: {e}")
            results['threads'] = None
    else:
        print("⏭️  Skipping Threads (credentials not set)")
    
    # Upload to Twitter/X
    if all([
        os.getenv('TWITTER_API_KEY'),
        os.getenv('TWITTER_API_SECRET'),
        os.getenv('TWITTER_ACCESS_TOKEN'),
        os.getenv('TWITTER_ACCESS_SECRET')
    ]):
        print("\n" + "="*60)
        print("🐦 Uploading to Twitter/X...")
        print("="*60)
        try:
            result = upload_to_twitter(video_file, description)
            results['twitter'] = result
            if result:
                print(f"✅ Twitter: Uploaded successfully")
        except Exception as e:
            print(f"❌ Twitter failed: {e}")
            results['twitter'] = None
    else:
        print("⏭️  Skipping Twitter (credentials not set)")
    
    # Upload to VK
    if all([
        os.getenv('VK_ACCESS_TOKEN'),
        os.getenv('VK_GROUP_ID')
    ]):
        print("\n" + "="*60)
        print("🔵 Uploading to VK...")
        print("="*60)
        try:
            # VK often needs description and then title as third arg
            result = upload_to_vk(video_file, title, description)
            results['vk'] = result
            if result:
                print(f"✅ VK: Uploaded successfully")
        except Exception as e:
            print(f"❌ VK failed: {e}")
            results['vk'] = None
    else:
        print("⏭️  Skipping VK (credentials not set)")
    # Upload to Telegram
    if os.getenv('TELEGRAM_BOT_TOKEN') and os.getenv('TELEGRAM_CHANNEL_ID'):
        print("\n" + "="*60)
        print("✈️ Uploading to Telegram...")
        print("="*60)
        try:
            result = upload_to_telegram(video_file, description)
            results['telegram'] = result
            if result:
                print(f"✅ Telegram: Uploaded successfully")
        except Exception as e:
            print(f"❌ Telegram failed: {e}")
            results['telegram'] = None
    else:
        print("⏭️  Skipping Telegram (credentials not set)")
    
    # Summary
    print("\n" + "="*60)
    print("📊 Upload Summary")
    print("="*60)
    for platform, result in results.items():
        status = "✅ Success" if result else "❌ Failed"
        print(f"{platform.capitalize()}: {status}")
    print("="*60)

if __name__ == '__main__':
    main()
