import pygame
from random import choice
pygame.init()
pygame.display.set_caption("Flappy Bird - by Jesus")

# Constants:
SIZE = WIDTH, HEIGHT = 320, 569
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
FPS = 60
playing = False
menu = True
font = pygame.font.Font("FlappyBirdy.ttf", 32)

# Images:
bg_img = pygame.image.load("sprites/day_bg.png")
title_img = pygame.image.load("sprites/title.png")
game_over_img = pygame.image.load("sprites/game_over.png")
tap_tap_img = pygame.image.load("sprites/tap_tap.png")
bird0_img = pygame.image.load("sprites/bird0.png")
pipe_img = pygame.image.load("sprites/pipe.png")

pygame.display.set_icon(bird0_img)

# Colors:
WHITE = 255, 255, 255
BLACK = 0, 0, 0


class Bird:
    def __init__(self, x, y, score):
        self.x = x
        self.y = y
        self.img = bird0_img
        self.rect = self.img.get_rect(topleft=(self.x - 20, self.y))
        self.width = self.img.get_width()  # 40
        self.height = self.img.get_height()  # 30
        self.vel_y = 0
        self.score = score

    def draw_bird(self):
        screen.blit(self.img, (self.x - self.width // 2, self.y))
        # pygame.draw.rect(screen, WHITE, self.rect, 1)

    def move(self, pipes):
        global playing
        dy = 0

        # Collision with pipes
        for pair in pipes:
            for pipe in pair:
                if self.rect.colliderect(pipe.rect):
                    playing = False

        # Collision with top/bottom of the screen
        if self.rect.bottom >= HEIGHT or self.rect.top <= 0:
            playing = False

        # When it goes through a pair of pipes, gets a point
        if self.x == pipes[0][0].x + pipes[0][0].width//2:
            self.score += 1

        # "GRAVITY"
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # Updating y and rect
        self.y += dy
        self.rect.topleft = (self.x - self.width//2, self.y)


class Pipe:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = pipe_img
        self.rect = self.img.get_rect(topleft=(self.x, self.y))
        self.height = self.img.get_height()
        self.width = self.img.get_width()

    def draw_pipe(self):
        screen.blit(self.img, self.rect)
        # pygame.draw.rect(screen, WHITE, self.rect, 1)

    def move_pipe(self):
        self.x -= 1
        self.rect.topleft = (self.x, self.y)


# Returns a new pipe
def new_pipe():
    possible_y = [HEIGHT // 3, HEIGHT // 2, 3 * HEIGHT // 4]
    return Pipe(WIDTH, choice(possible_y))


# Returns a new pair of pipes
def pair_of_pipes():
    space_between_pipes = 140

    pipe = new_pipe()
    opposite_pipe = Pipe(pipe.x, pipe.y - pipe.height - space_between_pipes)
    opposite_pipe.img = pygame.transform.flip(pipe_img, False, True)

    return pipe, opposite_pipe


def draw_screen(bird, pipes):
    screen.blit(bg_img, (0, 0))
    bird.draw_bird()
    for pair in pipes:
        for pipe in pair:
            pipe.draw_pipe()

    if menu:
        screen.blit(title_img, (WIDTH//2 - title_img.get_width()//2, HEIGHT//5))
    else:
        score = font.render(str(bird.score), True, BLACK)
        screen.blit(score, (WIDTH // 2 - 5, 20))

    # Game over
    if not playing:
        screen.blit(tap_tap_img, (WIDTH // 2 - tap_tap_img.get_width() // 2, HEIGHT // 2 + tap_tap_img.get_height()))

        if not menu:
            screen.blit(game_over_img, (WIDTH // 2 - game_over_img.get_width() // 2, HEIGHT // 5))

    pygame.display.update()


def update_screen(bird, pipes):
    bird.move(pipes)

    for pair in pipes:
        for pipe in pair:
            pipe.move_pipe()
    # Spawning a new pair of pipes
    if pipes[0][0].rect.left <= WIDTH // 5 and len(pipes) == 1:
        pipes.append(pair_of_pipes())

    # Removing the old pair of pipes
    if pipes[0][0].rect.right <= 0:
        pipes.remove(pipes[0])


def main():
    running = True
    global playing, menu

    bird = Bird(WIDTH // 2, HEIGHT // 2, 0)
    pipes = [pair_of_pipes()]

    while running:
        clock.tick(FPS)
        if playing:
            update_screen(bird, pipes)

        draw_screen(bird, pipes)

        for event in pygame.event.get():
            # Close the window
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:  # Jump
                    if not playing:
                        playing = True
                        menu = False
                        bird = Bird(WIDTH // 2, HEIGHT // 2, 0)
                        pipes = [pair_of_pipes()]
                    bird.vel_y = -10

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not playing:  # Jump
                    playing = True
                    menu = False
                    bird = Bird(WIDTH // 2, HEIGHT // 2, 0)
                    pipes = [pair_of_pipes()]
                bird.vel_y = -10

    pygame.quit()


main()
