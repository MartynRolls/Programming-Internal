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

step = 0
transition = 0
transition_tiles = []
sheet = pygame.image.load('Sprites/Transition.png').convert_alpha()
for x in range(32):
    image = pygame.Surface((10, 10), pygame.SRCALPHA)
    image.blit(sheet, (0, 0), (x * 10, 0, x * 10 + 10, 10))
    transition_tiles.append(image)


level = game.Level(1)
cords, goal = level.draw_level()

player = game.Player(cords, goal)
player.level_map = level.level_map
player.sword.level_map = level.level_map

# Main loop
while True:
    # Checking events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and not transition:
                transition = 1

    screen.fill((30, 60, 90))

    # Checking key presses
    player.dx = 0
    keys = pygame.key.get_pressed()
    if player.alive:
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

    collide = player.collision_box.colliderect(player.goal.collision_box)
    if collide and not transition:  # Checking for a win
        transition = 1
        level.level += 1

    player.enemy_list = []
    for enemy in level.enemies:
        enemy.sword_location = player.sword.collision_box  # Telling enemies where the sword is
        enemy.move(player.sword.airborne)  # Move all the enemies
        player.enemy_list.append(enemy.collision_box)  # Tell player enemy locations

    # Drawing sprites
    surface = pygame.Surface((300, 200), pygame.SRCALPHA)

    image = player.sword.draw_sword()
    surface.blit(image, (0, 0))

    image = level.image
    surface.blit(image, (0, 0))

    image = level.draw_enemies()
    surface.blit(image, (0, 0))

    image = player.goal.draw_goal()
    surface.blit(image, (0, 0))

    image = player.draw_player()
    surface.blit(image, (0, 0))

    # Drawing transition if needed
    if transition:
        transition += 1
        if transition % 5 == 0:
            step += 1

        if transition == 75:
            level = game.Level(level.level)
            cords, goal = level.draw_level()

            player = game.Player(cords, goal)
            player.level_map = level.level_map
            player.sword.level_map = level.level_map

        try:
            for x in range(30):
                for y in range(20):
                    surface.blit(transition_tiles[step], (x * 10, y * 10))
        except IndexError:
            transition = 0
            step = 0

    # Placing image onto screen
    surface = pygame.transform.scale_by(surface, (size, size))
    screen.blit(surface, (0, 0))

    pygame.display.flip()
    clock.tick(60)
    # print(clock.get_fps())
