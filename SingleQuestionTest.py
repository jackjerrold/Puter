import pyaudio
import wave
import keyboard
import time
import speech_recognition as sr
import os
from google import genai
import pyttsx3

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

r = sr.Recognizer()

with sr.AudioFile(OUTPUT_FILENAME) as source:
    audio_data = r.record(source)
    question = r.recognize_google(audio_data)
    print(f"question {question}")

history = []
def query(prompt):
    history.append({"role": "user", "parts": [{"text": prompt}]})
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=history
    )
    history.append({"role": "model", "parts": [{"text": response.text}]})
    return response.text

print("API initilising...")

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
client = genai.Client(api_key=GEMINI_API_KEY)
print("API started")
response = query(f"you are a JARVIS style robotic assistant, and you have been asked the question: {question}. give a very short response")
response.replace("*","")
print(f"response {response}")

time.sleep(0.5)
engine = pyttsx3.init()
engine.say(response)
engine.runAndWait()