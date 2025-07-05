import streamlit as st
from utils.voice import speak
from utils.sidebar import render_sidebar
import base64
import os
import time

render_sidebar()
# Reset if user manually navigated here
if not st.session_state.get("came_from_proceed", False):
    st.session_state.played = False
    st.session_state.start_time = None
    st.session_state.redirect_ready = False


LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr",
    "Tamil": "ta",
    "Telugu": "te",
    "Gujarati": "gu",
    "Bengali": "bn"
}

WELCOME_MESSAGES = {
    "en": "Welcome to the insurance assistant!",
    "hi": "बीमा सहायक में आपका स्वागत है!",
    "mr": "विमा सहाय्यामध्ये आपले स्वागत आहे!",
    "ta": "காப்பீட்டு உதவியாளருக்கு வரவேற்கிறோம்!",
    "te": "భీమా సహాయకుడికి స్వాగతం!",
    "gu": "વીમા સહાયકમાં આપનું સ્વાગત છે!",
    "bn": "বীমা সহকারী-তে আপনাকে স্বাগতম!"
}

# 🟢 Setup session state
if "played" not in st.session_state:
    st.session_state.played = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "redirect_ready" not in st.session_state:
    st.session_state.redirect_ready = False

st.title("🌐 Select Language")
st.write("Please choose your preferred language.")

selected_lang_name = st.selectbox("Choose a language", list(LANGUAGES.keys()))
selected_lang_code = LANGUAGES[selected_lang_name]
st.session_state.language = selected_lang_code

# Button press: play audio once
if st.button("Proceed") and not st.session_state.played:
    st.session_state.came_from_proceed = True
    welcome_text = WELCOME_MESSAGES.get(selected_lang_code, "Welcome!")
    audio_file = speak(welcome_text, selected_lang_code, filename="welcome_speech.mp3")
    
    # Encode audio for autoplay
    with open(audio_file, "rb") as f:
        audio_bytes = f.read()
    b64 = base64.b64encode(audio_bytes).decode()
    st.markdown(f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
    """, unsafe_allow_html=True)

    # Mark that audio was played and store timestamp
    st.session_state.played = True
    st.session_state.start_time = time.time()

# Delay-based redirect logic (after rerun)
if st.session_state.played and not st.session_state.redirect_ready:
    elapsed = time.time() - st.session_state.start_time
    if elapsed > 3.5:
        st.session_state.redirect_ready = True
        st.rerun()

# Finally redirect after flag is set
if st.session_state.redirect_ready:
    st.session_state.came_from_proceed = False
    st.switch_page("pages/4_explore_insurance_types.py")

st.session_state["last_clicked_page"] = "language_select"  # Or whatever that page is
