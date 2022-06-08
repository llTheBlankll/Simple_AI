import pyttsx3  # Recognition Voice Function
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import dotenv

# Load the environment variables which is more safe and a good habit rather than loading it directly on the script.
dotenv.load_dotenv(dotenv_path="./config.env")

MASTER = os.getenv("MASTER")

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


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
def takeCommand():
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
        print("Unknown Value ERROR: \n" + e)
    return query


def startup():
    """
    * Removing the long intro. that slows the testing and development.
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


# * Main Program starts here..
def main():
    # speak("Initializing Jarvis...")
    startup()
    wishMe()
    query = takeCommand()

    # Logic for executing  tasks as per the query
    if 'wikipedia' in query.lower():
        speak('Searching wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        print(results)
        speak(results)
    elif 'open youtube' in query.lower():
        url = "youtube.com"
        chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(chrome_path).open(url)

    elif 'open google' in query.lower():
        url = "google.com"
        chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(chrome_path).open(url)

    elif 'open facebook' in query.lower():
        url = "facebook.com"
        chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(chrome_path).open(url)

    elif 'open instagram' in query.lower():
        url = "instagram.com"
        chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(chrome_path).open(url)

    elif 'open twitter' in query.lower():
        url = "twitter.com"
        chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(chrome_path).open(url)

    elif 'open netflix' in query.lower():
        url = "netflix.com"
        chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(chrome_path).open(url)

    elif 'play music' in query.lower():
        songs_dir = "C:\\Users\\63956\\Music\\Musics"
        songs = os.listdir(songs_dir)
        print(songs)
        os.startfile(os.path.join(songs_dir, songs[0]))

    elif 'what time and date today' in query.lower():
        strTime = datetime.datetime.now().strftime("%H:%M:%S %p")
        date = datetime.datetime.now().strftime("%m %d %Y")
        speak(f"{MASTER} the time is {strTime}")
        speak(f"{MASTER} and the date is {date}")

    elif 'open visual code' in query.lower():
        codePath = "D:\\Microsoft VS Code\\Code.exe"
        os.startfile(codePath)

    elif 'open pycharm' in query.lower():
        codePath = "D:\\APPS\\PyCharm Community Edition 2021.3.3\\bin\\pycharm64.exe"
        os.startfile(codePath)


if __name__ == "__main__":
    main()
