import pygame
import game

# Initialising game
pygame.init()

# Defining Variables
width, height = 750, 500
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption('Window Title')

level = game.Level()

# Main loop
while True:
    # Checking events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill('white')

    # Checking key presses
    keys = pygame.key.get_pressed()

    level.draw_level(screen)

    pygame.display.flip()
    clock.tick(60)
