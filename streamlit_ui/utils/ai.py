import openai
import json

# Load secrets from openAIKey.json
with open("openAIKey.json") as f:
    secrets = json.load(f)

client = openai.OpenAI(api_key=secrets["openAIKey"])

def get_insurance_summary(prompt: str):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You're a helpful insurance assistant. Respond in simple Hindi and English."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
