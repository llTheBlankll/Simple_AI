import time

import pydub
import os
import threading

from pydub.playback import play


class Music:
    def __init__(self, song_directory):
        # Check if the directory exists.
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

    def play_song(self, song: str):
        audio_segment = pydub.AudioSegment.from_mp3(song)
        self.is_playing = True
        self.song_duration = audio_segment.duration_seconds
        play(audio_segment)

    def play_music(self):
        for song in os.listdir(self.song_directory):
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
                self.song_thread.run()

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