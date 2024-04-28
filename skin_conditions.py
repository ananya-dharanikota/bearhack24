import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv(".env")

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro-latest')

location_on_body = []  # List of strings of where the skin lesion is located
pain_level = ""  # Pain Level - Mild, Moderate, Severe
pain_description = []  #  Pain description: Throbbing, Burning, Stinging, Dull, Aching, Stabbing
color = ""  # What color skin lesion is: Purple/Blue, Green/Yellow, Red/brown, Brown/Black, White
arrangement = ""  # Randomly Scattered, Grouped in Clusters, Uniform Pattern, N/A
length = ""  # How long they've been experiencing: 3-5 days, 1-3 weeks, 2+ months, 1+ years
exposure = [] # Chemicals, Environments, Animals
family_history = [] # Eczema, Skin Cancer, Ichthyosis, Albinism, Rosacea



def print_symptoms(diagnosis):
    prompt = f'''
        You are a dermatologist, who specializes in identifying skin conditions.
        Give me the treatment options of eczema.
         '''

    response = model.generate_content(prompt)
    print(response.text)
    #return response.text

def print_causes(diagnosis):
    pass

def print_description(diagnosis):
    pass