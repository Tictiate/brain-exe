import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPEN_ROUTER_KEY")

def get_insurance_summary(prompt: str):
    if not api_key:
        raise Exception("❌ API key not found in environment variables.")

    url = "https://openrouter.ai/api/v1/chat/completions"


    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",  # optional but recommended
        "X-Title": "Brain-Exe-Assistant"
}


    data = {
        "model": "mistralai/mistral-7b-instruct",  # Use an available free model
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            print("⚠️ AI Error:", response.status_code, "-", response.text)
            return None

        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("❌ Exception while calling OpenRouter:", str(e))
        return None
