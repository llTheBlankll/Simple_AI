import time
import os
import \
    multiprocessing  # Separating the Process between main and music so that we can continue executing voice commands.
import mutagen.mp3  # Getting the duration of the song.
import threading
import playsound

class Music(threading.Thread):
    def __init__(self, song_directory):
        # Check if the directory exists.
        super().__init__()
        if not os.path.exists(song_directory):
            print("Music Folder doesn't exist. Please configure it on config.env")
            exit(1)

        # Strings
        self.song_directory = song_directory
        self.previous_song = ""

        # Booleans
        self.is_playing = False

        # Threads
        self.song_thread = threading.Thread()

        # Integers
        self.song_duration = 0  # Seconds. Its value will be assigned later.

        # Debugging
        print("Song Directory: " + self.song_directory)
        count: int = 0
        for song in os.listdir(self.song_directory):
            print(str(count) + ". Song found: " + song.replace(".mp3", ""))
            count += 1

    def play_song(self, song: str):
        try:
            print(self.song_directory + "\\" + song)
            song_path = self.song_directory + "\\" + song
            self.is_playing = True
            self.song_duration = mutagen.mp3.MP3(self.song_directory + "\\" + song).info.length

            # Playing the entire duration of song.
            # block parameter is used to keep the program running and not stop during the song.
            playsound.playsound(song_path, block=True)
            print("I CAN STILL CONTINUE!!!")
        except FileNotFoundError:
            print(f"File {song} not found.")
            time.sleep(1)
            return
        except KeyboardInterrupt:
            print("Song Stopped.")
            return

    def play_music(self):
        song_directory = os.listdir(self.song_directory)
        song_directory.remove("desktop.ini")
        for song in song_directory:
            self.song_thread = threading.Thread(target=self.play_song, args=(song,))
            if self.is_playing:
                try:
                    print("Playing...")
                    time.sleep(self.song_duration)
                    print(f"Song {song} is finished playing.")
                    print(f"Playing next song...")
                except KeyboardInterrupt:
                    print("Stopping Song...")
                    time.sleep(0.5)
                    print("Song stopped.")
                    self.song_thread.join()
            else:
                print(f"Play the first song {song}")
                self.song_thread.run()
                print("Song started!")
                time.sleep(self.song_duration)

    def stop_music(self):
        if self.song_thread is not None:
            self.song_thread.join()
        else:
            print("No music is playing.")

    def replay_music(self):
        # If you're in first song, return.
        if self.previous_song == "" or self.previous_song is None:
            print("You are just currently playing your first song, please finish it first.")
            time.sleep(1)
            return

        if self.song_thread.is_alive():
            print("There is a song playing, stopping it...")
            self.stop_music()
            print("Success! Playing the previous music.")
            self.play_song(self.previous_song)
