import pygame
import random

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Lind")

background_image = pygame.image.load('pildid/cityreflection1.png').convert()
background_width = background_image.get_width()
background_x1 = 0
background_x2 = background_width

lind_image = pygame.image.load('pildid/lennuk.png')
lind_width = 100
lind_height = 100
lind_image = pygame.transform.scale(lind_image, (lind_width, lind_height))

lind_x = 50
lind_y = 300
lind_rect = lind_image.get_rect(topleft=(lind_x, lind_y))
lind_mask = pygame.mask.from_surface(lind_image)

lind_velocity = 0
gravity = 0.7

pipe_image = pygame.image.load('pildid/image-removebg-preview.png')
pipe_width = 140
space_between_pipes = 200

score = 0

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Lind")

running = True
clock = pygame.time.Clock()

time_since_last_increase = 0
speed_increase_interval = 5000
pipe_speed = 4

class Pipe:
    def __init__(self, x, height):
        self.x = x
        self.height = height
        self.width = pipe_width
        self.passed = False
        self.image_upper = pygame.transform.scale(pipe_image, (pipe_width, height))
        self.image_lower = pygame.transform.scale(pipe_image, (pipe_width, SCREEN_HEIGHT - height - space_between_pipes))
        self.rect_upper = pygame.Rect(x, 0, pipe_width, height)
        self.rect_lower = pygame.Rect(x, height + space_between_pipes, pipe_width, SCREEN_HEIGHT - height - space_between_pipes)
    
    def create_mask(self):
        combined_surface = pygame.Surface((self.width, SCREEN_HEIGHT), pygame.SRCALPHA)
        combined_surface.blit(self.image_upper, (0, 0))
        combined_surface.blit(self.image_lower, (0, self.height + space_between_pipes))
        return pygame.mask.from_surface(combined_surface)

pipes = []
initial_pipe_count = 5
pipe_spacing = 300
for i in range(initial_pipe_count):
    new_pipe = Pipe(400 + i * pipe_spacing, random.randint(150, 450))
    pipes.append(new_pipe)

while running:
    background_x1 -= 2
    background_x2 -= 2
    if background_x1 <= -background_width:
        background_x1 = background_width
    if background_x2 <= -background_width:
        background_x2 = background_width

    screen.blit(background_image, (background_x1, 0))
    screen.blit(background_image, (background_x2, 0))

    dt = clock.tick(30)
    time_since_last_increase += dt

    if time_since_last_increase >= speed_increase_interval:
        pipe_speed += 0.2
        time_since_last_increase = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                lind_velocity = -10

    lind_velocity += gravity
    lind_y += lind_velocity
    lind_rect.topleft = (lind_x, lind_y)

    for pipe in pipes:
        pipe.x -= pipe_speed
        pipe.mask = pipe.create_mask()

        if not pipe.passed and lind_x > pipe.x + pipe.width:
            pipe.passed = True
            score += 1

        if pipes[0].x < -pipe_width:
            pipes.pop(0)
            new_pipe = Pipe(pipes[-1].x + pipe_spacing, random.randint(150, 450))
            pipes.append(new_pipe)

        screen.blit(pipe.image_upper, (pipe.x, 0))
        screen.blit(pipe.image_lower, (pipe.x, pipe.height + space_between_pipes))

        offset_x = pipe.x - lind_rect.left
        offset_y = 0 - lind_rect.top

        if lind_mask.overlap(pipe.mask, (offset_x, offset_y)):
            running = False
            break

    if lind_y > SCREEN_HEIGHT - lind_height or lind_y < 0:
        running = False

    screen.blit(lind_image, (lind_x, lind_y))

    font = pygame.font.SysFont(None, 90)
    text = font.render(f"{score}", True, (255, 255, 255))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 70))
    screen.blit(text, text_rect)

    pygame.display.update()

pygame.quit()
