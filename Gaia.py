import math
import time
import webbrowser
# Mute ALSA errors
from ctypes import *
from datetime import datetime
from pathlib import Path

# Google TTS
import pygame
# import pyttsx3
import speech_recognition as sr
import wikipedia
import wolframalpha
from dotenv import load_dotenv
from openai import OpenAI

# from original import tts_type

load_dotenv()
error_handler_func = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)


# error_handler_func = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)


def py_error_handler(filename, line, function, err, fmt):
    pass


c_error_handler = error_handler_func(py_error_handler)
#
# engine = pyttsx3.init()
# voices = engine.getProperty("voices")
# engine.setProperty("voice", voices[1].id)

activation_word = "wednesday"

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(chrome_path))

app_id = "EU3HEJ-JW6Q6PR558"
wolfram_client = wolframalpha.Client(app_id)
client = OpenAI()


# def google_tts(voice_name: str, text: str):
#     language_code = "-".join(voice_name.split("-")[:2])
#     text_input = tts.SynthesisInput(text=text)
#     voice_params = tts.VoiceSelectionParams(language_code=language_code, name=voice_name)
#     audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)
#
#     client = tts.TextToSpeechClient()
#     response = client.synthesize_speech(
#         input=text_input, voice=voice_params, audio_config=audio_config
#     )
#
#     return response.audio_content


def gaia_foundation():
    speak("Welcome Sir")

    while True:
        query = get_command().lower().split()
        if query[0] == activation_word and len(query) > 1:
            query.pop(0)

            if query[0] == "say":
                if "hello" in query:
                    speak("Greetings, father")
                else:
                    query.pop()
                    speech = " ".join(query)
                    speak(speech)

            if query[0] == 'recall':
                query.pop(0)
                query = ' '.join(query)
                speech = query_openai(query)
                speak("Ok")
                speak(speech)

            if query[0] == "go" and query[1] == "to":
                speak("Opening...")
                query = " ".join(query[2:])
                webbrowser.get("chrome").open_new(query)

            if query[0] == "wikipedia":
                query = " ".join(query[1:])
                speak("Querying Wikipedia")
                speak(search_wikipedia(query))

            if query[0] == "compute" or query[0] == "computer":
                query = " ".join(query[1:])
                speak("Computing")
                try:
                    result = search_wolframalpha(query)
                    speak(result)
                except:
                    speak("Unable to compute")

            if query[0] == "log":
                take_notes()

            if query[0] == "shut" and query[1] == "down":
                speak("Shutting down")
                break


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
        # try:
        #     if tts_type == 'google' or tts_type == 'openai':
        #         pygame.mixer.quit()
        # except:
        #     pass
        return


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


def search_wikipedia(query=""):
    search_results = wikipedia.search(query)
    if not search_results:
        print("No results found")
        return "No results received"
    try:
        wikipage = wikipedia.page(search_results[0])
    except wikipedia.DisambiguationError as error:
        wikipage = wikipedia.page(error.options[0])
    print(wikipage.title)
    wiki_summary = str(wikipage.summary)
    return wiki_summary


def list_or_dict(var):
    if isinstance(var, list):
        return var[0]["plaintext"]
    else:
        return var["plaintext"]


def take_notes():
    speak("Ready to record note")
    new_note = get_command().lower()
    now = datetime.now().strftime('%H-%M-%S-%d-%m-%Y')
    with open("note_%s.txt" % now, "w") as new_file:
        new_file.write(new_note)
    speak("Note written")


def search_wolframalpha(query=""):
    response = wolfram_client.query(query)

    if response["@success"] == "false":
        return "Could not compute"

    else:
        result = ""
        pod0 = response["pod"][0]
        pod1 = response["pod"][1]

        if ("result" in pod1["@title"].lower()) or (pod1.get("@primary", "false") == "true") or (
                "definition" in pod1["@title"].lower()):

            result = list_or_dict(pod1["subpod"])

            return result.split("(")[0]
        else:
            question = list_or_dict(pod0["subpod"])
            speak("Computing failed, querying Wikipedia")
            return question.split("(")[0], search_wikipedia(question)


def query_openai(prompt=""):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response


if __name__ == "__main__":
    gaia_foundation()