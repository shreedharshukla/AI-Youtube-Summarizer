import os
from googleapiclient.discovery import build
import yt_dlp


def search_youtube(topic: str, api_key: str):
    print(f"🤖 Searching YouTube for videos on '{topic}'...")
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.search().list(
            part='snippet', q=topic, type='video', order='relevance', maxResults=1
        )
        response = request.execute()
        if not response['items']:
            print("😔 No videos found on this topic.")
            return None, None
        video_id = response['items'][0]['id']['videoId']
        video_title = response['items'][0]['snippet']['title']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"✅ Found video: '{video_title}'")
        return video_url, video_title
    except Exception as e:
        print(f"❌ Error searching YouTube. Please ensure your YouTube API key is correct and the API is enabled.")
        return None, None


def download_audio(video_url: str, output_path: str = "temp_audio.mp3"):
    print(f"📥 Downloading audio...")
    if os.path.exists(output_path):
        os.remove(output_path)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
        'outtmpl': output_path.replace('.mp3', ''),
        'quiet': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print("✅ Audio downloaded successfully.")
        return output_path
    except Exception as e:
        print(f"❌ Error downloading audio: {e}")
        return None
