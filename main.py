import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

# Bird properties
lind_x = 50
lind_y = 300
lind_width = 40
lind_height = 40
gravity = 0.5
lind_velocity = 0

# Pipe properties
pipe_width = 70
pipe_height = random.randint(150, 550)
pipe_color = (0, 255, 0)
pipe_x = 400
space_between_pipes = 200

# Score
score = 0

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Lind")

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill((0, 0, 0))  # Clear screen

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                lind_velocity = -10

    # Bird movement
    lind_velocity += gravity
    lind_y += lind_velocity

    # Pipe movement
    pipe_x -= 2
    if pipe_x < -pipe_width:
        pipe_x = SCREEN_WIDTH
        pipe_height = random.randint(150, 550)
        score += 1

    # Draw bird
    pygame.draw.rect(screen, (255, 255, 0), (lind_x, lind_y, lind_width, lind_height))

    # Draw pipes
    pygame.draw.rect(screen, pipe_color, (pipe_x, 0, pipe_width, pipe_height))
    pygame.draw.rect(screen, pipe_color, (pipe_x, pipe_height + space_between_pipes, pipe_width, SCREEN_HEIGHT))

    # Collision detection
    if lind_y > SCREEN_HEIGHT - lind_height or lind_y < 0:
        running = False

    if pipe_x < lind_x + lind_width and lind_x < pipe_x + pipe_width:
        if lind_y < pipe_height or lind_y > pipe_height + space_between_pipes:
            running = False

    # Display score
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    pygame.display.update()
    clock.tick(30)

pygame.quit()
