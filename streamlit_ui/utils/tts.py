# utils/tts.py
from gtts import gTTS
import os

def speak(text, lang='en', filename='response.mp3'):
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)
    return filename  # So you can play it using st.audio
