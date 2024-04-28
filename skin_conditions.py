import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv(".env")

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro-latest')

# location_on_body = []  # List of strings of where the skin lesion is located
# pain_level = ""  # Pain Level - Mild, Moderate, Severe
# pain_description = []  #  Pain description: Throbbing, Burning, Stinging, Dull, Aching, Stabbing
# color = ""  # What color skin lesion is: Purple/Blue, Green/Yellow, Red/brown, Brown/Black, White
# arrangement = ""  # Randomly Scattered, Grouped in Clusters, Uniform Pattern, N/A
# length = ""  # How long they've been experiencing: 3-5 days, 1-3 weeks, 2+ months, 1+ years
# exposure = [] # Chemicals, Environments, Animals
# family_history = [] # Eczema, Skin Cancer, Ichthyosis, Albinism, Rosacea

def filter_response(gemini_response) -> list:
    response = gemini_response.split("\n")
    filtered_text = []

    # List of characters we want to keep (whitelist)
    allowed_characters = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ -,;:")

    for line in response:
        # Keep only the allowed characters
        filtered_line = "".join(char for char in line.strip() if char in allowed_characters)
        
        # Add the filtered line to the list if it's not empty
        if filtered_line:
            filtered_text.append(filtered_line)

    return filtered_text


def print_symptoms(diagnosis):
    prompt = f'''
        You are a dermatologist, and you just identified that a patient
        of yours has {diagnosis}.
        Briefly explain in a list, the symptoms of {diagnosis}
        '''

    response = model.generate_content(prompt)
    print(response.text)
    return response.text
    #return response.text

def print_treatments(diagnosis):
    prompt = f'''
        You are a dermatologist, and you just identified that a patient
        of yours has {diagnosis}.
        Briefly explain in a list what possible treatments that the patient can do
        to treat {diagnosis}. The patient already knows the warnings, so you don't have
        to say them, just possible treatments.
        '''

    response = model.generate_content(prompt)
    print(response.text)
    return response.text

def print_description(diagnosis):
    prompt = f'''
        You are a dermatologist, and you just identified that a patient
        of yours has {diagnosis}.
        Briefly explain the description of {diagnosis}. Keep it short
        and don't say the symptoms or causes, just what {diagnosis} is.
        '''

    response = model.generate_content(prompt)
    print(response.text)
    return response.text

# skin = "acne"
# # # # print_symptoms(skin)
# # # # print_causes(skin)
# # # print_description(skin)

# print(filter_response(print_symptoms(skin)))