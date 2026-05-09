import os
from google import genai

history = []
def query(prompt):
    history.append({"role": "user", "parts": [{"text": prompt}]})
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=history
    )
    history.append({"role": "model", "parts": [{"text": response.text}]})
    return response.text

print("API initilising...")

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
client = genai.Client(api_key=GEMINI_API_KEY)
promt = "hi"
print("API started")
response = query(promt)
print(response)