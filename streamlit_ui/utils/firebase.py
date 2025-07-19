import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()


service_account_info = os.getenv("FIREBASE_KEY_PATH")

# ✅ Initialize Firebase app
if not firebase_admin._apps:
    cred = credentials.Certificate(service_account_info)
    firebase_admin.initialize_app(cred)

# ✅ Get Firestore DB
db = firestore.client()

# ✅ Store survey
def store_survey_response(data):
    db.collection("user_survey_responses").add(data)

# ✅ Get latest survey by user
def get_latest_survey_by_user(user_id):
    try:
        docs = (
            db.collection("user_survey_responses")
            .where("user_id", "==", user_id)
            .order_by("timestamp", direction=firestore.Query.DESCENDING)
            .limit(1)
            .stream()
        )
        for doc in docs:
            return doc.to_dict()
        return None
    except Exception as e:
        print("🔥 Error in get_latest_survey_by_user():", e)
        return None
