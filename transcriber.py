import whisper
import os


def transcribe_audio(audio_path: str, model_size: str = "base"):
    if not os.path.exists(audio_path):
        print(f"[ERROR] Audio file not found at {audio_path}")
        return ""
    try:
        model = whisper.load_model(model_size)
        result = model.transcribe(audio_path, fp16=False)
        return result["text"]
    except Exception as e:
        print(f"[ERROR] Transcription failed: {e}")
        return ""
