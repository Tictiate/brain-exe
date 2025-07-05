import streamlit as st
import base64
import time
import os
from utils.voice import speak
from utils.sidebar import render_sidebar

render_sidebar()

# Detect manual navigation (user did NOT come here by pressing an insurance button)
manual_nav = (
    st.session_state.get("play_and_redirect", False)
    and "last_clicked_page" in st.session_state
    and st.session_state["last_clicked_page"] != "explore_insurance"
)

# Reset redirect flags if navigated manually
if manual_nav:
    st.session_state.play_and_redirect = False
    st.session_state.start_time = None
    st.session_state.speech_text = None
    st.session_state.selected_insurance_type = None
    st.session_state.selected_scheme_name = None

# Mark that we're now on this page
st.session_state["last_clicked_page"] = "explore_insurance"

# Get selected language
lang = st.session_state.get("language", "en")
INSURANCE_TRANSLATIONS = {
    "en": {
        "Health Insurance": "Health Insurance",
        "Life Insurance": "Life Insurance",
        "Crop Insurance": "Crop Insurance",
        "Livestock Insurance": "Livestock Insurance",
        "Vehicle Insurance": "Vehicle Insurance",
        "Disability Insurance": "Disability Insurance",
        "Travel Insurance": "Travel Insurance",
        "Home Insurance": "Home Insurance"
    },
    "hi": {
        "Health Insurance": "स्वास्थ्य बीमा",
        "Life Insurance": "जीवन बीमा",
        "Crop Insurance": "फसल बीमा",
        "Livestock Insurance": "पशुधन बीमा",
        "Vehicle Insurance": "वाहन बीमा",
        "Disability Insurance": "विकलांगता बीमा",
        "Travel Insurance": "यात्रा बीमा",
        "Home Insurance": "गृह बीमा"
    },
    "mr": {
        "Health Insurance": "आरोग्य विमा",
        "Life Insurance": "जीवन विमा",
        "Crop Insurance": "पिक विमा",
        "Livestock Insurance": "पशुधन विमा",
        "Vehicle Insurance": "वाहन विमा",
        "Disability Insurance": "अपंगत्व विमा",
        "Travel Insurance": "प्रवास विमा",
        "Home Insurance": "गृह विमा"
    },
    "ta": {
        "Health Insurance": "சுகாதார காப்பீடு",
        "Life Insurance": "வாழ்க்கை காப்பீடு",
        "Crop Insurance": "பயிர் காப்பீடு",
        "Livestock Insurance": "மாடுகள் காப்பீடு",
        "Vehicle Insurance": "வாகன காப்பீடு",
        "Disability Insurance": "ஊனமுற்றோர் காப்பீடு",
        "Travel Insurance": "பயண காப்பீடு",
        "Home Insurance": "வீட்டு காப்பீடு"
    },
    "te": {
        "Health Insurance": "ఆరోగ్య బీమా",
        "Life Insurance": "జీవన బీమా",
        "Crop Insurance": "పంట బీమా",
        "Livestock Insurance": "పశుసంవర్ధక బీమా",
        "Vehicle Insurance": "వాహన బీమా",
        "Disability Insurance": "వికలాంగుల బీమా",
        "Travel Insurance": "ప్రయాణ బీమా",
        "Home Insurance": "గృహ బీమా"
    },
    "gu": {
        "Health Insurance": "આરોગ્ય વીમા",
        "Life Insurance": "જીવન વીમા",
        "Crop Insurance": "પાક વીમા",
        "Livestock Insurance": "પશુપાલન વીમા",
        "Vehicle Insurance": "વાહન વીમા",
        "Disability Insurance": "અપંગતા વીમા",
        "Travel Insurance": "મુસાફરી વીમા",
        "Home Insurance": "ઘર વીમા"
    },
    "bn": {
        "Health Insurance": "স্বাস্থ্য বীমা",
        "Life Insurance": "জীবন বীমা",
        "Crop Insurance": "শস্য বীমা",
        "Livestock Insurance": "পশুপালন বীমা",
        "Vehicle Insurance": "যানবাহন বীমা",
        "Disability Insurance": "প্রতিবন্ধী বীমা",
        "Travel Insurance": "ভ্রমণ বীমা",
        "Home Insurance": "বাড়ির বীমা"
    }
}


insurance_options = {
    "Health Insurance": "Ayushman Bharat - PMJAY",
    "Life Insurance": "Pradhan Mantri Jeevan Jyoti Bima Yojana",
    "Crop Insurance": "Pradhan Mantri Fasal Bima Yojana",
    "Livestock Insurance": "Livestock Insurance Scheme",
    "Vehicle Insurance": "Pradhan Mantri Suraksha Bima Yojana",
    "Disability Insurance": "National Disability Insurance Scheme",
    "Travel Insurance": "Bharat Gaurav Scheme",
    "Home Insurance": "Griha Aadhar Yojana"
}

lang_code = st.session_state.get("language", "en")

# Title
st.title("🛡️ Select Type of Insurance")

if "language" not in st.session_state:
    st.warning("Language not selected. Returning to language selection page...")
    st.switch_page("language_select")

lang = st.session_state.language
translations = INSURANCE_TRANSLATIONS.get(lang, INSURANCE_TRANSLATIONS["en"])


# Step 1: Check and setup state
if "play_and_redirect" not in st.session_state:
    st.session_state.play_and_redirect = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None

# Step 2: Display all insurance buttons
for ins_type, scheme in insurance_options.items():
    label = translations.get(ins_type, ins_type)
    if st.button(label) and not st.session_state.play_and_redirect:
        st.session_state.selected_insurance_type = ins_type
        st.session_state.selected_scheme_name = scheme
        st.session_state.speech_text = label
        st.session_state.play_and_redirect = True
        st.session_state.start_time = time.time()
        st.rerun()

# Step 3: If button clicked previously, play and redirect
if st.session_state.play_and_redirect:
    # Generate and play audio
    audio_file = speak(st.session_state.speech_text, lang_code, filename="ins_choice.mp3")
    if audio_file and os.path.exists(audio_file):
        with open(audio_file, "rb") as f:
            audio_bytes = f.read()
        b64 = base64.b64encode(audio_bytes).decode()
        st.markdown(f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
        """, unsafe_allow_html=True)

    # Check timer
    if time.time() - st.session_state.start_time > 2.5:
        st.session_state.play_and_redirect = False
        st.switch_page("pages/4b_insurance_summary.py")

