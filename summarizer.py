import google.generativeai as genai


def custom_summarize_gemini(transcript: str, instruction: str, api_key: str):
    print("🤖 Configuring Gemini and generating custom summary...")
    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        print(f"❌ Error configuring Gemini: {e}")
        return "Sorry, there was an issue setting up the API key."
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Instruction: {instruction}\n\nTranscript:\n\"\"\"\n{transcript}\n\"\"\"\n\nSummary:"
    try:
        response = model.generate_content(prompt)
        print("✅ Custom summary generated.")
        return response.text
    except Exception as e:
        error_message = str(e)
        if "API key not valid" in error_message:
            return "Sorry, the provided Gemini API key is not valid. Please check the key and try again."
        print(f"❌ Error generating summary with Gemini: {e}")
        return "Sorry, I couldn't generate the summary."
