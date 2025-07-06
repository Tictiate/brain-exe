import razorpay
import json

# Load secrets from razorpayKey.json

RAZORPAY_KEY = "rzp_test_2CCzX1D1zas25Q"
RAZORPAY_SECRET = "KRPd7wQMCrICP9c7xYeegL2g"
 
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