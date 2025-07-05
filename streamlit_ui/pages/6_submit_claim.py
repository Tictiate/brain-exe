import streamlit as st
import requests
import json
from utils.sidebar import render_sidebar
render_sidebar()

st.title("📤 Submit Insurance Claim")

with st.form("claim_form", clear_on_submit=True):
    aadhaar = st.text_input("🔢 Aadhaar Number", max_chars=12)
    photo = st.file_uploader("📸 Upload Photo (JPEG/PNG)", type=["jpg", "jpeg", "png"])
    submitted = st.form_submit_button("🚀 Submit Claim")

    if submitted:
        if not aadhaar or len(aadhaar) != 12 or not aadhaar.isdigit():
            st.warning("❌ Please enter a valid 12-digit Aadhaar number.")
        elif not photo:
            st.warning("❌ Please upload a photo.")
        else:
            try:
                files = {"photo": photo}
                response = requests.post("http://127.0.0.1:5000/submit-claim", files=files)
                result = response.json()

                if result["status"] == "success":
                    st.success(result["message"])
                    st.markdown("### 🔍 Extracted EXIF Metadata:")
                    st.json(result["exif"])
                else:
                    st.error(result["message"])
            except Exception as e:
                st.error("🚨 Backend error or connection failed.")
                st.code(str(e))

