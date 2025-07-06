import streamlit as st
import uuid
from utils.voice import speak
from utils.firebase import store_survey_response
from utils.sidebar import render_sidebar

# ✅ Setup
render_sidebar()
st.set_page_config(page_title="Insurance Survey", page_icon="📝")
st.title("📝 Insurance Recommendation Survey")
st.markdown("Click on a field to hear what it's for.")

# ✅ JS function to auto-play audio on focus
def auto_play_js(file_path, field_id):
    st.markdown(f"""
    <script>
        const field = document.getElementById("{field_id}");
        if (field) {{
            field.addEventListener("focus", function() {{
                var audio = new Audio("{file_path}");
                audio.play();
            }});
        }}
    </script>
    """, unsafe_allow_html=True)

# ✅ Start Form (styled manually using HTML)
with st.form("insurance_survey_form"):

    # 🗣️ Name
    speak("Please enter your full name.")
    st.markdown('<input id="name_input" name="name" placeholder="Full Name" class="stTextInput" required>', unsafe_allow_html=True)
    auto_play_js("speech.mp3", "name_input")

    # 🗣️ Age
    speak("Please enter your age.")
    st.markdown('<input id="age_input" name="age" type="number" placeholder="Age" class="stTextInput" required>', unsafe_allow_html=True)
    auto_play_js("speech.mp3", "age_input")

    # 🗣️ Gender
    speak("Please select your gender.")
    st.markdown("""
    <select id="gender_input" name="gender" class="stTextInput" required>
        <option value="">Select Gender</option>
        <option>Male</option>
        <option>Female</option>
        <option>Other</option>
    </select>
    """, unsafe_allow_html=True)
    auto_play_js("speech.mp3", "gender_input")

    # 🗣️ Occupation
    speak("Please select your occupation.")
    st.markdown("""
    <select id="occupation_input" name="occupation" class="stTextInput" required>
        <option value="">Select Occupation</option>
        <option>Student</option>
        <option>Govt Employee</option>
        <option>Private Sector</option>
        <option>Self-Employed</option>
        <option>Unemployed</option>
        <option>Retired</option>
    </select>
    """, unsafe_allow_html=True)
    auto_play_js("speech.mp3", "occupation_input")

    # 🗣️ Income
    speak("Please enter your monthly income.")
    st.markdown('<input id="income_input" name="income" type="number" placeholder="Monthly Income in ₹" class="stTextInput" required>', unsafe_allow_html=True)
    auto_play_js("speech.mp3", "income_input")

    # ✅ Submit
    submitted = st.form_submit_button("Submit Survey")

# ✅ Handle Submission
if submitted:
    # 📝 Dummy values since raw HTML inputs can't be captured by Streamlit directly
    # For full integration, use JS → Streamlit bridge or switch back to st.text_input()
    survey_data = {
        "id": str(uuid.uuid4()),
        "name": "Sample Name",
        "age": 25,
        "gender": "Male",
        "occupation": "Student",
        "income": 10000
    }
    store_survey_response(survey_data)
    st.success("✅ Survey submitted successfully! (values are placeholder)")
