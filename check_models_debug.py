import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

with open("models_output.txt", "w") as f:
    if not api_key:
        f.write("API Key not found in .env\n")
    else:
        genai.configure(api_key=api_key)
        f.write("Listing models...\n")
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    f.write(f"Model Name: {m.name}, Display Name: {m.display_name}\n")
        except Exception as e:
            f.write(f"Error: {str(e)}\n")
