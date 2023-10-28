import sounddevice as sd
import numpy as np
import soundfile as sf
import os
import sys

fs_low = 22050
fs_medium = 44100
fs_high = 96000

audio_quality = 'medium'

fs_dict = {
    'low': fs_low,
    'medium': fs_medium,
    'high': fs_high
}

fs = fs_dict[audio_quality]

recorded_data = []

admin_mode = False
user_authenticated = False

admin_username = "admin"
admin_password = "admin123"

folder = False
folder_path = ''  

def audio_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    recorded_data.append(indata.copy())

def start_recording():
    with sd.InputStream(callback=audio_callback, channels=2, samplerate=fs):
        print("Recording Started")
        input("Press 2 to stop recording : ")

def stop_recording():
    print("Recording stopped.")

def play_recorded_audio():
    if recorded_data:
        print("Playing the recorded audio...")
        sd.play(np.concatenate(recorded_data), fs)
        sd.wait()
    else:
        print("No data to play.")

def save_audio(folder_path):
    if recorded_data:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        filename = input("Enter filename: ")
        full_path = os.path.join(folder_path, filename + '.wav') 
        sf.write(full_path, np.concatenate(recorded_data), fs)
        print(f"Audio file saved as {filename + '.wav'} at {os.getcwd()+full_path}")
    else:
        print("No data present to save into a file.")

def set_audio_quality():
    global audio_quality, fs  
    if admin_mode:
        print("Audio Quality Options: low, medium, high")
        new_quality = input("Enter the desired audio quality: ").lower()
        if new_quality in ['low', 'medium', 'high']:
            audio_quality = new_quality
            fs = fs_dict[audio_quality]
            print(f"Audio quality set to {audio_quality}.")
        else:
            print("Invalid quality option.")
    else:
        print("Admin privileges required to set audio quality.")

def login_to_admin_mode():
    global admin_mode, user_authenticated  
    if not admin_mode and not user_authenticated:
        username = input("Enter username: ")
        password = input("Enter password: ")

        if username == admin_username and password == admin_password:
            admin_mode = True
            print("Admin mode enabled.")
        else:
            print("Invalid credentials.")
    else:
        print("You are already logged in.")

def delete_file(folder_path):
    if admin_mode: 
        path = input("Enter the file name to be deleted: ")
        full_path = os.path.join(folder_path, path)
        try:
            os.remove(full_path)
            print(f"{path} deleted successfully")
        except FileNotFoundError:
            print("No such file exists.")
    else:
        print("Admin privileges required to delete files.")
while True:
    choice = int(input(
        "Enter 1 - Start Recording , 2 - Stop/Pause Recording , 3 - Continue Recording , 4 - Play Recorded File , 5 - Save Recording "
        "\n6 - Delete Recorded File, 7 - Set Audio Quality (Admin Only), 8 - Log in To Admin Mode , 9 - Close Voice Recorder : "))

    if choice == 1 or choice == 3:
        start_recording()
    elif choice == 2:
        stop_recording()
    elif choice == 4:
        play_recorded_audio()
    elif choice == 5:
        if not folder_path:
            ch1 = input("Would You Like To Name The Folder Which Contains All The Recording Yourself Y/N : ")
            if (ch1 == 'y' or ch1 == 'Y'):
                folder_path = input("Enter the folder path where you want to save recordings : ").strip()
            else:
                folder_path = 'Recording'
            folder = True

        if not folder_path:
            folder_path = 'Recording'

        save_audio(folder_path)
    elif choice == 6:
        delete_file(folder_path)
    elif choice == 7:
        set_audio_quality()
    elif choice == 8:
        login_to_admin_mode()
    elif choice == 9:
        print("Voice Recorder Closed")
        exit()
    else:
        print("Invalid choice.")
