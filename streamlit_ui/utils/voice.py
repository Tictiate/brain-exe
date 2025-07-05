from gtts import gTTS

def speak(text, lang_code='en', filename='speech.mp3'):
    try:
        tts = gTTS(text=text, lang=lang_code)
        tts.save(filename)
        return filename
    except Exception as e:
        return None
