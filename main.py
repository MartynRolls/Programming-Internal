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
player = game.Player()

player.set_level(level.level_map)

# Main loop
while True:
    # Checking events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill('white')

    # Checking key presses
    player.dx = 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.jump()
    if keys[pygame.K_a]:
        player.dx -= 10
    if keys[pygame.K_d]:
        player.dx += 10

    player.move()

    image = level.draw_level()
    screen.blit(image, (0, 0))
    pygame.draw.rect(screen, 'red', player.collision_box)

    pygame.display.flip()
    clock.tick(60)
