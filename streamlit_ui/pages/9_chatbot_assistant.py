import streamlit as st
from utils.sidebar import render_sidebar
from utils.ai import get_insurance_summary
from utils.firebase import store_survey_response, get_latest_survey_by_user
import firebase_admin
from firebase_admin import credentials, firestore
from utils.voice_input import record_audio, transcribe_audio

render_sidebar()
st.title("🤖 Insurance Chatbot Advisor")

# ✅ Firebase init
if not firebase_admin._apps:
    cred = credentials.Certificate("firebaseKey.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()


user_id = st.session_state.get("user_id")
if not user_id:
    st.warning("User not found. Please fill the survey first.")
    st.stop()


docs = db.collection("user_survey_responses")\
    .where("user_id", "==", user_id)\
    .order_by("timestamp", direction=firestore.Query.DESCENDING)\
    .limit(1).stream()

user_data = next(docs, None)
if not user_data or not user_data.exists:
    st.error("Survey data not found.")
    st.stop()

user_data = user_data.to_dict()

# ✅ Recommendation Prompt
prompt = f"""You are an expert insurance advisor.
Suggest the best insurance schemes for the following profile:

👤 {user_data['name']}, {user_data['age']} y/o, {user_data['gender']}, {user_data['marital_status']}
👪 Dependents: {user_data['dependents']}
💼 Occupation: {user_data['occupation']} ({user_data['sector']})
💵 Income: ₹{user_data['income']} (Proof: {user_data['has_income_proof']})
🩺 Health: {user_data['health_conditions'] or 'None'}
✅ Existing: {user_data['has_existing_insurance']} - {', '.join(user_data['insurance_type']) if user_data['insurance_type'] else 'None'}
🎯 Preferences: Coverage = {', '.join(user_data['preferred_coverage'])}, Premium ≤ ₹{user_data['preferred_premium']}
🏁 Payout: {user_data['payout_expectation']}, Priority: {user_data['priority']}

List relevant **government schemes**, with eligibility, premium, coverage, and claim process in simple Hindi and English.
"""

with st.spinner("Generating recommendations..."):
    initial_reply = get_insurance_summary(prompt)
    st.success(initial_reply)
    # speak(initial_reply)

# ✅ Chat mode
st.markdown("### 🗣️ Ask follow-up questions")
mode = st.radio("Choose input mode:", ["💬 Text", "🎙️ Voice"])

if mode == "💬 Text":
    q = st.text_input("Your question")
    if st.button("Ask AI"):
        followup = get_insurance_summary(f"{prompt}\nFollow-up: {q}")
        st.success(followup)
        # speak(followup)
else:
    if st.button("🎤 Start Voice Chat"):
        with st.spinner("Listening..."):
            try:
                file_path = record_audio(duration=5)
                q = transcribe_audio(file_path)
                st.info(f"🗣️ You said: {q}")
                followup = get_insurance_summary(f"{prompt}\nFollow-up: {q}")
                st.success(followup)
                # speak(followup)
            except Exception as e:
                st.error(f"Voice input failed: {e}")