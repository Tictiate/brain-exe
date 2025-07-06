import streamlit as st
import base64
import os
import time
from utils.voice import speak
from utils.sidebar import render_sidebar

render_sidebar()

# 🧠 Init session state
for key in ["played", "start_time", "redirect_ready", "heading_spoken", "came_from_proceed"]:
    st.session_state.setdefault(key, False)
st.session_state.setdefault("start_time", None)

# 🌐 Languages in native script
LANGUAGES = {
    "English": "en",
    "हिन्दी (Hindi)": "hi",
    "मराठी (Marathi)": "mr",
    "தமிழ் (Tamil)": "ta",
    "తెలుగు (Telugu)": "te",
    "ગુજરાતી (Gujarati)": "gu",
    "বাংলা (Bengali)": "bn"
}

# 🔊 Welcome messages
WELCOME_MESSAGES = {
    "en": "Welcome to the insurance assistant!",
    "hi": "बीमा सहायक में आपका स्वागत है!",
    "mr": "विमा सहाय्यामध्ये आपले स्वागत आहे!",
    "ta": "காப்பீட்டு உதவியாளருக்கு வரவேற்கிறோம்!",
    "te": "భీమా సహాయకుడికి స్వాగతం!",
    "gu": "વીમા સહાયકમાં આપનું સ્વાગત છે!",
    "bn": "বীমা সহকারী-তে আপনাকে স্বাগতম!"
}

# 🖼️ UI
st.title("🌐 भाषा चुनें / Select Language")
st.write("कृपया अपनी पसंदीदा भाषा चुनें। / Please choose your preferred language.")

selected_lang_name = st.selectbox("Choose a language", list(LANGUAGES.keys()))
selected_lang_code = LANGUAGES[selected_lang_name]
st.session_state.language = selected_lang_code

# ▶️ Play welcome voice
if st.button("Proceed") and not st.session_state.played:
    st.session_state.came_from_proceed = True
    welcome_text = WELCOME_MESSAGES.get(selected_lang_code, "Welcome!")

    with st.spinner("Generating welcome message..."):
        audio_file = speak(welcome_text, selected_lang_code, filename="welcome.mp3")

    if audio_file and os.path.exists(audio_file):
        with open(audio_file, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
        """, unsafe_allow_html=True)

    st.session_state.played = True
    st.session_state.start_time = time.time()

# ⏱️ Redirect after audio
if st.session_state.came_from_proceed and st.session_state.played and not st.session_state.redirect_ready:
    if time.time() - st.session_state.start_time > 3.5:
        st.session_state.redirect_ready = True
        st.rerun()

if st.session_state.came_from_proceed and st.session_state.redirect_ready:
    st.session_state.came_from_proceed = False
    st.switch_page("pages/4_explore_insurance_types.py")

st.session_state["last_clicked_page"] = "language_select"
