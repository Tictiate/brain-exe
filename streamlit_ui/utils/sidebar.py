import streamlit as st
# st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Emblem_of_India.svg/240px-Emblem_of_India.svg.png", width=80)

def render_sidebar():
    # st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Emblem_of_India.svg/240px-Emblem_of_India.svg.png", width=60)
    st.sidebar.markdown("### 🛡️ Voice-Backed Insurance Assistant")
    st.sidebar.markdown("---")

    # Show current language if selected
    if "language" in st.session_state:
        st.sidebar.markdown(f"🌐 Language: `{st.session_state.language.upper()}`")

    st.sidebar.markdown("### 🔗 Pages")
    st.sidebar.page_link("app.py", label="🏠 Home")
    st.sidebar.page_link("pages/2_aadhaar_kyc.py", label="🆔 Aadhaar KYC")
    st.sidebar.page_link("pages/3_otp_verify.py", label="🔐 OTP Verification")
    st.sidebar.page_link("pages/1_language_select.py", label="🌐 Select Language")
    st.sidebar.page_link("pages/4_explore_insurance_types.py", label="🔍 Explore Insurance Types")
    # st.sidebar.page_link("pages/4b_insurance_summary.py", label="🧠 AI Insurance Summary")
    st.sidebar.page_link("pages/5_plan_browser.py", label="📄 Browse Plans")
    st.sidebar.page_link("pages/6_submit_claim.py", label="📤 Submit Claim")
    st.sidebar.page_link("pages/7_payment_gateway.py", label="💳 UPI Payment")

    st.sidebar.markdown("---")
    st.sidebar.caption("🎓 Built by team Brain.exe for Inceptia 2025") 