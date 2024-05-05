import pygame
import game

clock = pygame.time.Clock()
pygame.display.set_caption('Window Title')

level = game.Level()

# Main loopwhile True:
    # Checking events    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill('white')

    # Checking key presses    keys = pygame.key.get_pressed()

    image = level.draw_level(25)
    screen.blit(image, (0, 0))

    pygame.display.flip()
    clock.tick(60)
