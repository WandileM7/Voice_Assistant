from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from main import get_openai_response
from openai import OpenAI
import os
from pyngrok import ngrok
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenAI setup
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
thread = client.beta.threads.create()

# Twilio configuration
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_client = Client(account_sid, auth_token)
twilio_phone_number = 'whatsapp:+19387772439'  # Replace with your Twilio WhatsApp number

app = Flask(__name__)

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    from_number = request.values.get('From', '')

    logger.info(f"Received message: {incoming_msg} from {from_number}")

    # Get the response from the OpenAI assistant
    response = get_openai_response(thread.id, incoming_msg, use_speech=False)
    
    # Create a Twilio MessagingResponse
    resp = MessagingResponse()
    resp.message(response)

    logger.info(f"Sent response: {response} to {from_number}")

    return str(resp)

if __name__ == "__main__":
    app.run()
