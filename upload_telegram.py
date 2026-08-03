"""
Upload video to Telegram channel
"""
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def upload_to_telegram(video_path, caption):
    """
    Upload video to Telegram channel
    """
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    channel_id = os.getenv('TELEGRAM_CHANNEL_ID')
    
    if not bot_token or not channel_id:
        print("[telegram] Skipping: Missing credentials. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHANNEL_ID")
        return None
    
    # Telegram API endpoint
    url = f"https://api.telegram.org/bot{bot_token}/sendVideo"
    
    # Prepare the video file
    try:
        with open(video_path, 'rb') as video_file:
            files = {
                'video': video_file
            }
            
            data = {
                'chat_id': channel_id,
                'caption': caption,
                'parse_mode': 'HTML'
            }
            
            print(f"[telegram] Uploading to Telegram channel: {channel_id}")
            response = requests.post(url, files=files, data=data, timeout=300)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    print(f"✅ Successfully uploaded to Telegram!")
                    return result
                else:
                    raise Exception(f"Telegram API error: {result.get('description')}")
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
    except Exception as e:
        print(f"[telegram] ❌ Failed: {e}")
        return None

if __name__ == "__main__":
    # Test upload
    test_video = Path("output") / "final_video.mp4"
    if test_video.exists():
        try:
            result = upload_to_telegram(
                str(test_video),
                "Test video upload to Telegram"
            )
            print(f"Upload result: {result}")
        except Exception as e:
            print(f"Failed: {e}")
    else:
        print("No test video found")
