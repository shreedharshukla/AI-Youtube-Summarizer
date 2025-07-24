import os
from dotenv import load_dotenv
from youtube_agent import search_youtube, download_audio
from transcriber import transcribe_audio
from summarizer import custom_summarize_gemini

# Load environment variables from a .env file at the start
load_dotenv()


def main():
    """
    Main function to orchestrate the AI YouTube Summarizer application.
    It handles user input, API key validation, and the workflow of
    searching, downloading, transcribing, and summarizing.
    """
    print("--- AI YouTube Summarizer ---")

    # 1. Get API keys from environment variables
    youtube_api_key = os.getenv("YOUTUBE_API_KEY")
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    if not youtube_api_key or not gemini_api_key:
        print("\n❌ Error: API keys for YouTube and/or Gemini are not set.")
        print("Please create a .env file in the project root and add your keys:")
        print("YOUTUBE_API_KEY='your_key_here'")
        print("GEMINI_API_KEY='your_key_here'")
        return

    # 2. Get user input for topic and instruction
    topic = input(
        "\nEnter the topic for the YouTube video you want to summarize: ")
    if not topic.strip():
        print("Topic cannot be empty.")
        return

    instruction = input(
        "Enter the summarization instruction (e.g., 'Summarize for a beginner'): ")
    if not instruction.strip():
        print("Instruction cannot be empty.")
        return

    try:
        # 3. Search for the video on YouTube
        video_url, video_title = search_youtube(topic, youtube_api_key)
        if not video_url:
            return  # search_youtube will print its own error

        # 4. Download the audio from the video
        audio_path = "temp_audio.mp3"
        downloaded_audio_path = download_audio(video_url, audio_path)
        if not downloaded_audio_path:
            return  # download_audio will print its own error

        # 5. Transcribe the audio to text
        print("\n🎤 Transcribing audio... This may take a few moments depending on video length.")
        transcript = transcribe_audio(downloaded_audio_path, model_size="base")
        if not transcript:
            print("❌ Transcription failed. Could not extract text from the audio.")
            return
        print("✅ Transcription complete.")

        # 6. Generate the custom summary using the transcript
        summary = custom_summarize_gemini(
            transcript, instruction, gemini_api_key)

        # 7. Print the final results
        print("\n" + "="*60)
        print(f"🎥 Video Title: {video_title}")
        print(f"🔗 URL: {video_url}")
        print("\n📝 Summary:")
        print(summary)
        print("="*60)

    finally:
        # 8. Clean up the downloaded audio file to save space
        if os.path.exists("temp_audio.mp3"):
            os.remove("temp_audio.mp3")
            print(f"\n🗑️ Temporary audio file 'temp_audio.mp3' has been removed.")


if __name__ == "__main__":
    main()
