import datetime
import json  # Manipulating JSON Format files.
import os  # Manipulating and opening files.
import win10toast  # Displaying Notification
import dotenv  # loading Configuration
import pyttsx3  # Recognition Voice Function
import requests
import speech_recognition as sr  # Voice Recognition and commands
import wikipedia  # Dictionary and definitions.

# User Music manipulate.
from music import Music

# Getting Weather Conditions.
from weather import Weather

# Load the environment variables file which is more safe and a good habit rather than loading it directly on the script.
dotenv.load_dotenv(dotenv_path="./config.env")

MASTER = os.getenv("MASTER")

engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# * Modules Startup
mod_weather = Weather(os.getenv("WEATHER_API"))
mod_music = Music(os.getenv("MUSIC_BASE_DIRECTORY"))
toast = win10toast.ToastNotifier()


# Speak Function
def speak(text):
    engine.say(text)
    engine.runAndWait()


# This function will speak or greet you
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning" + MASTER)
    elif 12 <= hour < 18:
        speak("Good Afternoon" + MASTER)
    else:
        speak("Good Evening" + MASTER)


# This function will take command from Microphone
def takeCommand() -> str:
    query = ""  # To prevent local variable referenced before assignment.
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        """
        That got you a little closer to the actual phrase, but it still isn’t perfect.
        Also, “what” is missing from the beginning of the phrase. Why is that?
        """
        r.adjust_for_ambient_noise(source=source, duration=0.25)
        audio = r.listen(source, timeout=5)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-us')
        print(f"user said: {query}\n")
    except sr.WaitTimeoutError:
        pass
    except sr.UnknownValueError:
        pass

    return query if query is not None or query != "" else exit(1)


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
    # Temporarily disabled for testing and development.
    # query = takeCommand()

    with open("sentences_logic.json", "r") as sentences:
        data = json.load(sentences)

        # query = takeCommand().lower()
        query = takeCommand()

        if query == "" or query is None:
            print("Waiting for Voice Command.")
            return

        for sentence_object in data:
            sentence = sentence_object["sentence"]
            sentence_execute = sentence_object["execute"]
            sentence_type = sentence_object["type"]
            # * This if condition will be used if we are executing applications or only for the AI Speaking.
            if sentence in query.lower():
                # If the query has sentence similarity from this,
                # the code according to the meaning of the sentence is called.
                special_string_processed = special_string_replace(sentence_execute)

                # START_FILE: This will start the files like Chrome executable or Visual Studio Code with or without argument.
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
                print(f"Today's weather is {mod_weather.getTodayCondition()}")
                break
            elif "wikipedia" in query.lower():
                query = query.replace("wikipedia", "")
                try:
                    info = wikipedia.summary(query.lower(), sentences=2)
                except wikipedia.exceptions.PageError:
                    speak("No matching page in Wikipedia.")
                    return
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
            elif "my ip address" in query.lower():
                toast.show_toast("IP Address", requests.get("https://api.ipify.org/").text)
                break
            elif "set timer" in query.lower():
                break


if __name__ == "__main__":
    while True:
        sentence_execution()
    # main()
