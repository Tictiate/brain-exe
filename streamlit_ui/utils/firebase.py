# backend/firebase_utils.py

import firebase_admin
from firebase_admin import credentials, firestore
import os

# ⚠️ Only initialize Firebase once
if not firebase_admin._apps:
    # Set path to your Firebase service account key JSON
    cred_path = "backend/serviceAccountKey.json"
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

def store_survey_response(data: dict):
    """
    Stores the survey response in the 'user_survey_responses' collection in Firestore.
    Each document uses a unique UUID from the data dict.
    """
    try:
        doc_id = data.get("id")
        if not doc_id:
            raise ValueError("Missing unique 'id' in survey data.")

        db.collection("user_survey_responses").document(doc_id).set(data)
        print(f"✅ Survey data saved to Firestore with ID: {doc_id}")

    except Exception as e:
        print(f"🔥 Failed to save survey response: {e}")
