import pyaudio
import wave
import keyboard
import time
import speech_recognition as sr
import os
from google import genai
import pyttsx3

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
client = genai.Client(api_key=GEMINI_API_KEY)

recording = False

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
OUTPUT_FILENAME = "AudioFile.wav"

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

history = []
frames = []
print("Press SPACE to start")
keyboard.wait("space")
print("Rec...")
time.sleep(0.2)

def stopRec(frames):
    stream.stop_stream()

    wf = wave.open(OUTPUT_FILENAME, 'wb')  
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    frames = []

def Speach_To_Text():
    r = sr.Recognizer()

    with sr.AudioFile(OUTPUT_FILENAME) as source:
        audio_data = r.record(source)
        question = r.recognize_google(audio_data)
        print(f"question {question}")
        return question
    
def query_Ai(promt):

    promt = f"you are a JARVIS style robotic assistant, and you have been asked the question: {promt}. give a very short response"
    history.append({"role": "user", "parts": [{"text": promt}]})
    print("Javis responding")
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=history
    )
    history.append({"role": "model", "parts": [{"text": response.text}]})
    answer = response.text.replace("*","")
    print(f"response {answer}")
    return answer

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

while True:

    if keyboard.is_pressed("q"):
        break

    if keyboard.is_pressed("space") and not recording:
        stream.start_stream()
        recording = True

    if recording:
        data = stream.read(CHUNK)
        frames.append(data)

        if not keyboard.is_pressed("space"):

            recording = False
            print("rec stopping")
            stopRec(frames)
            question = Speach_To_Text()
            if question == "":
                answer = "how can i assist you"
            else:
                answer = query_Ai(question)
            speak(answer)

stream.close()
audio.terminate()