import streamlit as st
from utils.sidebar import render_sidebar
from utils.ai import get_insurance_summary
from utils.firebase import get_user_profile
from utils.tts_stt import speak, listen
import firebase_admin
from firebase_admin import credentials, firestore
from utils.tts_stt import speak, listen


st.set_page_config(page_title="Chat with AI", page_icon="🤖")
render_sidebar()
st.title("🤖 Insurance Chatbot Advisor")

# --- Get user profile from Firebase ---
if "user_id" not in st.session_state:
    st.warning("User not found. Please fill the survey first.")
    st.stop()

if not firebase_admin._apps:
    cred = credentials.Certificate("firebaseKey.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

user_id = st.session_state["user_id"]
doc = db.collection("users").document(user_id).get()

if not doc.exists:
    st.error("User data not found in Firebase.")
    st.stop()

user_data = doc.to_dict()

# --- Get selected insurance type ---
selected_type = st.session_state.get("selected_insurance_type", None)
if not selected_type:
    st.warning("Please select an insurance type from the Explore page.")
    st.stop()

st.markdown(f"### 💼 You are exploring: **{selected_type}** insurance")

# --- Build system prompt ---
def build_prompt(user_data, ins_type, user_query=None):
    base = f"""
You are an expert insurance advisor helping Indian citizens select the best government insurance schemes.

Here is the user's profile:
👤 Name: {user_data.get('name')}
🎂 Age: {user_data.get('age')}
🚻 Gender: {user_data.get('gender')}
💍 Marital Status: {user_data.get('marital_status')}
👔 Occupation: {user_data.get('occupation')}
🏭 Work Sector: {user_data.get('sector')}
💵 Income: ₹{user_data.get('income')}
🧾 Income Proof: {user_data.get('income_proof')}
🩺 Health Issues: {user_data.get('health_issues')}
💼 Existing Insurance: {user_data.get('has_existing_insurance')}
📄 Existing Insurance Type: {user_data.get('existing_insurance_type')}
🎯 Preferred Premium: ₹{user_data.get('preferred_premium')}
🎯 Preferred Coverage: ₹{user_data.get('preferred_coverage')}
💰 Payout Expectation: {user_data.get('payout_expectations')}

The user is interested in **{ins_type} Insurance**.
Explain government schemes in simple Hindi and English. Mention:
- Eligibility
- Premium
- Coverage
- Claim process
"""

    if user_query:
        base += f"\nUser also asked: \"{user_query}\". Answer that as well."

    return base.strip()

# --- Chat Interface ---
st.markdown("### 🗣️ Ask your question")
mode = st.radio("Select input mode:", ["🧠 Type", "🎙️ Voice"])

if mode == "🧠 Type":
    question = st.text_input("Ask a question about this scheme:")
    if st.button("Ask AI"):
        prompt = build_prompt(user_data, selected_type, question)
        with st.spinner("Thinking..."):
            reply = get_insurance_summary(prompt)
        if reply:
            st.success(reply)
            speak(reply)
else:
    if st.button("🎤 Start Voice Chat"):
        with st.spinner("Listening..."):
            user_voice_input = listen()
            st.info(f"🗣️ You said: {user_voice_input}")
            prompt = build_prompt(user_data, selected_type, user_voice_input)
            reply = get_insurance_summary(prompt)
        if reply:
            st.success(reply)
            speak(reply)
