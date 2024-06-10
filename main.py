import pygame
import game

# Initialising game
pygame.init()

# Defining Variables
size = 3
width, height = size * 300, size * 200
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption('Cool Game')

level = game.Level()
player = game.Player()

player.level_map = level.level_map
player.sword.level_map = level.level_map

level_image = level.draw_level()

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
    if keys[pygame.K_SPACE]:
        player.sword.throw()
    if keys[pygame.K_w]:
        player.jump()
    if keys[pygame.K_s]:
        player.y += 1
        if player.collision(0, 0):
            player.y -= 1
    if keys[pygame.K_a]:
        player.dx -= 6
    if keys[pygame.K_d]:
        player.dx += 6

    player.move()  # Move the player

    player.enemy_list = []
    for enemy in level.enemies:
        enemy.sword_location = player.sword.collision_box  # Telling enemies where the sword is
        enemy.move(player.sword.airborne)  # Move all the enemies
        player.enemy_list.append(enemy.collision_box)  # Tell player enemy locations

    # Drawing sprites
    surface = pygame.Surface((300, 200), pygame.SRCALPHA)

    image = player.sword.draw_sword()
    surface.blit(image, (0, 0))

    image = level_image
    surface.blit(image, (0, 0))

    image = level.draw_enemies()
    surface.blit(image, (0, 0))

    image = player.draw_player()
    surface.blit(image, (0, 0))

    surface = pygame.transform.scale_by(surface, (size, size))
    screen.blit(surface, (0, 0))

    pygame.display.flip()
    clock.tick(60)
    # print(clock.get_fps())
