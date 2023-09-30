import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import sounddevice as sd
import numpy as np
import soundfile as sf
import os

fs_low = 22050
fs_medium = 44100
fs_high = 96000
admin_username = "admin"
admin_password = "admin123"
audio_quality = 'medium'

fs_dict = {
    'low': fs_low,
    'medium': fs_medium,
    'high': fs_high
}

fs = fs_dict[audio_quality]

recorded_data = []

class VoiceRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Recorder App")

        # Title
        title_label = tk.Label(root, text="Voice Recorder App", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        # Created by Text
        created_by_label = tk.Label(root, text="Created by Saumya Sehgal and Pulkit Kumar", font=("Helvetica", 10))
        created_by_label.pack(pady=5)

        # Functionality Buttons
        self.stream = sd.InputStream(channels=2, samplerate=fs, callback=self.audio_callback)
        self.admin_mode = False
        self.folder_path = ''
        self.filename = ''

        self.start_button = self.create_button("Start Recording", self.start_recording, bg='yellow', width=20, height=2)
        self.start_button.pack(pady=5)

        self.cont_button = self.create_button("Continue Recording", self.continue_recording, bg='yellow', width=20, height=2)
        self.cont_button.pack(pady=5)

        self.stop_button = self.create_button("Stop Recording", self.stop_recording, bg='yellow', width=20, height=2)
        self.stop_button.pack(pady=5)

        self.play_button = self.create_button("Play Recorded Audio", self.play_recorded_audio, bg='yellow', width=20, height=2)
        self.play_button.pack(pady=5)

        self.save_button = self.create_button("Save Recorded Audio", self.save_audio, bg='yellow', width=20, height=2)
        self.save_button.pack(pady=5)

        self.delete_button = self.create_button("Delete File", self.delete_file, bg='yellow', width=20, height=2)
        self.delete_button.pack(pady=5)

        self.set_quality_button = self.create_button("Set Audio Quality", self.set_audio_quality, bg='yellow', width=20, height=2)
        self.set_quality_button.pack(pady=5)

        self.admin_login_button = self.create_button("Login to Admin Mode", self.login_to_admin_mode, bg='yellow', width=20, height=2)
        self.admin_login_button.pack(pady=5)

        # Features Text
        features_text = "Features:\n1) Records Audio\n2) Plays the Audio Recording\n3) Saves the Audio Recording\n4) Deletes the Recording (Allowed by the Admin only)\n5) Sets the Audio Quality (Only allowed by the Admin)"
        features_label = tk.Label(root, text=features_text, font=("Helvetica", 12, "bold"))
        features_label.pack(pady=20)

        # Status Bar
        self.status_bar = tk.Label(root, text="Idle", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_button(self, text, command, **kwargs):
        return tk.Button(self.root, text=text, command=command, **kwargs)

    def audio_callback(self, indata, frames, time, status):
        recorded_data.extend(indata.copy())

    def start_recording(self):
        global recorded_data
        recorded_data = []
        self.stream.start()
        self.update_status("Recording Started")

    def continue_recording(self):
        global recorded_data
        self.stream.start()
        self.update_status("Recording Continued")

    def stop_recording(self):
        self.stream.stop()
        self.update_status("Recording Stopped")

    def play_recorded_audio(self):
        if recorded_data:
            sd.play(np.array(recorded_data), fs)
            sd.wait()
        else:
            self.show_warning("No data to play.")

    def set_audio_quality(self):
        global fs, audio_quality
        if self.admin_mode:
            new_quality = simpledialog.askstring("Audio Quality", "Enter the desired audio quality (low, medium, high):")
            if new_quality and new_quality.lower() in ['low', 'medium', 'high']:
                audio_quality = new_quality.lower()
                fs = fs_dict[audio_quality]
                self.show_info(f"Audio quality set to {audio_quality}.")
            else:
                self.show_error("Invalid quality option.")
        else:
            self.show_error("Admin privileges required to set audio quality.")

    def login_to_admin_mode(self):
        global admin_username, admin_password
        entered_username = simpledialog.askstring("Admin Login", "Enter username:")
        entered_password = simpledialog.askstring("Admin Login", "Enter password:", show='*')

        if entered_username == admin_username and entered_password == admin_password:
            self.admin_mode = True
            self.show_info("Admin mode enabled.")
        else:
            self.show_error("Invalid credentials.")

    def save_audio(self):
        global recorded_data
        if recorded_data:
            self.filename = filedialog.asksaveasfilename(defaultextension=".wav", initialdir=self.folder_path,
                                                        filetypes=[("WAV files", "*.wav")])
            if self.filename:
                sf.write(self.filename, np.array(recorded_data), fs)
                self.show_info(f"Audio file saved as {os.path.basename(self.filename)} at {os.path.dirname(self.filename)}")
        else:
            self.show_warning("No data present to save.")

    def delete_file(self):
        if self.admin_mode:
            file_to_delete = filedialog.askopenfilename(initialdir=self.folder_path, title="Select file to delete",
                                                        filetypes=[("All files", "*.*")])
            if file_to_delete:
                try:
                    os.remove(file_to_delete)
                    self.show_info(f"File deleted successfully at {os.path.dirname(file_to_delete)}")
                except FileNotFoundError:
                    self.show_error("File not found.")
        else:
            self.show_warning("Admin Privileges Required To Delete Files")

    def show_info(self, message):
        messagebox.showinfo("Info", message)

    def show_warning(self, message):
        messagebox.showwarning("Warning", message)

    def show_error(self, message):
        messagebox.showerror("Error", message)

    def update_status(self, message):
        self.status_bar.config(text=message)


if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceRecorderApp(root)
    root.mainloop()
