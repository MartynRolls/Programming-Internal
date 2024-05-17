import pygame
import game

# Initialising game
pygame.init()

# Defining Variables
size = 3
width, height = size * 300, size * 200
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption('Window Title')

level = game.Level()
player = game.Player()

player.set_level(level.level_map)
level_image = level.draw_level()
level_image = pygame.transform.scale_by(level_image, (size, size))

# Main loop
while True:
    # Checking events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill((30, 60, 90))

    # Checking key presses
    player.dx = 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.jump()
    if keys[pygame.K_s]:
        player.y += 1
        if player.collision(0, 0):
            player.y -= 1
    if keys[pygame.K_a]:
        player.dx -= 6
        go_right = False
    if keys[pygame.K_d]:
        player.dx += 6

    player.move()

    screen.blit(level_image, (0, 0))

    image = player.draw_player()
    image = pygame.transform.scale_by(image, (size, size))
    screen.blit(image, (0, 0))

    pygame.display.flip()
    clock.tick(60)
    # print(clock.get_fps())
