import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils.sidebar import render_sidebar
render_sidebar()

st.set_page_config(
    page_title="Voice-Backed Insurance Assistant",
    page_icon="💬",
    layout="centered"
)

st.markdown("<h1 style='text-align: center;'>💬 Voice-Backed Insurance Assistant</h1>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; font-size: 16px;'>
Welcome to an AI-powered platform to explore, understand, and claim government insurance schemes — in your own language.
</div>
""", unsafe_allow_html=True)

st.markdown("### 🚀 Get Started")

st.info("Use the sidebar to navigate through the steps.")

if st.button("🔓 Start KYC"):
    st.switch_page("pages/2_aadhaar_kyc.py")

