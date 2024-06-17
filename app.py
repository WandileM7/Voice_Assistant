import sys
from codex import Chatbot
from configparser import ConfigParser
import os
from dotenv import load_dotenv
load_dotenv()


def main():
    config = ConfigParser()
    config.read('credentials.ini')
    api_key=os.getenv('API_KEY')

    chatbot = Chatbot(api_key=api_key)
    print("Welcome to Chatbot. TYpe 'quit to exit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            sys.exit("exiting bot...")
        try:
            response = chatbot.send_prompt(user_input)
            print(f"{chatbot.CHATBOT_NAME}: {response}")
        except Exception as e:
            print(f"Error: {e}")

main()