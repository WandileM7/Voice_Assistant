import os
import time
import math
import pygame
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client with the API key
client = OpenAI(api_key=api_key)

def speak(text, rate=120):
    """
    Convert text to speech using OpenAI's text-to-speech API and play it.

    Args:
        text (str): The text to be spoken.
        rate (int, optional): The speech rate. Defaults to 120.
    """
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
    except Exception as e:
        print(f"An error occurred during speech synthesis: {e}")
    finally:
        # Clean up the temporary speech file
        if os.path.exists(speech_file_path):
            os.remove(speech_file_path)
