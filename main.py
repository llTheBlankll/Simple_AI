import datetime
import json  # Manipulating JSON Format files.
import os  # Manipulating and opening files.
import subprocess

import win10toast  # Displaying Notification
import dotenv  # loading Configuration
import pyttsx3  # Recognition Voice Function
import requests  # For API
import speech_recognition as sr  # Voice Recognition and commands
import wikipedia  # Dictionary and definitions.

# User Music manipulate.
from modules.music import Music

# Getting Weather Conditions.
from modules.weather import Weather

# For setting up Timer
from modules.timer import Timer

# Load the environment variables file which is more safe and a good habit rather than loading it directly on the script.
dotenv.load_dotenv(dotenv_path="./config.env")

# Assign variables.
MASTER = os.getenv("MASTER")

# File paths for file reading.
special_text_list_file = os.getenv("SPECIAL_TEXT_LIST")
sentences_logic_file = os.getenv("SENTENCES_LOGIC_FILE")
todolist_file = os.getenv("TODOLIST_FILE")

# * Initialize Speech to Text.
engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# * Modules Startup
mod_weather = Weather(os.getenv("WEATHER_API"))
mod_music = Music(os.getenv("MUSIC_BASE_DIRECTORY"))
toast = win10toast.ToastNotifier()


def speak(text):
    """
    Read the word or sentence by AI.
    Basically, Text to speech.
    Parameters
    ----------
    text: string
    """
    engine.say(text)
    engine.runAndWait()


def wishMe():
    """
    Greet the user for the first launch/run.

    Returns
    -------
    None
    """
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning" + MASTER)
    elif 12 <= hour < 18:
        speak("Good Afternoon" + MASTER)
    else:
        speak("Good Evening" + MASTER)


def takeCommand() -> str or None:
    """
    Speech to text,
    This will read what you are saying and convert it into text to your language.

    Returns
    -------
    None: if the user said nothing for a period of time.
    str : Is what the user said to the microphone.
    """
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
    """
    In the special_text.json, this will replace the meaning of special symbols or text like '<CHROME_EXE>',
    with a type of
    'VAR_ENVIRONMENT'
    This means that it will take the value from the 'config.env' which is 'CHROME_EXE'.
    In the 'config.env', there's a key CHROME_EXE and the value of the key is the path of the Google Chrome executable file.
    Like this -> 'C:\Program Files\Google\Chrome\Application\chrome.exe'

    [
      {
        "name": "<CHROME>",
        "data": "CHROME_EXE",
        "type": "VAR_ENVIRONMENT"
      },
      {
        "name": "<VSCODE_EXE>",
        "data": "VSCODE_EXE",
        "type": "VAR_ENVIRONMENT"
      },
      {
        "name": "<GITHUB_PROFILE>",
        "data": "GITHUB_PROFILE",
        "type": "VAR_ENVIRONMENT"
      }
    ]

    and the 'config.env'
    ====
    PYCHARM_EXE="C:\Program Files\JetBrains\PyCharm Community Edition 2022.1.2\bin\pycharm64.exe"
    VSCODE_EXE="C:\Program Files\Microsoft VS Code\Code.exe"
    CHROME_EXE="C:\Program Files\Google\Chrome\Application\chrome.exe"
    ====

    Parameters
    ----------
    value: str = the value should be in special_text.json in a key called "name".

    Returns
    -------
    if the parameter value is "<CHROME>" and if it exists in 'special_text.json',
    then using the key called "data" from the file which has the value of 'CHROME_EXE' that exists in 'config.env',
    it will return the data from the value of CHROME_EXE in 'config.env'
    """
    with open(special_text_list_file, "r") as csp:
        data = json.load(csp)

        for json_object in data:
            for keys, content in json_object.items():
                if keys == "name" and content in value:
                    value = value.replace(json_object["name"], os.getenv(json_object["data"]) if json_object[
                                                                                                     "type"] == "VAR_ENVIRONMENT" else
                    json_object["data"])
                    value = value.replace("\\", "/")
                    break
        return value


def sentence_execution():
    """
    Execute voice commands.
    I will update this function documentation in the future.

    Returns
    -------
    None
    """
    with open(sentences_logic_file, "r") as sentences:
        data = json.load(sentences)

        query = takeCommand().lower()

        if query == "" or query is None:
            return

        for sentence_object in data:
            sentence = sentence_object["sentence"]
            sentence_execute = sentence_object["execute"]
            sentence_type = sentence_object["type"]
            # * This if condition will be used if we are executing applications or only for the AI Speaking.
            if sentence in query:
                # If the query has been sentenced similar to this,
                # the code according to the meaning of the sentence is called.
                special_string_processed = special_string_replace(sentence_execute)

                # START_FILE: This will start the files like Chrome executable or Visual Studio Code with or without argument.
                # SAY: Use the speak() function to say.
                if sentence_type == "START_FILE":
                    #  os.system(special_string_processed)
                    subprocess.Popen(special_string_processed.split(" "))
                    break
                elif sentence_type == "SAY":
                    speak(special_string_processed)
                    break
            # Else, we will create our own block just like the first version of this project.
            elif "what is today's weather" in query:
                speak(f"Today's weather is {mod_weather.get_today_condition()}")
                print(f"Today's weather is {mod_weather.get_today_condition()}")
                break
            elif "wikipedia" in query:
                query = query.replace("wikipedia", "")
                try:
                    info = wikipedia.summary(query, sentences=2)
                except wikipedia.exceptions.PageError:
                    speak("No matching page in Wikipedia.")
                    return
                speak(info)
            elif ("play music" in query) or ("play song" in query):
                mod_music.play_music()
                break
            elif ("stop music" in query) or ("stop song" in query):
                mod_music.stop_music()
                break
            elif ("replay music" in query) or ("replay song" in query):
                mod_music.replay_music()
                break
            elif "my ip address" in query:
                toast.show_toast("IP Address", requests.get("https://api.ipify.org/").text)
                break
            elif "set timer" in query:
                # Start a Timer
                Timer(query.split(" ")).start_countdown()
                break


if __name__ == "__main__":
    while True:
        sentence_execution()
    # main()
