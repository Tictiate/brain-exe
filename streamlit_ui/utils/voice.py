from gtts import gTTS
import tempfile
import os
import streamlit as st

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
