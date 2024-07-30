import datetime
# import math
# from pathlib import Path
# import sys
import time
# import threading
import webbrowser
from dotenv import load_dotenv
from openai import OpenAI
# import pygame
# import pyttsx3
import speech_recognition as sr
# import pyautogui
import os.path
import json
from events import *
import subprocess
import warnings
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import pywhatkit
import platform
from tools import tools
from utils import speak 
from gmail import *


# Ignore DeprecationWarning
warnings.filterwarnings("ignore", category=DeprecationWarning)
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client with the API key
client = OpenAI(api_key=api_key)



# Set up Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv('SPOTIPY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
    redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
    scope="user-read-playback-state,user-modify-playback-state"
))

# def speak(text, rate=120):
#     time.sleep(0.3)
#     try:
#         response = client.audio.speech.create(
#             model="tts-1",
#             voice="nova",
#             input=text
#         )
#         speech_file_path = Path(__file__).parent / "speech.mp3"
#         response.stream_to_file(speech_file_path)
#         pygame.mixer.init(frequency=12000, buffer=512)
#         speech_sound = pygame.mixer.Sound(speech_file_path)
#         speech_length = int(math.ceil(pygame.mixer.Sound.get_length(speech_sound)))
#         speech_sound.play()
#         time.sleep(speech_length)
#         pygame.mixer.quit()
#     except Exception as e:
#         print(f"An error occurred during speech synthesis: {e}")
#     finally:
#         # Clean up the temporary speech file
#         if os.path.exists(speech_file_path):
#             os.remove(speech_file_path)

def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        r.pause_threshold = 1.0
        r.phrase_threshold = 0.3
        r.non_speaking_duration = 0.5
        r.energy_threshold = 4000
        r.dynamic_energy_threshold = True
        r.dynamic_energy_adjustment_ratio = 1.5
        r.phrase_time_limit = 5

        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-ZA')
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            print("Sorry, I did not catch that")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return ""
        except Exception as e:
            print(f"An error occurred: {e}")
            return ""

def cal_day():
    day = datetime.datetime.today().weekday()
    day_dic = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }
    return day_dic[day]

def play_song(song_name=None, song_uri=None):
    if song_uri is None and song_name is None:
        # If no song URI or name is provided, play a default song or user's last played song
        song_uri = 'spotify:track:57vxBYXtHMk6H1aD29V7PU'  # Default song URI
    elif song_uri is None:
        # Search for the song if only a name is provided
        results = sp.search(q=song_name, limit=1, type='track')
        if results['tracks']['items']:
            song_uri = results['tracks']['items'][0]['uri']
        else:
            return f"Couldn't find a song named '{song_name}'"

    devices = sp.devices()
    if not devices['devices']:
        return "No Spotify devices found"

    device_id = devices['devices'][0]['id']

    try:
        sp.start_playback(device_id=device_id, uris=[song_uri])
        track_info = sp.track(song_uri)
        return f"Playing '{track_info['name']}' by {track_info['artists'][0]['name']}"
    except spotipy.SpotifyException as e:
        error_message = f"An error occurred while playing the song: {e}"
        print(error_message)
        return error_message

def wishMe():
    hour = datetime.datetime.now().hour
    t = time.strftime("%I:%M %p")
    day = cal_day()

    if 0 <= hour < 12:
        greeting = "Good morning"
    elif 12 <= hour < 16:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    speak(f"{greeting} Boss, It's {day} and the time is {t}")

def social_media(command):
    sites = {
        'facebook': "https://facebook.com/",
        'discord': "https://discord.com/channels/@me/",
        'instagram': "https://instagram.com",
        'anime': "https://www.crunchyroll.com/"
    }

    for keyword, url in sites.items():
        if keyword in command:
            speak(f"Opening your {keyword}")
            webbrowser.open(url)
            return

    speak("No results found")



