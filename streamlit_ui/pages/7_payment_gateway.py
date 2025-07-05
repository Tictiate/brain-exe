import streamlit as st
import os
import sys

# Enable import from the backend folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.razorpay_payment import create_payment_link

st.title("💳 UPI Payment via Razorpay")

st.markdown("Fill in your details and you’ll be redirected to Razorpay’s payment page.")

# Input fields
name = st.text_input("Your Name")
email = st.text_input("Email")
amount = st.number_input("Amount (INR)", min_value=1, value=100)

if st.button("Proceed to Razorpay"):
    if not name or not email:
        st.warning("⚠ Please enter both your name and email.")
        st.stop()

    # Generate Razorpay Payment Link
    payment_url = create_payment_link(amount, name, email)

    # Show success message and manual fallback link
    st.success("✅ Redirecting you to Razorpay...")
    st.markdown(f"[Click here if you are not redirected automatically]({payment_url})", unsafe_allow_html=True)

    # Automatically redirect after 1 second
    st.markdown(f"""
        <meta http-equiv="refresh" content="1; url={payment_url}">
    """, unsafe_allow_html=True)