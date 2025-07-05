import streamlit as st
import requests
from utils.sidebar import render_sidebar
render_sidebar()

st.title("🛡️ Insurance Plans")

if "aadhaar_number" not in st.session_state or "otp_verified" not in st.session_state:
    st.warning("Please complete Aadhaar and OTP verification first.")
    st.stop()

aadhaar = st.session_state.aadhaar_number

# Fetch plans
try:
    response = requests.get("http://127.0.0.1:5000/plans")
    if response.status_code == 200:
        plans = response.json().get("plans", [])
    else:
        st.error("Failed to load plans from server.")
        st.stop()
except Exception as e:
    st.error(f"Server error: {e}")
    st.stop()

st.write("Choose a plan that best suits your needs:")

# Show plans as cards with radio buttons
plan_ids = [plan["plan_id"] for plan in plans]
plan_names = {plan["plan_id"]: plan["name"] for plan in plans}
plan_details = {plan["plan_id"]: plan for plan in plans}

selected_plan_id = st.radio(
    "Available Plans:",
    options=plan_ids,
    format_func=lambda pid: f"{plan_names[pid]} — ₹{plan_details[pid]['weekly_premium']} / week"
)

# Show selected plan description
if selected_plan_id:
    st.markdown(f"**Coverage:** {plan_details[selected_plan_id]['coverage']}")
    st.markdown(f"**Claim Process:** {plan_details[selected_plan_id]['claim_process']}")

if st.button("Confirm Plan"):
    with st.spinner("Submitting your plan..."):
        try:
            response = requests.post("http://127.0.0.1:5000/select-plan", json={
                "user_id": aadhaar,
                "plan_id": selected_plan_id
            })
            if response.status_code == 200:
                st.success("✅ Plan selected successfully!")
                st.write("You may now proceed to Submit Claim →")
            else:
                result = response.json()
                st.error(f"❌ {result.get('message', 'Unknown error')}")
        except Exception as e:
            st.error(f"Error submitting plan: {e}")

