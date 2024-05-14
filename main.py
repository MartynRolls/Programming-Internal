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

go_right = True

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
        player.dx -= 8
        go_right = False
    if keys[pygame.K_d]:
        player.dx += 8
        go_right = True

    player.move()

    screen.blit(level_image, (0, 0))

    player_sprite = pygame.transform.scale_by(player.sprites[0], (size, size))

    if not go_right:
        image = pygame.transform.flip(player_sprite, True, False)
    else:
        image = player_sprite

    screen.blit(image, (player.x, player.y))

    pygame.display.flip()
    clock.tick(60)
    # print(clock.get_fps())
