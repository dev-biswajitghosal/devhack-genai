"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv('API_KEY')

genai.configure(api_key=API_KEY)

# Set up the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[
    {
        "role": "user",
        "parts": ["hi"]
    },
    {
        "role": "model",
        "parts": ["Hello! How can I assist you today?"]
    },
])


def generate_content(prompt=None):
    prompt = prompt or "Please provide a prompt for me."
    convo.send_message(prompt)
    return convo.last.text

# def generate_content(prompt=None, file=None):
#     if file is not None:
#         with open(file, "r") as f:
#             file_content = f.read()
#         prompt = "Summarize the following article:\n\n" + file_content
#     else:
#         prompt = prompt or "Please provide a prompt for me."
#
#     convo.send_message(prompt)
#     print(convo.last.text)
#     return convo.last.text
