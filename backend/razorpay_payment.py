import razorpay
import json

# Load secrets from razorpayKey.json
with open("razorpayKey.json") as f:
    secrets = json.load(f)

RAZORPAY_KEY = secrets["RAZORPAY_KEY"]
RAZORPAY_SECRET = secrets["RAZORPAY_SECRET"]

# Initialize Razorpay client
client = razorpay.Client(auth=(RAZORPAY_KEY, RAZORPAY_SECRET))

def create_payment_link(amount_in_rupees, customer_name, email):
    amount_in_paise = int(amount_in_rupees * 100)

    response = client.payment_link.create({
        "amount": amount_in_paise,
        "currency": "INR",
        "accept_partial": False,
        "description": "Hackathon Insurance Payment",
        "customer": {
            "name": customer_name,
            "email": email,
        },
        "notify": {
            "email": True
        },
        "reminder_enable": False,
        "callback_url": "http://localhost:8501",
        "callback_method": "get"
    })

    return response["short_url"]