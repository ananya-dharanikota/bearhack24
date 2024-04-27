import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv(".env")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro-latest')



prompt = f'''
        Give me a description of Acne
         '''

response = model.generate_content(prompt)
print(response.text)