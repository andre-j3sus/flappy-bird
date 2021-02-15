import pygame
from random import choice
pygame.init()
pygame.display.set_caption("Flappy Bird - by Jesus")

# Constants:
SIZE = WIDTH, HEIGHT = 320, 569
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
FPS = 60
playing = True
font = pygame.font.Font("FlappyBirdy.ttf", 32)

# Images:
bg_img = pygame.image.load("sprites/day_bg.png")
bird0_img = pygame.image.load("sprites/bird0.png")
pipe_img = pygame.image.load("sprites/pipe.png")


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

        # Jump
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.vel_y = -10

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
    space_between_pipes = 180

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

    score = font.render(str(bird.score), True, BLACK)
    screen.blit(score, (WIDTH // 2 - 5, 20))

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
    global playing

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

            # If the game is over and yhe player press the SPACE key -> Restart Game
            if not playing and event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    playing = True
                    bird = Bird(WIDTH // 2, HEIGHT // 2, 0)
                    pipes = [pair_of_pipes()]

    pygame.quit()


main()
