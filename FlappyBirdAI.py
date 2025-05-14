import pygame
import neat
import os
import random

pygame.font.init()

# Constants
WIN_WIDTH = 500
WIN_HEIGHT = 800
GEN = 0
quit_flag = False
hard_mode_enabled = False


# Load Assets
BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))
]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

STAT_FONT = pygame.font.SysFont("comicsans", 50)


# Bird Class
class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        displacement = self.vel * self.tick_count + 1.5 * self.tick_count**2

        if displacement >= 16:
            displacement = 16
        if displacement < 0:
            displacement -= 2

        self.y += displacement

        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1
        img_index = self.img_count // self.ANIMATION_TIME % len(self.IMGS)
        self.img = self.IMGS[img_index]

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


# Pipe Class
class Pipe:
    GAP = 200
    VEL = 5
    MOVE_VEL = 2

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG
        self.passed = False
        self.direction = random.choice([-1, 1])
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        # Horizontal movement
        self.x -= self.VEL

        # Vertical movement if "Hard Move" is enabled
        if hard_mode_enabled:
            self.height += self.MOVE_VEL * self.direction

            # Reverse direction if out of bounds
            if self.height < 50 or self.height > 450:
                self.direction *= -1

            # Update pipe positions
            self.top = self.height - self.PIPE_TOP.get_height()
            self.bottom = self.height + self.GAP

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        return bird_mask.overlap(top_mask, top_offset) or bird_mask.overlap(bottom_mask, bottom_offset)


# Base Class
class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


