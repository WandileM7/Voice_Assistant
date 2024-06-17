import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv('API_KEY'))

model = genai.GenerativeModel('gemini-pro')
response = model.generate_content('Please tell me if i  can code my own jarvis from home: ...')

print(response.text)