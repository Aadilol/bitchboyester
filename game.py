import pygame
import os
import random

pygame.init()

# Game window dimensions
screen_width = 600
screen_height = 400

# Create game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Esters Figs")

# Set frame rate
clock = pygame.time.Clock()
FPS = 60

# Game variables
gravity = 1
max_amount = 4
game_over = False
score = 0
fade_counter = 0

# Make sure no errors are created when the score text file doesn't exist because the game wasn't played multiple times yet
if os.path.exists("score.txt"):
  with open("score.txt", "r") as file:
    high_score = int(file.read())
else:
  high_score = 0

# Define colour variables
white = (255,255,255)
black = (150, 20, 50)
panel = (120, 217, 130)

# Define font variables
font_small = pygame.font.SysFont("Lucida Sans", 30)
font_big = pygame.font.SysFont("Boucherie Block", 40)
font_title = pygame.font.SysFont("Boucherie Block", 48)

# Define regular time intervals for poop spawn rate
lowest_time = 4000
highest_time = 6000

# Variables for tracking time intervals
fig_spawn_time = pygame.time.get_ticks()
fig_spawn_interval = random.randint(2000, 4000)  # Random interval between 2 to 4 seconds
poop_spawn_time = pygame.time.get_ticks()
poop_spawn_interval = random.randint(lowest_time, highest_time)
# Load ester
ester_img = pygame.transform.scale(pygame.image.load("assets/ester.png"), (20, 30)).convert_alpha()

# Load background
bg_img = pygame.transform.scale(pygame.image.load("assets/background.png"), (600, 400)).convert_alpha()

# Load title screen
title_img = pygame.transform.scale(pygame.image.load("assets/title_screen.png"), (600, 400)).convert_alpha()

# Load figs
fig_img = pygame.transform.scale(pygame.image.load("assets/fig.png"), (60, 60)).convert_alpha()

# Load bird poop
poop_img = pygame.transform.scale(pygame.image.load("assets/poop.png"), (20, 20)).convert_alpha()

# Function for outputing text onto the screen
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

# Function for drawing info panel
def draw_panel():
  pygame.draw.rect(screen, panel, (0, 0, screen_width, 20))
  pygame.draw.line(screen, white, (0, 20), (screen_width, 20), 1)
  draw_text("SCORE: " + str(score), font_small, white, 0, 0)

# Function for drawing the background
def draw_bg():
  screen.blit(bg_img, (0,0))

# Create sprite groups
fig_group = pygame.sprite.Group()
poop_group = pygame.sprite.Group()

# Create the player class
class Player:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(ester_img, (45, 60))
        self.width = 20
        self.height = 30
        self.rect = pygame.Rect(0, 0, self.width + 22, self.height + 28)
        self.rect.center = (x, y)
        self.flip = False

    def move(self):
        # Reset variables
        dx = 0

        # Processes for keypresses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            dx = -5
            # Flip the player when moving left
            self.flip = False
        if keys[pygame.K_d]:
            dx = 5
            self.flip = True

        # Ensure player doesn't go off the edge of the screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right

        # Update rectangle position
        self.rect.x += dx

        # Check collision with fig
        for fig in fig_group:
            if self.rect.colliderect(fig.rect):
                fig.kill()
                global score
                score = score + 1

        # Check collision with poop
        for poop in poop_group:
            if self.rect.colliderect(poop.rect):
                poop.kill()
                global game_over
                game_over = True

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 8, self.rect.y - 5))
        pygame.draw.rect(screen, white, self.rect, 2)

# Figs class
class Figs(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity):
        super().__init__()
        self.image = fig_img
        self.velocity = velocity
        self.rect = self.image.get_rect()
        self.vel_y = 1
        self.rect.x = x
        self.rect.y = y

    def update(self):
        # Remove the fig if it reaches the bottom of the screen
        if self.rect.y > 300:
            self.kill()
            # Generate new fig outside the screen
            self.rect.y = 0
            self.rect.x = random.randint(20, screen_width - 20)

        # Move the fig down
        self.rect.y += self.vel_y

        # Generate figs
        if len(fig_group) < max_amount:
            # Add a new fig instance to the fig_group
            fig_group.add(Figs(random.randint(20, screen_width - 20), 30, velocity=2))


class Poop(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity):
        super().__init__()
        self.image = poop_img
        self.velocity = velocity
        self.rect = self.image.get_rect()
        self.vel_y = 2
        self.rect.x = x
        self.rect.y = y

    def update(self):
        # Remove the poop if it reaches the bottom of the screen
        if self.rect.y > 300:
            self.kill()
            # Generate new poop outside the screen
            self.rect.y = 0
            self.rect.x = random.randint(20, screen_width - 20)

        # Move the poop down
        self.rect.y += self.vel_y

        # Generate poop
        if len(poop_group) < max_amount:
            # Add a new poop instance to the poop_group
            poop_group.add(Poop(random.randint(20, screen_width - 20), 30, velocity=2))


# Position the player
ester = Player(screen_width // 2, screen_height // 2 + 110)
poop = Poop(random.randint(20, screen_width - 20), 30, velocity = 2)
fig = Figs(random.randint(20, screen_width - 20), 30, velocity = 2)

# Game loop
run = True
while run:
    clock.tick(FPS)

    # Process events if the game is not defined as over
    if game_over == False:
        # Draw background
        draw_bg()

        # Check if it's time to spawn a new fig
        current_time = pygame.time.get_ticks()
        if current_time - fig_spawn_time > fig_spawn_interval and len(fig_group) < max_amount:
            fig = Figs(random.randint(20, screen_width - 20), 30, velocity=2)
            fig_group.add(fig)
            fig_spawn_time = current_time
            # Reset interval for the next fig
            fig_spawn_interval = random.randint(3000, 4500)

        elif current_time - poop_spawn_time > poop_spawn_interval and len(poop_group) < max_amount:
            poop = Poop(random.randint(20, screen_width - 20), 30, velocity=2)
            poop_group.add(poop)
            poop_spawn_time = current_time
            # Reset interval for the next poop
            poop_spawn_interval = random.randint(3000, 4500)

        # Update and draw the figs
        fig_group.update()
        poop_group.update()
        fig_group.draw(screen)
        poop_group.draw(screen)

        ester.move()
        ester.draw()
        # Display the score and update the screen
        draw_panel()
        pygame.display.update()

    else:
        # Draw game over screen
        if fade_counter < screen_width:
            fade_counter += 5
            for y in range(0, 4, 2):
                pygame.draw.rect(screen, black, (0, y * 100, fade_counter, 100))
                pygame.draw.rect(screen, black, (screen_width - fade_counter, (y + 1) * 100, screen_width, 100))
        else:
            draw_text("GAME OVER!", font_big, white, 220, 100)
            draw_text("SCORE: " + str(score), font_big, white, 240, 150)
            draw_text("PRESS SPACE TO PLAY AGAIN", font_big, white, 100, 250)

            # Update high score/create score file
            if score > high_score:
                high_score = score
                with open("score.txt", "w") as file:
                    file.write(str(high_score))

            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:

                # Reset variables
                game_over = False
                score = 0
                fade_counter = 0
                # Reposition ester
                ester.rect.center = (screen_width // 2, screen_height // 2 + 110)
                # Reset objects
                fig_group.empty()
                poop_group.empty()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.quit()