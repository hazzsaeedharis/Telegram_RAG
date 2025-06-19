import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Uncomment this if you want to use OpenAI later
# import openai
# openai.api_key = os.getenv("OPENAI_API_KEY")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite-001:generateContent"


def ask_llm(prompt: str) -> str:
    """
    Sends the prompt to the Gemini API.
    Returns the LLM's response as a string.
    """
    headers = {
        "Content-Type": "application/json"
    }
    
    params = {
        "key": GEMINI_API_KEY
    }
    
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    
    response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=data)
    
    if response.status_code == 200:
        result = response.json()
        try:
            return result['candidates'][0]['content']['parts'][0]['text'].strip()
        except (KeyError, IndexError):
            return "Received an unexpected response format from Gemini API."
    else:
        return f"Request failed with status code {response.status_code}: {response.text}"

# Uncomment this if you want to switch back to OpenAI implementation later
# def ask_llm(prompt: str) -> str:
#     """
#     Sends the prompt to the OpenAI ChatCompletion API.
#     Returns the LLM's response as a string.
#     """
#     response = openai.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0.2,
#         max_tokens=512
#     )
#     return response.choices[0].message.content.strip()

# Example test
if __name__ == "__main__":
    reply = ask_llm("Tell me a fun fact about space.")
    print(reply)