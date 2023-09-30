#import required libraries 
import sounddevice as sd
from scipy.io.wavfile import write 
import wavio as wv
import numpy as np
#Sampling Frequency 
freq=44100
#Recording Duration
#Any duration in Seconds can be given 
duration=10 #duration for 10 sec given 
#Start recorder with the given values 
#of duration and the sample frequency 
recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)
#Record  audio for the given number of seconds 
sd.wait()   # Wait until recording is finished
#this will convert the numpy array to an audio 
#file with the given sampling frequency 
write("recording0.wav",freq,recording)
#Convert the NumPy array to audio file 
wv.write("recording1.wav",recording,freq,sampwidth=2)

