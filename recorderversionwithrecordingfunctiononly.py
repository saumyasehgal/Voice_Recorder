import sounddevice as sd
import numpy as np
import wave

def record_audio(filename, duration, samplerate=44100):
    print("Recording...")
    audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=2, dtype=np.int16)
    sd.wait()
    print("Recording complete.")

    # Save the recorded audio to a WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(audio_data.tobytes())

if __name__ == "__main__":
    output_file = "recorded_audio.wav"
    recording_duration = 5  # in seconds

    record_audio(output_file, recording_duration)
