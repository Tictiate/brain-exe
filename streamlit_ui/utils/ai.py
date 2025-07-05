import openai

client = openai.OpenAI(api_key="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")  # use your actual key

def get_insurance_summary(prompt: str):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You're a helpful insurance assistant. Respond in simple Hindi and English."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
