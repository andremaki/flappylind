import pygame
import random

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

lind_x = 50
lind_y = 300
lind_width = 40
lind_height = 40
gravity = 0.8
lind_velocity = 0

pipe_width = 70
pipe_color = (0, 255, 0)
space_between_pipes = 200

score = 0

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Lind")

running = True
clock = pygame.time.Clock()

passed_pipe = False

class Pipe:
    def __init__(self, x, height):
        self.x = x
        self.height = height
        self.width = pipe_width

pipes = []
initial_pipe_count = 6
pipe_spacing = 300
for i in range(initial_pipe_count):
    new_pipe = Pipe(400 + i * pipe_spacing, random.randint(150, 450))
    pipes.append(new_pipe)

while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                lind_velocity = -10

    lind_velocity += gravity
    lind_y += lind_velocity



    for pipe in pipes:
        pipe.x -= 8

    if pipes[0].x < -pipe_width:
        pipes.pop(0)
        new_pipe = Pipe(pipes[-1].x + pipe_spacing, random.randint(150, 450))
        pipes.append(new_pipe)
        passed_pipe = False

    for pipe in pipes:
        if not passed_pipe and lind_x > pipe.x + pipe.width:
            passed_pipe = True
            score += 1

    for pipe in pipes:
        pygame.draw.rect(screen, pipe_color, (pipe.x, 0, pipe.width, pipe.height))
        pygame.draw.rect(screen, pipe_color, (pipe.x, pipe.height + space_between_pipes, pipe.width, SCREEN_HEIGHT))

    if lind_y > SCREEN_HEIGHT - lind_height or lind_y < 0:
        running = False

    for pipe in pipes:
        if lind_x + lind_width > pipe.x and lind_x < pipe.x + pipe.width:
            if lind_y < pipe.height or lind_y + lind_height > pipe.height + space_between_pipes:
                running = False

    pygame.draw.rect(screen, (255, 255, 0), (lind_x, lind_y, lind_width, lind_height))

    font = pygame.font.SysFont(None, 100)
    text = font.render(f"{score}", True, (255, 255, 255))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 80))
    screen.blit(text, text_rect)

    pygame.display.update()
    clock.tick(30)

pygame.quit()