def open_application(app_name):
    system = platform.system()
    try:
        if system == 'Windows':
            os.startfile(app_name)
        elif system == 'Darwin':  # macOS
            subprocess.run(["open", "-a", app_name])
        elif system == 'Linux':
            subprocess.Popen([app_name.lower()])
        return f"Opening {app_name}"
    except Exception as e:
        return f"Failed to open {app_name}: {str(e)}"

def close_application(app_name):
    system = platform.system()
    try:
        if system == 'Windows':
            subprocess.run(["taskkill", "/F", "/IM", f"{app_name.lower()}.exe"])
        elif system in ['Darwin', 'Linux']:
            subprocess.run(["pkill", "-f", app_name.lower()])
        return f"Closing {app_name}"
    except Exception as e:
        return f"Failed to close {app_name}: {str(e)}"

def send_whatsapp_message(recipient, message):
    contacts = {
        "bert": "+27832178843",
        "bubbles": "+27720656667",
        # Add more contacts as needed
    }

    if recipient in contacts:
        try:
            pywhatkit.sendwhatmsg_instantly(contacts[recipient], message)
            return f"Message sent to {recipient}"
        except Exception as e:
            error_message = f"An error occurred while sending the message: {str(e)}"
            print(error_message)
            return error_message
    else:
        return f"Sorry, I couldn't find {recipient} in your contacts."





assistant = client.beta.assistants.create(
    name="Personal Assistant",
    instructions="You are a helpful assistant named Wednesday that performs various tasks based on user commands. Your personality is based on Wednesday Addams. Engage in conversation and use functions when necessary. Any query regarding email reading and scheduling should be kept short and sweet ",
    tools=tools,
    model="gpt-4-1106-preview",
)

def get_openai_response(thread_id, user_input, use_speech=True):
    try:
        # Check for any active runs
        runs = client.beta.threads.runs.list(thread_id=thread_id)
        active_runs = [run for run in runs.data if run.status in ["queued", "in_progress", "requires_action"]]

        if active_runs:
            # If there's an active run, wait for it to complete
            active_run = active_runs[0]
            while active_run.status != "completed":
                time.sleep(1)
                active_run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=active_run.id)

        # Add user message to the thread
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_input
        )

        # Run the assistant
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant.id
        )

        # Wait for the run to complete or require action
        while run.status not in ["completed", "failed", "requires_action"]:
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)

        if run.status == "requires_action":
            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            tool_outputs = []

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                # Use a dictionary to map function names to their corresponding functions
                function_map = {
                    "play_song": play_song,
                    "open_application": open_application,
                    "close_application": close_application,
                    "send_whatsapp_message": send_whatsapp_message,
                    "schedule": schedule,
                    "social_media": social_media,
                    "create_event": create_event,
                    "read_emails": read_emails,
                    "send_email": send_email
                }

                if function_name in function_map:
                    output = function_map[function_name](**function_args)
                else:
                    output = f"Function {function_name} not implemented"

                tool_outputs.append({
                    "tool_call_id": tool_call.id,
                    "output": output
                })

            # Submit the tool outputs
            run = client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )

            # Wait for the run to complete after submitting tool outputs
            while run.status != "completed":
                time.sleep(1)
                run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)

        # Retrieve the messages
        messages = client.beta.threads.messages.list(thread_id=thread_id)

        # Return the last assistant message
        for message in messages.data:
            if message.role == "assistant":
                response = messages.data[0].content[0].text.value
                if use_speech:
                    speak(response)
                return response
        

    except Exception as e:
        print(f"An error occurred: {e}")
        return "Sorry, I couldn't process your request."

def main():
    wishMe()
    thread = client.beta.threads.create()

    while True:
        user_input = command().lower()

        if not user_input:
            continue

        if "goodbye" in user_input.lower() or "exit" in user_input.lower():
            speak("Goodbye! Have a great day.")
            break

        response = get_openai_response(thread.id, user_input, use_speech=True)
        print(f"Assistant: {response}")

if __name__ == "__main__":
    main()