import pyaudio
import wave
import keyboard
import time

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
OUTPUT_FILENAME = "AudioFile.wav"

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

frames = []
print("Press SPACE to start")
keyboard.wait("space")
print("Rec...")
time.sleep(0.2)

while True:
    data = stream.read(CHUNK)
    frames.append(data)
    if keyboard.is_pressed("space"):
        print("rec stopping")
        time.sleep(0.2)
        break

stream.stop_stream()
stream.close()
audio.terminate()

wf = wave.open(OUTPUT_FILENAME, 'wb')  
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

import speech_recognition as sr

filename = "AudioFile.wav"

r = sr.Recognizer()

with sr.AudioFile(filename) as source:
    audio_data = r.record(source)
    text = r.recognize_google(audio_data)
    print(text)