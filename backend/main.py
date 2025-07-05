from flask import Flask, request, jsonify
from flask_cors import CORS
from random import randint

import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Simple in-memory store (MVP only)
otp_store = {}

app = Flask(__name__)
CORS(app)  # Allow frontend to access this backend

@app.route("/")
def home():
    return "Brain.exe Backend Running ✅"


@app.route("/kyc", methods=["POST"])
def kyc():
    data = request.json
    aadhaar = data.get("aadhaar_number")

    # Validate Aadhaar number
    if not aadhaar or len(aadhaar) != 12 or not aadhaar.isdigit():
        return jsonify({
            "status": "error",
            "message": "Invalid Aadhaar number"
        }), 400

    # Generate a fake OTP
    otp = str(randint(100000, 999999))
    otp_store[aadhaar] = otp  # Store OTP in memory (MVP only)
    print(f"[DEBUG] Simulated OTP sent to user: {otp}")
    db.collection("kyc_submissions").add({
    "aadhaar_number": aadhaar,
    "otp": otp,
    "timestamp": firestore.SERVER_TIMESTAMP
    })

    # Return response
    return jsonify({
        "status": "success",
        "message": "OTP sent (simulated)",
        "otp": otp  # Show in response for demo
    })

from PIL import Image
import os

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/submit-claim", methods=["POST"])
def submit_claim():
    if 'photo' not in request.files:
        return jsonify({"status": "error", "message": "No photo file provided"}), 400

    image = request.files["photo"]
    filename = image.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    image.save(filepath)

    # Try to extract EXIF metadata
    try:
        img = Image.open(filepath)
        exif_data = img._getexif() or {}
        exif_clean = {}

        for tag_id, value in exif_data.items():
            tag = Image.ExifTags.TAGS.get(tag_id, tag_id)
            exif_clean[tag] = str(value)

    except Exception as e:
        exif_clean = {"error": str(e)}

    return jsonify({
        "status": "success",
        "message": f"Image '{filename}' uploaded successfully.",
        "exif": exif_clean
    })

from datetime import datetime

@app.route("/upi-payment", methods=["POST"])
def upi_payment():
    data = request.json
    user_id = data.get("user_id", "demo_user")  # Optional user reference
    amount = data.get("amount", 10)  # Default: ₹10

    transaction_id = f"MOCKTXN-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    # Save to Firebase
    db.collection("upi_payments").add({
        "user_id": user_id,
        "amount": amount,
        "transaction_id": transaction_id,
        "status": "success",
        "timestamp": firestore.SERVER_TIMESTAMP
    })

    return jsonify({
        "status": "success",
        "message": f"₹{amount} simulated payment received",
        "transaction_id": transaction_id
    })

@app.route("/plans", methods=["GET"])
def get_plans():
    plans = [
        {
            "plan_id": "accident-basic",
            "name": "Accident Cover - Basic",
            "weekly_premium": 10,
            "coverage": "₹50,000 accidental cover",
            "claim_process": "Voice + photo submission"
        },
        {
            "plan_id": "hospital-cash",
            "name": "Hospital Cash Plan",
            "weekly_premium": 15,
            "coverage": "₹500/day for hospitalization (max 10 days)",
            "claim_process": "Upload bill & photo proof"
        },
        {
            "plan_id": "bike-insure",
            "name": "Bike + Life Bundle",
            "weekly_premium": 20,
            "coverage": "₹1 lakh accident + ₹10K bike repair",
            "claim_process": "Photo of accident + registration"
        }
    ]

    return jsonify({
        "status": "success",
        "plans": plans
    })

@app.route("/get-claims", methods=["GET"])
def get_claims():
    claims = []
    docs = db.collection("claims").stream()
    
    for doc in docs:
        claim = doc.to_dict()
        claim["id"] = doc.id
        claims.append(claim)

    return jsonify({
        "status": "success",
        "claims": claims
    })

@app.route("/select-plan", methods=["POST"])
def select_plan():
    data = request.json
    user_id = data.get("user_id")
    plan_id = data.get("plan_id")

    if not user_id or not plan_id:
        return jsonify({
            "status": "error",
            "message": "Missing user_id or plan_id"
        }), 400

    db.collection("selected_plans").add({
        "user_id": user_id,
        "plan_id": plan_id,
        "timestamp": firestore.SERVER_TIMESTAMP
    })

    return jsonify({
        "status": "success",
        "message": f"Plan '{plan_id}' saved for user '{user_id}'"
    })

@app.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.json
    aadhaar = data.get("aadhaar_number")
    user_otp = data.get("otp")

    real_otp = otp_store.get(aadhaar)

    if not real_otp:
        return jsonify({
            "status": "error",
            "message": "No OTP found for this Aadhaar"
        }), 404

    if user_otp == real_otp:
        return jsonify({
            "status": "success",
            "message": "OTP verified successfully"
        })
    else:
        return jsonify({
            "status": "error",
            "message": "Incorrect OTP"
        }), 401


@app.route('/recommend_insurance', methods=['POST'])
def recommend_insurance():
    data = request.json

    age = data.get("age", 0)
    profession = data.get("profession", "").lower()
    has_family = data.get("has_family", False)
    is_bpl = data.get("is_bpl", False)
    has_vehicle = data.get("has_vehicle", False)
    travels_by_train = data.get("travels_by_train", False)
    is_pwd = data.get("is_pwd", False)
    has_savings_account = data.get("has_savings_account", False)
    has_children = data.get("has_children", False)

    recommendations = []

    if is_bpl:
        recommendations.append("🛡 Ayushman Bharat PMJAY (Free Health Insurance)")
    if 18 <= age <= 50 and has_savings_account:
        recommendations.append("👨‍👩‍👧‍👦 PM Jeevan Jyoti Bima Yojana (Life Insurance)")
    if profession == "farmer":
        recommendations.append("🌾 PM Fasal Bima Yojana (Crop Insurance)")
    if has_vehicle:
        recommendations.append("🚗 Third-party Motor Insurance (Mandatory)")
    if travels_by_train:
        recommendations.append("🧳 IRCTC Travel Insurance")
    if is_pwd:
        recommendations.append("🧑‍🦽 Niramaya Disability Insurance")
    if 18 <= age <= 70:
        recommendations.append("🔐 PM Suraksha Bima Yojana (Accident Insurance)")
    if has_children:
        recommendations.append("🎓 LIC Jeevan Tarun (Education Insurance)")

    return jsonify({
        "recommended_insurances": recommendations or ["No insurance match found."]
    })



# Always put shit above this
if __name__ == "__main__":
    print("Starting Flask app...")
    app.run(debug=True)

