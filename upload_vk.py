"""
Upload videos to VK (VKontakte) using vk_api library
This method is MUCH easier and handles OAuth automatically!
"""
import os
import vk_api
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def upload_to_vk(video_path, title="", description=""):
    """
    Upload video to VK community using vk_api library
    
    This is the EASY way - vk_api handles all the complex OAuth stuff!
    
    Args:
        video_path: Path to video file
        title: Video title
        description: Video description/caption
        
    Returns:
        dict: Upload result with video_id and post_id
    """
    # Get credentials from environment
    access_token = os.getenv('VK_ACCESS_TOKEN')
    group_id = os.getenv('VK_GROUP_ID')
    
    if not access_token:
        raise ValueError("VK_ACCESS_TOKEN not found in environment variables")
    if not group_id:
        raise ValueError("VK_GROUP_ID not found in environment variables")
    
    # Ensure group_id is positive for vk_api (it handles the negative conversion)
    group_id_clean = str(group_id).lstrip('-')
    group_id_int = int(group_id_clean)
    
    print(f"🇷🇺 Starting VK upload using vk_api...")
    print(f"📁 Video: {video_path}")
    print(f"👥 Group ID: {group_id}")
    
    try:
        # Initialize VK session
        print("\n🔑 Initializing VK session...")
        vk_session = vk_api.VkApi(token=access_token)
        vk = vk_session.get_api()
        upload = vk_api.VkUpload(vk_session)
        
        # Prepare message
        message = description if description else "🏛️ História das Mulheres Antigas!\n\n#HistoriaDasMulheres #MulheresNaHistoria #Educacao #Cultura"

        # Ensure message is not empty (VK requirement)
        if not message.strip():
            message = "🏛️ Novo vídeo!"

        # Upload video to community
        print("\n📤 Uploading video to VK...")
        print("⏳ This may take a few minutes depending on video size...")
        
        # vk_api handles everything: getting upload URL, uploading file, and saving
        video = upload.video(
            video_file=str(video_path),
            name=title or 'História das Mulheres Antigas',
            description=description[:220] if description else '',  # VK 220 char limit
            group_id=group_id_int,
            wallpost=0  # Don't auto-post, we'll do it manually
        )
        
        print(f"✅ Video uploaded successfully!")
        print(f"📹 Video ID: {video['video_id']}")
        print(f"👤 Owner ID: {video['owner_id']}")
        
        # Post video to community wall
        print("\n📝 Posting to community wall...")
        
        attachment = f"video{video['owner_id']}_{video['video_id']}"
        
        post_result = vk.wall.post(
            owner_id=-group_id_int,  # Negative for community
            from_group=1,  # Post on behalf of community
            message=message,
            attachments=attachment
        )
        
        post_id = post_result['post_id']
        post_url = f"https://vk.com/wall-{group_id_int}_{post_id}"
        
        print(f"✅ Posted to wall successfully!")
        print(f"📌 Post ID: {post_id}")
        print(f"🔗 View post: {post_url}")
        
        result = {
            'success': True,
            'video_id': video['video_id'],
            'owner_id': video['owner_id'],
            'post_id': post_id,
            'post_url': post_url,
            'message': 'Video uploaded and posted to VK successfully'
        }
        
        print(f"\n🎉 VK Upload Complete!")
        
        return result
        
    except vk_api.exceptions.ApiError as e:
        error_msg = f"VK API Error: {e}"
        print(f"\n❌ {error_msg}")
        
        # Provide helpful error messages
        if "Access denied" in str(e):
            print("\n💡 Solution:")
            print("   Your token doesn't have the required permissions.")
            print("   You need a USER token with 'video', 'wall', and 'groups' permissions.")
            print("   See VK_SIMPLE_SOLUTION.md for the easiest way to get this!")
        
        raise Exception(error_msg)
        
    except FileNotFoundError:
        raise Exception(f"Video file not found: {video_path}")
        
    except Exception as e:
        raise Exception(f"Failed to upload to VK: {e}")


def main():
    """Test VK upload"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python upload_vk.py <video_path> [title] [description]")
        sys.exit(1)
    
    video_path = sys.argv[1]
    title = sys.argv[2] if len(sys.argv) > 2 else "História das Mulheres Antigas"
    description = sys.argv[3] if len(sys.argv) > 3 else "🏛️ História das Mulheres Antigas!"
    
    try:
        result = upload_to_vk(video_path, title, description)
        print("\n✅ Success!")
        print(f"Post URL: {result['post_url']}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()