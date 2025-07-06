import streamlit as st
import uuid
from utils.firebase import store_survey_response
from utils.sidebar import render_sidebar

# ✅ Render custom sidebar
render_sidebar()

st.set_page_config(page_title="Insurance Survey", page_icon="📝")
st.title("📝 Insurance Recommendation Survey")
st.markdown("Please fill out the details below to get policy suggestions.")

# ✅ Form starts here
with st.form("insurance_survey_form"):

    name = st.text_input("Full Name")
    age = st.number_input("Age", min_value=18, max_value=120)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced", "Widowed"])
    dependents = st.slider("Number of Dependents", 0, 10)

    occupation = st.selectbox("Occupation", [
        "Student", "Govt Employee", "Private Sector", "Self-Employed", "Unemployed", "Retired"
    ])
    income = st.number_input("Monthly Income (₹)", min_value=0)
    sector = st.radio("Work Sector", ["Formal", "Informal", "Not applicable"])
    has_income_proof = st.radio("Do you have income proof?", ["Yes", "No"])

    has_existing_insurance = st.radio("Do you already have insurance?", ["Yes", "No"])
    insurance_type = st.multiselect("If yes, what type?", [
        "Health", "Life", "Accident", "Disability", "Pension"
    ])
    health_conditions = st.text_area("Mention any health conditions")

    preferred_coverage = st.multiselect("What coverage do you want?", [
        "Health", "Life", "Maternity", "Senior", "Child Benefit"
    ])
    preferred_premium = st.number_input("Preferred Monthly Premium (₹)", min_value=0)
    payout_expectation = st.selectbox("Preferred payout type", [
        "Lump sum", "Monthly pension", "Emergency medical", "Death benefit", "Not sure"
    ])
    priority = st.selectbox("Your priority", [
        "Low premium", "High coverage", "Easy claim", "Govt-backed", "Tax benefits"
    ])

    submitted = st.form_submit_button("Submit Survey")

# ✅ On submit — save to Firebase
if submitted:
    survey_data = {
        "id": str(uuid.uuid4()),
        "name": name,
        "age": age,
        "gender": gender,
        "marital_status": marital_status,
        "dependents": dependents,
        "occupation": occupation,
        "income": income,
        "sector": sector,
        "has_income_proof": has_income_proof,
        "has_existing_insurance": has_existing_insurance,
        "insurance_type": insurance_type,
        "health_conditions": health_conditions,
        "preferred_coverage": preferred_coverage,
        "preferred_premium": preferred_premium,
        "payout_expectation": payout_expectation,
        "priority": priority
    }

    store_survey_response(survey_data)
    st.success("✅ Survey submitted successfully!")
