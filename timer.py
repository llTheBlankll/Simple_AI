import threading
import time
import multiprocessing


def beep():
    print("\a")


class Timer(threading.Thread):
    def __init__(self, timer=0, *args):
        super().__init__()
        self.timer = timer
        self.countdown = 0

        if len(args) >= 1:
            if args[0] == "minutes" or args[0] == "minute":
                self.countdown = timer * 60
            elif len(args) >= 1 and args[0] == "hours" or args[0] == "hour":
                self.countdown = (timer * 60) * 60
            else:
                self.countdown = timer

        self.start_countdown()

    def start_countdown(self):
        print("Timer starting now!")
        for i in range(self.countdown):
            i += 1
            print(i)
            time.sleep(1)

        # Indicator that the Timer is finished.
        # Beep 3x
        for i in range(3):
            beep()
            time.sleep(1)
