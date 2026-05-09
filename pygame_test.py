import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Scaling Circle")

clock = pygame.time.Clock()

running = True
time = 0

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill((30, 30, 30))

    radius = 50 + int(30 * math.sin(time/2))

    pygame.draw.circle(
        screen,
        (255, 255, 255),
        (WIDTH // 2, HEIGHT // 2),
        radius
    )

    pygame.display.flip()

    time += 0.05

    clock.tick(60)

pygame.quit()