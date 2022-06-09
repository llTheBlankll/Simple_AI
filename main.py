import json

import pyttsx3  # Recognition Voice Function
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import dotenv

from weather import Weather

# Load the environment variables which is more safe and a good habit rather than loading it directly on the script.
dotenv.load_dotenv(dotenv_path="./config.env")

MASTER = os.getenv("MASTER")

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

weather = Weather(os.getenv("WEATHER_API"))


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

    return query


def startup():
    """
    * Removing the long intro. that slows the testing and development.
    * Can be remove anytime.
    speak("Initializing Jarvis")
    speak("Starting all systems applications")
    speak("Installing and checking for all drivers")
    speak("Calibrating and examines all the core processors")
    speak("Checking for internet service")
    speak("Wait for a moment" + MASTER)
    speak("All drivers are up and running")
    speak("All systems have been activated")
    speak("Now I am online how may I help you" + MASTER)
    strTime = datetime.datetime.now().strftime("%H:%M:%S %p")
    date = datetime.datetime.now().strftime("%m %d %Y")
    speak(f"{MASTER} the time today is {strTime}")
    speak(f"{MASTER} the date today is {date}")
    """

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
        query = "open instagram"

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
                    os.startfile(special_string_processed)
                elif sentence_type == "SAY":
                    speak(special_string_processed)
            # Else, we will create our own block just like the first version of this project.
            elif "what is today's weather" in query.lower():
                speak(f"Today's weather is { weather.getTodayCondition() }")
            elif "wikipedia" in query.lower():
                query = query.replace("wikipedia", "")
                info = wikipedia.summary(query.lower(), sentence=2)

if __name__ == "__main__":
    sentence_execution()
    #main()
