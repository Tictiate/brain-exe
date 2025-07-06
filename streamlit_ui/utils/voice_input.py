import whisper
import sounddevice as sd
import numpy as np
import tempfile
import scipy.io.wavfile

# Load model only once
model = whisper.load_model("base")  # or "small", "medium", "large"

def record_audio(duration=5, fs=44100):
    print("🎙️ Recording...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    print("✅ Recording done.")

    # Save to temp file
    temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    scipy.io.wavfile.write(temp_wav.name, fs, audio)
    return temp_wav.name

def transcribe_audio(file_path):
    print("🧠 Transcribing...")
    result = model.transcribe(file_path)
    return result.get("text", "")
