import pyaudio
import wave
import keyboard
import time
import speech_recognition as sr
import os
from google import genai
from openai import OpenAI
import pyttsx3
import pygame
import numpy as np

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
ORK = os.environ["OR_API_KEY"]
client = genai.Client(api_key=GEMINI_API_KEY)

print("Gemini key exists:", GEMINI_API_KEY is not None)
print("OpenRouter key exists:", ORK is not None)

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jarvis")

client1 = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key= ORK,
        default_headers={
        "HTTP-Referer": "http://localhost",
        "X-Title": "Jarvis"
}
        )

clock = pygame.time.Clock()

smoothed_rms = 0
alpha = 0.03

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

def stopRec(frames):

    wf = wave.open(OUTPUT_FILENAME, 'wb')  
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    frames = []

def Speach_To_Text():
    r = sr.Recognizer()

    try:
        with sr.AudioFile(OUTPUT_FILENAME) as source:
            audio_data = r.record(source)
            question = r.recognize_google(audio_data)
            print(f"question: {question}")
            return question
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""
    except Exception as e:
        print("Speech error:", e)
        return ""
    
def query_Ai(question):

    promt = f"you are a JARVIS style robotic assistant, our recent conversation history: {history}. I just asked: {question}. give a very short response"
    print("Javis responding...")
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=promt
        )
    except Exception as e:
        print(f"Gemini failed. Report: {e}.")

        response = client1.chat.completions.create(
            model="deepseek/deepseek-chat-v3-0324:free",
            messages=[
            {
                "role": "user",
                "content": promt
            }
            ]
        )
        answer = response.choices[0].message.content


    answer = response.text.replace("*","")
    history.append(f"ME: {question} && YOU: {answer}.")
    history[:] = history[-6:]
    print(f"response: {answer}")
    return answer

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def draw_GUI(radius):

    screen.fill((30, 30, 30))

    pygame.draw.circle(
            screen,
            (255, 255, 255),
            (WIDTH // 2, HEIGHT // 2),
            radius
        )

    clock.tick(60)

    pygame.display.flip()

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    radius = 80

    if keyboard.is_pressed("q"):
        break

    if keyboard.is_pressed("space") and not recording:
        recording = True

    if recording:

        data = stream.read(CHUNK, exception_on_overflow=False)
    
        val = np.frombuffer(data, dtype=np.int16)
        rms = np.sqrt(np.mean(val.astype(np.float32) ** 2))

        if np.isnan(rms):
            rms = 0

        display_rms = min(rms/25, 200)
        radius = 70 + int(display_rms)

        if radius < 80:
            radius = 80

        frames.append(data)

        if not keyboard.is_pressed("space"):

            recording = False
            print("rec stopping.")
            stopRec(frames)
            frames = []
            question = Speach_To_Text()
            if question == "":
                answer = "I did not understand that"
            else:
                answer = query_Ai(question)
            speak(answer)

    draw_GUI(radius)

stream.stop_stream()
stream.close()
audio.terminate()
pygame.quit()

