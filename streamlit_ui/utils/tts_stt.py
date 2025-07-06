# streamlit_ui/utils/tts_stt.py

from gtts import gTTS
import tempfile
import os
import pygame
import openai
import speech_recognition as sr

# ✅ Text-to-Speech
def speak(text, lang="hi"):
    tts = gTTS(text=text, lang=lang)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        tts.save(f.name)
        pygame.mixer.init()
        pygame.mixer.music.load(f.name)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        os.remove(f.name)

# ✅ Speech-to-Text using Whisper
def listen():
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        print("🎙️ Speak now...")
        audio = r.listen(source)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio.get_wav_data())
        f_path = f.name

    try:
        audio_file = open(f_path, "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript["text"]
    except Exception as e:
        return "Sorry, couldn't understand."