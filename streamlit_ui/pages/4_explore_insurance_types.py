import streamlit as st
import base64
import time
import os
from utils.voice import speak
from utils.sidebar import render_sidebar

render_sidebar()

# 🔁 Reset state if user navigated manually
if st.session_state.get("last_clicked_page") != "explore_insurance":
    for key in ["play_and_redirect", "start_time", "speech_text", 
                "selected_insurance_type", "selected_scheme_name", 
                "last_clicked_label", "button_click_count"]:
        if key in st.session_state:
            del st.session_state[key]

st.session_state["last_clicked_page"] = "explore_insurance"
lang_code = st.session_state.get("language", "en")

# 🌍 Headings in local language
heading_texts = {
    "en": "Select Type of Insurance",
    "hi": "बीमा का प्रकार चुनें",
    "mr": "विमा प्रकार निवडा",
    "ta": "காப்பீட்டு வகையைத் தேர்ந்தெடுக்கவும்",
    "te": "బీమా రకాన్ని ఎంచుకోండి",
    "gu": "વીમા પ્રકાર પસંદ કરો",
    "bn": "বীমার ধরন নির্বাচন করুন"
}
heading = heading_texts.get(lang_code, heading_texts["en"])
st.title(f"🛡️ {heading}")

# 🔊 Speak heading once
if not st.session_state.get("heading_spoken", False):
    audio_file = speak(heading, lang_code, filename="heading.mp3")
    if audio_file and os.path.exists(audio_file):
        with open(audio_file, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
        """, unsafe_allow_html=True)
    st.session_state.heading_spoken = True

# 🔠 Insurance translations
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

# 🧠 Init click tracking
st.session_state.setdefault("last_clicked_label", None)
st.session_state.setdefault("button_click_count", 0)

# 🟢 Render insurance options
translations = INSURANCE_TRANSLATIONS.get(lang_code, INSURANCE_TRANSLATIONS["en"])
for ins_type, scheme in insurance_options.items():
    label = translations.get(ins_type, ins_type)
    if st.button(label):
        if st.session_state.last_clicked_label == label:
            st.session_state.button_click_count += 1
        else:
            st.session_state.last_clicked_label = label
            st.session_state.button_click_count = 1
            st.session_state.speech_text = label
            st.session_state.start_time = time.time()

        # 1st click: Speak only
        if st.session_state.button_click_count == 1:
            audio_file = speak(label, lang_code, filename="ins_choice.mp3")
            if audio_file and os.path.exists(audio_file):
                with open(audio_file, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                st.markdown(f"""
                    <audio autoplay>
                        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                    </audio>
                """, unsafe_allow_html=True)

        # 2nd click: Redirect
        elif st.session_state.button_click_count == 2:
            st.session_state.selected_insurance_type = ins_type
            st.session_state.selected_scheme_name = scheme
            st.session_state.button_click_count = 0
            st.switch_page("pages/4b_insurance_summary.py")
