import sounddevice as sd
import numpy as np
import soundfile as sf
import os
import sys  # Added to import sys module

recorded_data = []

folder = False
folder_path = ''  # Initialize folder_path
fs=44100
def audio_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    recorded_data.append(indata.copy())
#start recording
def start_recording():
    with sd.InputStream(callback=audio_callback, channels=2, samplerate=fs):
        print("Recording Started")
        input("Press 2 to stop recording : ")
#stop recording 
def stop_recording():
    print("Recording stopped.")
#play recorded audio
def play_recorded_audio():
    if recorded_data:
        print("Playing the recorded audio...")
        sd.play(np.concatenate(recorded_data), fs)
        sd.wait()
    else:
        print("No data to play.")

while True:
    choice = int(input(
        "Enter 1 - Start Recording , 2 - Stop/Pause Recording , 3 - Continue Recording , 4 - Play Recorded File , 5 - Exit" ))

    if choice == 1 or choice == 3:
        start_recording()
    elif choice == 2:
        stop_recording()
    elif choice == 4:
        play_recorded_audio()
    elif choice == 5:
        print("Voice Recorder Closed")
        exit()
        # break
    else:
        print("Invalid choice.")
