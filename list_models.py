import google.generativeai as genai
import os

# Set the API key from your environment variable
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Print a list of all available models
for model in genai.list_models():
  # Only show models that support the generateContent method, as we need that for our app.
  if 'generateContent' in model.supported_generation_methods:
    print(model.name)