import pygame
import math
import numpy as num
import pyaudio
import sys
import numpy as np
import keyboard

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Listening Circle")

clock = pygame.time.Clock()

p = pyaudio.PyAudio()

stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK
)

running = True
time = 0

smoothed_rms = 0
alpha = 0.03

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill((30, 30, 30))

    data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)

    rms = np.mean(data.astype(np.float32)**2)

    if np.isnan(rms):
        rms = 0

    smoothed_rms = (alpha * rms) + (1 - alpha) * smoothed_rms
    smoothed_rms = min(smoothed_rms/130 , 200)
        
    print("Volume:", str(smoothed_rms))

    radius = 50 + int(smoothed_rms)
    if radius < 70:
        radius = 70

    pygame.draw.circle(
        screen,
        (255, 255, 255),
        (WIDTH // 2, HEIGHT // 2),
        radius
    )

    pygame.display.flip()

    time += 0.05

    if (keyboard.is_pressed("space")):
        running = False

    clock.tick(60)

pygame.quit()
stream.stop_stream()
stream.close()
p.terminate()
