import json

import pyttsx3  # Recognition Voice Function
import datetime
import speech_recognition as sr
import wikipedia
import playsound
import os
import dotenv
import music

from weather import Weather
from music import Music

# Load the environment variables which is more safe and a good habit rather than loading it directly on the script.
dotenv.load_dotenv(dotenv_path="./config.env")

MASTER = os.getenv("MASTER")

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# * Modules Startup
mod_weather = Weather(os.getenv("WEATHER_API"))
mod_music = Music(os.getenv("MUSIC_BASE_DIRECTORY"))


# Speak Function
def speak(text):
    engine.say(text)
    engine.runAndWait()


# This function will speak or greet you
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning" + MASTER)
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon" + MASTER)
    else:
        speak("Good Evening" + MASTER)
    # speak("I am Jarvis. How may I help you?")


# This function will take command from Microphone
def takeCommand() -> str:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-us')
        print(f"user said: {query}\n")
    except sr.WaitTimeoutError as e:
        print("Say that again please.")
        query = None
    except sr.UnknownValueError as e:
        print("Unknown Value ERROR")

    if query == "" or query is None:
        speak("Please speak something.")
    else:
        return query


def special_string_replace(value: str):
    with open("./custom_string_replace.json", "r") as csp:
        data = json.load(csp)

        for json_object in data:
            for keys, content in json_object.items():
                if keys == "name" and content in value:
                    value = value.replace(json_object["name"], os.getenv(json_object["data"]) if json_object["type"] == "VAR_ENVIRONMENT" else json_object["data"])
                    value = value.replace("\\", "/")
                    break
        return value


def sentence_execution():
    # Temporarily disabled for testing and developement.
    # query = takeCommand()

    with open("sentences_logic.json", "r") as sentences:
        data = json.load(sentences)

        # query = takeCommand().lower()
        query = "play music"

        for sentence_object in data:
            sentence = sentence_object["sentence"]
            sentence_execute = sentence_object["execute"]
            sentence_type = sentence_object["type"]
            # * This if condition will be used if we are executing applications or only for the AI Speaking.
            if sentence in query.lower():
                # If the query has sentence similarity from this,
                # the code according to the meaning of the sentence is called.
                special_string_processed = special_string_replace(sentence_execute)

                # START_FILE: This will start the file with or without argument.
                # SAY: Use the speak() function to say.
                if sentence_type == "START_FILE":
                    os.system(special_string_processed)
                    break
                elif sentence_type == "SAY":
                    speak(special_string_processed)
                    break
            # Else, we will create our own block just like the first version of this project.
            elif "what is today's weather" in query.lower():
                speak(f"Today's weather is {mod_weather.getTodayCondition()}")
                break
            elif "wikipedia" in query.lower():
                query = query.replace("wikipedia", "")
                info = wikipedia.summary(query.lower(), sentence=2)
                speak(info)
            elif ("play music" in query.lower()) or ("play song" in query.lower()):
                mod_music.play_music()
                break
            elif ("stop music" in query.lower()) or ("stop song" in query.lower()):
                mod_music.stop_music()
                break
            elif ("replay music" in query.lower()) or ("replay song" in query.lower()):
                mod_music.replay_music()
                break

        speak("Sorry, I didn't understand.")
        return


if __name__ == "__main__":
    sentence_execution()
    # main()
