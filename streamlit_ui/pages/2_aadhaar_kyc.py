import streamlit as st
import requests
from utils.sidebar import render_sidebar
render_sidebar()

st.title("🔢 Aadhaar Verification")

st.write("Please enter your 12-digit Aadhaar number to begin.")

aadhaar_input = st.text_input("Enter Aadhaar Number", max_chars=12)

if st.button("Send OTP"):
    if len(aadhaar_input) != 12 or not aadhaar_input.isdigit():
        st.error("❌ Invalid Aadhaar number. Must be 12 digits.")
    else:
        with st.spinner("Sending OTP..."):
            try:
                response = requests.post("http://127.0.0.1:5000/kyc", json={"aadhaar_number": aadhaar_input})
                result = response.json()
                if response.status_code == 200:
                    st.success("✅ OTP sent successfully!")
                    st.session_state.aadhaar_number = aadhaar_input
                    st.session_state.otp_received = result.get("otp")
                    st.switch_page("pages/3_otp_verify.py")
                else:
                    st.error(result.get("message", "Unknown error"))
            except Exception as e:
                st.error(f"Error: {e}")
