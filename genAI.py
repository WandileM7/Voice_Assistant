import math
import os
import time
from ctypes import *
from pathlib import Path

import google.generativeai as palm
import openai
import pygame
import speech_recognition as sr
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
# palm.configure(api_key=os.getenv("MAKER_SUITE"))
error_handler_func = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()
# CHUNK_SIZE = 1024
# url = "https://api.elevenlabs.io/v1/text-to-speech/AZmkNsdMVV3QsXBcwabo"

import os
from dotenv import load_dotenv
import google.generativeai as palm

load_dotenv()
#
# palm.configure(api_key=os.getenv("MAKER_SUITE"))


def get_command():
    listener = sr.Recognizer()
    print("Listening for command...")

    with sr.Microphone() as source:
        listener.pause_threshold = 2
        input_speech = listener.listen(source)

    try:
        print("Recognizing speech...")
        query = listener.recognize_google(input_speech, language="en_gb")
        print(query)

    except Exception as exception:
        print("I did not quite catch that")
        speak("I did not quite catch that")
        print(exception)
        return None
    return query


def speak(text, rate=120):
    time.sleep(0.3)
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=text
        )
        speech_file_path = Path(__file__).parent / "speech.mp3"
        response.stream_to_file(speech_file_path)
        pygame.mixer.init(frequency=12000, buffer=512)
        speech_sound = pygame.mixer.Sound(speech_file_path)
        speech_length = int(math.ceil(pygame.mixer.Sound.get_length(speech_sound)))
        speech_sound.play()
        time.sleep(speech_length)
        pygame.mixer.quit()

    except KeyboardInterrupt:
        pass


def generate_response(messages):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        n=1,
        stop=None,
        temperature=0.99,
    )
    message = response.choices[0].message.content
    messages.append(response.choices[0].message)
    return message


if __name__ == "__main__":
    messages = []
    while 1:
        text = get_command()
        messages.append({"role": "user", "content": text})
        response = generate_response(messages)
        speak(response)
        print(response)
