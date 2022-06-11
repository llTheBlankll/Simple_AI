import multiprocessing
import threading
import time
import pyttsx3
import dotenv

# Initialize configuration environment
config = dotenv.dotenv_values(dotenv_path="./config.env")

# Initialize Text to Speech.
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

# Initialize variables
beeps: int = int(config["BEEPS"])


def speak(sentence: str):
    engine.say(sentence)
    engine.runAndWait()


def Tuple_getValueIndex(value: str, tup: list) -> object or int:
    """
    Get the index (int) of a value in a list.

    @param value: "value 2"
    @param tup: ["value 0", "value 1", "value 2", "value "3]
    @return: 2
    """
    count = 0

    i: str  # Variable Hint
    for i in tup:
        if i.lower() == value.lower():
            return count
        else:
            count += 1

    # Return None if nothing is found.
    return None


class Timer(threading.Thread):
    def __init__(self, words: list):
        """
        Takes the countdown in a sentence form.
        Ex:
        "set timer for 1 hour and 30 minutes"
        This will convert the sentence into countdown seconds which is a total of 5,400 seconds as shown above.
        an hour is equal to 3,600 seconds and 30 minutes is 1,800 seconds so if we add these two, the result will be 7,200 seconds total.
        or
        "1 hour and 30 seconds"
        which is a total of 3630 seconds.

        @param words:
        """
        super().__init__()
        self.countdown_process = multiprocessing.Process()

        if len(words) >= 1:
            try:
                # Try singular form
                hour_index = Tuple_getValueIndex("hour", words) if "hour" or "hours" in words else None
                minute_index = Tuple_getValueIndex("minute", words) if "minute" and "minutes" in words else None
                second_index = Tuple_getValueIndex("second", words) if "second" and "seconds" in words else None

                # Try plural form
                if hour_index is None:
                    hour_index = Tuple_getValueIndex("hours", words) if "hour" or "hours" in words else None

                if minute_index is None:
                    minute_index = Tuple_getValueIndex("minutes", words) if "minute" and "minutes" in words else None

                if second_index is None:
                    second_index = Tuple_getValueIndex("seconds", words) if "second" and "seconds" in words else None

                hour_value = int(words[hour_index - 1]) if hour_index is not None else 0
                minute_value = int(words[minute_index - 1]) if minute_index is not None else 0
                second_value = int(words[second_index - 1]) if second_index is not None else 0
                # Example:
                # If the query is:
                # set timer for 1 hour and 30 minutes.
                # the hour_value would be '1' and the minute value will '30'
                self.countdown = second_value + (60 * minute_value) + (3600 * hour_value)
            except TypeError as e:
                print(e)
                speak("Make sure you spoke the words and numbers correctly.")
                exit(0)
        else:
            try:
                self.countdown = int(words[0])
            except TypeError:
                pass

    def __countdown__(self):
        """
        This function should be called with Process or a Thread.
        This function initiate and the countdown and its internal mechanism.
        @return: None
        """
        for i in range(self.countdown):
            i += 1
            self.countdown -= 1
            time.sleep(1)

        # If the countdown is finished, beep for 1 time every second until 5 beeps.
        if self.countdown <= 0:
            for i in range(beeps):
                print("\a")
                time.sleep(1)

    def start_countdown(self):
        """
        Start the countdown by using "time.sleep" and subtracting "self.countdown" by 1 every second.
        @return: None
        """
        self.countdown_process = multiprocessing.Process(target=self.__countdown__(), args=(self.countdown,))

    def stop_countdown(self):
        """
        Basically stopping the Process because the "self.countdown" is already got subtracted, so we can continue
        where we left off.
        @return: None
        """
        if self.countdown_process.is_alive():
            self.countdown_process.terminate()
        else:
            speak("Countdown has not started yet.")
            print("Countdown has not started yet.")

    def resume_countdown(self):
        """
        Alias of start_countdown()
        @return: None
        """
        self.countdown_process = multiprocessing.Process(target=self.__countdown__(), args=(self.countdown,))


# test("set timer for 2 hours and 30 minutes".split(" "))
Timer("1 seconds".split(" ")).start_countdown()