# Draw Game Window
# Updated Draw Function for AI Mode
def draw_window(win, birds, pipes, base, score, gen, mode="AI"):
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    # Smaller font for Gen and Score
    top_font = pygame.font.SysFont("comicsans", 35)

    # Draw Gen and Score
    gen_text = top_font.render(f"Gen: {gen}", 1, (255, 255, 255))
    score_text = top_font.render(f"Score: {score}", 1, (255, 255, 255))

    win.blit(gen_text, (10, 10))
    win.blit(score_text, (WIN_WIDTH - score_text.get_width() - 10, 10))

    # Draw Quit button (centered between Gen and Score)
    quit_rect = pygame.Rect(WIN_WIDTH // 2 - 50, 10, 100, 40)  # Adjust size and position
    pygame.draw.rect(win, (255, 0, 0), quit_rect, border_radius=10)

    quit_text = top_font.render("Quit", 1, (255, 255, 255))
    quit_text_rect = quit_text.get_rect(center=quit_rect.center)
    win.blit(quit_text, quit_text_rect)

    base.draw(win)

    for bird in birds:
        bird.draw(win)

    pygame.display.update()



# Main Menu
# Main Menu
# Main Menu
def main_menu():
    global hard_mode_enabled
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Flappy Bird")

    # Fonts for title, buttons, and high score
    title_font = pygame.font.SysFont("comicsans", 60)
    button_font = pygame.font.SysFont("comicsans", 30)
    score_font = pygame.font.SysFont("comicsans", 30)

    # Load the high score for manual mode
    manual_high_score = 0
    if os.path.exists("high_score.txt"):
        with open("high_score.txt", "r") as f:
            manual_high_score = int(f.read())

    while True:
        # Draw the background
        win.blit(BG_IMG, (0, 0))

        # Draw the title
        title = title_font.render("Flappy Bird", 1, (255, 255, 255))
        title_rect = title.get_rect(center=(WIN_WIDTH // 2, 100))
        win.blit(title, title_rect)

        # Create buttons
        play_rect = pygame.Rect(WIN_WIDTH // 2 - 100, 300, 200, 60)
        ai_rect = pygame.Rect(WIN_WIDTH // 2 - 100, 400, 200, 60)
        toggle_rect = pygame.Rect(WIN_WIDTH // 2 - 100, 500, 20, 20)

        # Draw buttons with gradient
        pygame.draw.rect(win, (0, 0, 200), play_rect, border_radius=15)
        pygame.draw.rect(win, (200, 0, 0), ai_rect, border_radius=15)

        # Draw button text
        play_text = button_font.render("Play Yourself", 1, (255, 255, 255))
        ai_text = button_font.render("Watch AI Play", 1, (255, 255, 255))
        toggle_text = button_font.render("Hard Mode", 1, (255, 255, 255))

        play_text_rect = play_text.get_rect(center=play_rect.center)
        ai_text_rect = ai_text.get_rect(center=ai_rect.center)
        toggle_text_rect = toggle_text.get_rect(midleft=(toggle_rect.right + 10, toggle_rect.centery))

        win.blit(play_text, play_text_rect)
        win.blit(ai_text, ai_text_rect)
        win.blit(toggle_text, toggle_text_rect)

        # Draw the checkbox
        if hard_mode_enabled:
            pygame.draw.rect(win, (0, 200, 0), toggle_rect)
        else:
            pygame.draw.rect(win, (200, 0, 0), toggle_rect)

        # Draw manual mode high score
        high_score_text = score_font.render(f"High Score: {manual_high_score}", 1, (255, 255, 255))
        high_score_rect = high_score_text.get_rect(center=(WIN_WIDTH // 2, 550))
        win.blit(high_score_text, high_score_rect)

        # Update the display
        pygame.display.update()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if play_rect.collidepoint(pos):
                    manual_mode()
                elif ai_rect.collidepoint(pos):
                    local_dir = os.path.dirname(__file__)
                    config_path = os.path.join(local_dir, "config-NEAT.txt")
                    run(config_path)
                elif toggle_rect.collidepoint(pos):
                    hard_mode_enabled = not hard_mode_enabled  # Toggle the "Hard Move" option




# Manual Mode
def manual_mode():
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(700)]
    score = 0

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()
            if event.type == pygame.MOUSEBUTTONDOWN:
                bird.jump()

        bird.move()
        base.move()

        add_pipe = False
        rem = []
        for pipe in pipes:
            pipe.move()
            if pipe.collide(bird):
                run = False

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

        if add_pipe:
            score += 1
            pipes.append(Pipe(600))

        for r in rem:
            pipes.remove(r)

        if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
            run = False

        draw_window(win, [bird], pipes, base, score, GEN, mode="Manual")


# AI Mode
def ai_mode(genomes, config):
    global GEN, quit_flag
    GEN += 1

    nets = []
    ge = []
    birds = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    base = Base(730)
    pipes = [Pipe(700)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    score = 0

    # Quit button dimensions
    quit_rect = pygame.Rect(WIN_WIDTH // 2 - 50, 10, 100, 30)

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if quit_rect.collidepoint(pos):
                    quit_flag = True  # Set quit flag to True
                    return  # Exit AI mode to stop NEAT execution

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            run = False
            break

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                bird.jump()

        add_pipe = False
        rem = []
        for pipe in pipes:
            pipe.move()
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600))

        for r in rem:
            pipes.remove(r)

        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        base.move()

        # Draw window and quit button
        draw_window(win, birds, pipes, base, score, GEN)
        pygame.draw.rect(win, (255, 0, 0), quit_rect, border_radius=10)
        quit_text = STAT_FONT.render("Quit", 1, (255, 255, 255))
        quit_text_rect = quit_text.get_rect(center=quit_rect.center)
        win.blit(quit_text, quit_text_rect)
        pygame.display.update()


# Run Game
def run(config_path):
    global quit_flag
    quit_flag = False  # Reset quit flag
    config = neat.config.Config(
        neat.DefaultGenome, neat.DefaultReproduction,
        neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path
    )
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run NEAT loop until quit flag is set
    while not quit_flag:
        p.run(ai_mode, 1)

    # Return to main menu after quitting AI mode
    main_menu()


if __name__ == "__main__":
    main_menu()
