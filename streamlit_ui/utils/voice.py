from gtts import gTTS
import tempfile
import os
import streamlit as st

<<<<<<< HEAD
def speak(text):
    try:
        tts = gTTS(text=text, lang='en')
        tts.save("speech.mp3")
        return "speech.mp3"
    except Exception as e:
        print(f"[gTTS ERROR] {e}")
        return None
=======
def speak(text, lang_code="en", filename=None):
    tts = gTTS(text=text, lang=lang_code)

    if filename:
        tts.save(filename)
        return filename
    else:
        # Use temp file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)
        return temp_file.name
>>>>>>> 2c6f632cc5dd94e48aba54978b08353b2a4eab07
