import streamlit as st
from utils.sidebar import render_sidebar

render_sidebar()

st.title("✅ OTP Verification")

# Check if OTP was generated
if "otp_received" not in st.session_state:
    st.warning("🔒 No OTP sent yet. Please complete Aadhaar KYC first.")
    st.stop()

st.write("Please enter the OTP sent to your registered mobile number.")

# OTP Input
user_otp = st.text_input("Enter OTP", max_chars=6)

# Verify Button
if st.button("Verify OTP"):
    if user_otp == str(st.session_state.otp_received):
        st.success("✅ OTP Verified Successfully!")
        st.session_state.kyc_verified = True
        st.write("You can now proceed to explore insurance plans.")
        st.balloons()
    else:
        st.error("❌ Incorrect OTP. Please try again.")






































# import streamlit as st
# import requests
# from utils.sidebar import render_sidebar
# render_sidebar()

# st.title("🔐 Verify OTP")

# if "aadhaar_number" not in st.session_state:
#     st.warning("Aadhaar not found in session. Please go back to 'Aadhaar Verification' page first.")
# else:
#     aadhaar = st.session_state.aadhaar_number
#     st.write(f"Verifying for Aadhaar: **{aadhaar}**")

#     user_otp = st.text_input("Enter OTP received", max_chars=6)

#     if st.button("Verify OTP"):
#         if not user_otp or len(user_otp) != 6 or not user_otp.isdigit():
#             st.error("❌ Enter a valid 6-digit OTP.")
#         else:
#             with st.spinner("Verifying..."):
#                 try:
#                     response = requests.post("http://127.0.0.1:5000/verify-otp", json={
#                         "aadhaar_number": aadhaar,
#                         "otp": user_otp
#                     })

#                     result = response.json()
#                     if response.status_code == 200:
#                         st.success("✅ OTP Verified Successfully!")
#                         st.session_state.otp_verified = True
#                         st.write("You can now proceed to Plan Selection ➡️")
#                     else:
#                         st.error(f"❌ {result.get('message', 'Verification failed')}")
#                 except Exception as e:
#                     st.error(f"Error connecting to server: {e}")
