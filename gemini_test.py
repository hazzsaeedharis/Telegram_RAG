import google.generativeai as genai

# Replace this with your actual API key
api_key = "AIzaSyAjKCK9GSGsJs1LqF3f2IbFRZQXP8htS4s"

# Configure the API key
genai.configure(api_key=api_key)

# Initialize a generative model (Gemini 1.5 Pro for example)
model = genai.GenerativeModel("gemini-1.5-pro")

# Send a test prompt
response = model.generate_content("Hello Gemini, can you confirm you're working?")

# Print the response
print(response.text)