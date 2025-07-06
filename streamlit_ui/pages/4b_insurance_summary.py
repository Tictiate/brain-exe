import streamlit as st
from utils.sidebar import render_sidebar
from utils.static_data import insurance_descriptions
from utils.ai import get_insurance_summary


render_sidebar()

# Language + selected insurance type
lang = st.session_state.get("language", "en")
ins_type = st.session_state.get("selected_insurance_type", "Health Insurance")
selected_type = st.session_state.get("selected_insurance_type", None)
scheme = st.session_state.get("selected_scheme_name", None)

if not selected_type or not scheme:
    st.warning("Please select an insurance type from the previous page first.")
    st.stop()

# Get static data for selected type in current language
info = insurance_descriptions.get(lang, insurance_descriptions["en"]).get(selected_type)

if info:
    st.subheader(f"🛡️ {info['scheme']}")
    st.write(f"💰 **Premium**: {info['premium']}")
    st.write(f"✅ **Eligibility**: {info['eligibility']}")
    st.write(f"📦 **Coverage**: {info['coverage']}")
else:
    st.error("No scheme data available for this insurance type.")

# Static summary
st.title("📘 Insurance Scheme Details")

prompt = f"Explain the '{scheme}' insurance scheme in simple {lang}. Highlight eligibility, benefits, and how to claim. Give it in a friendly, easy-to-understand manner and keep it concise."

summary_key = f"summary_{ins_type}_{lang}"

if summary_key not in st.session_state:
    with st.spinner("🧠 Generating summary..."):
        ai_summary = get_insurance_summary(prompt)
        st.session_state[summary_key] = ai_summary

st.markdown("### 💬 Summary (AI):")
st.info(st.session_state[summary_key])


# Static summary placeholder
static_summaries = {
    "Health Insurance": "PM-JAY (Ayushman Bharat) provides ₹5 lakh cover to poor families. Available at empanelled hospitals across India.",
    "Life Insurance": "PMJJBY provides ₹2 lakh cover for ₹330/year. For citizens aged 18–50 with a bank account.",
    "Crop Insurance": "PMFBY helps farmers get insurance for crops affected by floods, droughts, etc.",
    "Disability Insurance": "Disability insurance provides financial support to individuals with long-term physical disabilities.",
    "Vehicle Insurance": "Covers accident damage and third-party liabilities. Often bundled with motor vehicle purchases.",
    "Travel Insurance": "Covers death/injury during travel. Some IRCTC tickets include free insurance.",
    "Home Insurance": "Provides compensation for flood/fire damage in homes. Targeted at low-income housing.",
    "Livestock Insurance": "Covers loss of insured animals due to accident, illness, or natural causes."
}

st.markdown("### ❓ Ask a Question About This Scheme")

user_question = st.text_input("Type your question here...", placeholder="e.g. Who is eligible for this scheme?")

if user_question and st.button("Ask AI"):
    with st.spinner("🤖 Thinking..."):
        try:
            full_prompt = f"You're an insurance assistant. The user has selected the scheme: '{scheme}'. Respond in simple {lang}. Question: {user_question}"
            response = get_insurance_summary(full_prompt)
            st.success(f"🧠 AI: {response}")
        except Exception as e:
            st.error("⚠️ AI failed to respond.")
            st.code(str(e))

# summary = static_summaries.get(selected_type, "No summary available yet.")
# st.info(summary)

# summary = get_insurance_summary(f"Summarize the {info} insurance scheme in simple terms.")































# import streamlit as st
# # from utils.ai import get_insurance_summary
# from utils.sidebar import render_sidebar
# render_sidebar()
# from utils.static_data import insurance_descriptions

# lang = st.session_state.get("language", "en")
# selected_type = st.session_state.get("selected_insurance_type", "Health Insurance")

# info = insurance_descriptions.get(lang, insurance_descriptions["en"]).get(selected_type)

# if info:
#     st.subheader(f"📘 {info['scheme']}")
#     st.write(f"💰 Premium: {info['premium']}")
#     st.write(f"✅ Eligibility: {info['eligibility']}")
#     st.write(f"🛡️ Coverage: {info['coverage']}")
# else:
#     st.warning("No scheme data available for this insurance type.")


# st.title("🧠 Insurance Summary (AI)")

# if "selected_insurance_type" not in st.session_state or "selected_scheme_name" not in st.session_state:
#     st.warning("Please select an insurance type from the previous page first.")
#     st.stop()

# scheme = st.session_state.selected_scheme_name
# ins_type = st.session_state.selected_insurance_type
# summary_key = f"summary_{ins_type}"

# # st.markdown(f"### 🛡️ {scheme}")
# # st.markdown(f"Type: **{ins_type}**")

# # # Dummy AI summaries for common types
# # STATIC_SUMMARIES = {
# #     "Health Insurance": "PM-JAY (Ayushman Bharat) provides ₹5 lakh cover to poor families. Available at empanelled hospitals across India.",
# #     "Life Insurance": "PMJJBY provides ₹2 lakh cover for ₹330/year. For citizens aged 18–50 with a bank account.",
# #     "Crop Insurance": "PMFBY helps farmers get insurance for crops affected by floods, droughts, etc.",
# #     "Disability Insurance": "Disability insurance provides financial support to individuals with long-term physical disabilities.",
# #     "Vehicle Insurance": "Accident cover + minor bike damage compensation under bundled plans.",
# #     "Travel Insurance": "Covers death/injury during train travel. Automatically applied on some ticket bookings.",
# #     "Home Insurance": "Compensation for damage due to flood/fire in low-cost housing."
# # }

# # Check if we've already called the AI (or dummy) before
# # if summary_key not in st.session_state or st.button("🔁 Regenerate Summary"):
# #     with st.spinner("Generating AI summary..."):
# #         # In production: call Gemini API here
# #         prompt = f"Explain the '{scheme}' insurance scheme in simple Hindi and English. Highlight eligibility, benefits, and how to claim."
# #         # summary = get_insurance_summary(prompt)
# #         st.session_state[summary_key] = summary

# # st.markdown("### 💬 Summary (AI):")
# # st.info(st.session_state[summary_key])
# # st.markdown("### 📊 Scheme Snapshot (Static Info)")
# # info = insurance_descriptions.get(ins_type)
# # if info:
# #     for key, value in info.items():
# #         st.markdown(f"✅ {key}: {value}")
# # else:
# #     st.info("No static data available for this scheme.")

# # # Optional: Ask your own question
# # st.markdown("### ❓ Ask your own question about this scheme")
# # user_q = st.text_input("Ask AI")

# # if user_q:
# #     # Simulate dummy AI response
# #     st.success(f"🤖 AI: This scheme is especially helpful for people with conditions related to: {ins_type.lower()}.")

