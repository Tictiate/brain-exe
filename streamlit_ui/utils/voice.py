from gtts import gTTS

def speak(text):
    try:
        tts = gTTS(text=text, lang='en')
        tts.save("speech.mp3")
        return "speech.mp3"
    except Exception as e:
        print(f"[gTTS ERROR] {e}")
        return None
