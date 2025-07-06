# 🧠 Brain-Exe – Insurance Assistant for Bharat

Brain-Exe is a multilingual, voice-enabled insurance assistant designed to help citizens—especially from small towns and rural India—understand, compare, and claim Indian government insurance schemes.

> Built for Hackathons. Made for Bharat.

---

## 🚀 Features

- 🇮🇳 **Supports Multiple Indian Languages** – Hindi, Marathi, Tamil, Telugu, Gujarati, Bengali, and more.
- 🎤 **Voice Input (Speech-to-Text)** – Ask your insurance questions using your voice.
- 🤖 **Chatbot Assistant** – Friendly and intelligent chatbot powered by OpenRouter LLMs for insurance Q&A and personalized recommendations.
- 📋 **User Survey** – Collects user details (location, age, job, Aadhaar, etc.) to suggest best-suited schemes.
- 📊 **Plan Explorer** – Easily browse and compare Indian government insurance schemes like Ayushman Bharat, PMJJBY, PMFBY, PMSBY, LIC, etc.
- ✅ **Aadhaar-based KYC Support** (Simulated)
- 📝 **Claim Filing Walkthroughs** – Explains how to claim your benefits in simple terms.
- 📦 **Recommendation Engine** – Suggests personalized plans based on survey responses.

---

## 🛠️ Tech Stack

| Frontend           | Backend               | AI/ML/LLM              | Other Integrations         |
|--------------------|-----------------------|------------------------|----------------------------|
| Streamlit (Python) | Firebase Firestore    | OpenRouter (LLM API)   | Whisper (voice input)      |
| Streamlit UI Pages | Firebase Auth         | Prompt Engineering     | Aadhaar KYC (simulated)    |
|                    | Python utils modules  |                        | Google Translate (optional)|

---

## 🔄 Flow

1. **Landing Page** → Choose language
2. **Option A: Explore Plans** → Browse schemes in your language
3. **Option B: Take Survey** → Fill a form with personal info
4. **Backend saves response to Firebase**
5. Redirect to **Chatbot Assistant Page**
6. Ask questions via **Text or Voice**
7. LLM generates answers, recommends plans
8. Option to **File a Claim** or **Learn More**

---

## 📁 Project Structure
brain-exe/
├── backend/
| ├── main.py
| ├── razorpay_payment.py/
├── streamlit_ui/
│ ├── app.py
│ ├── pages/
│ │ ├── 1_language_select.py
│ │ ├── 2_aadhar_kyc.py
│ │ ├── 3_otp_verify.py
│ │ ├── 3_explore_insurance.py
│ │ ├── 4b_insurance_summary.py
│ │ ├── 5_plan_browser.py
│ │ ├── 6_submit_claim.py
│ │ ├── 7_payment_gateway.py
│ │ ├── 8_survey_form.py
│ │ ├── 9_chatbot_assistant.py
│ │ ├── payment_success.py
│ ├── utils/
│ │ ├── ai.py
│ │ ├── firebase.py
│ │ ├── voice_input.py
│ │ ├── voice.py
│ │ ├── tts_stt.py
│ │ └── sidebar.py
├── requirements.txt
├── README.md
└── .env (for API keys)

---

## 🧪 How to Run Locally

1. Clone the repo:
   ```bash
   git clone https://github.com/Tictiate/brain-exe.git
   cd brain-exe

2. Create a virtual environment:
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

3. Install dependencies:
pip install -r requirements.txt

4. Add your `.env` files with keys

5. Run the app:
streamlit run streamlit_ui/app.py
python backend/main.py
 
📌 Key Insurance Schemes Covered
Health: Ayushman Bharat (PM-JAY)
Life: PMJJBY, LIC Jeevan Tarun
Accident: PMSBY
Disability: Niramaya Health Insurance
Crop: PMFBY
Travel: IRCTC Travel Insurance
Vehicle: IRDAI Motor Insurance
Education: LIC scholarship plans

💡 Vision
To empower every Indian—regardless of language, education, or access—to understand their rights and benefits under government insurance schemes.

🙌 Team
Built by team Brain.exe
For Hackathons, College Projects & Bharat
