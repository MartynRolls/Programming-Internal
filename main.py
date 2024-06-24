import pygame
import game

# Initialising game
pygame.init()

# Defining Variables
size = 5
width, height = size * 300, size * 200
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption('Cool Game')

sheet = pygame.image.load('Sprites/Transition.png')
transition_tiles = game.load_sheet(sheet, 10, 10, 32)
transition = 0
wait = 0

current = 0
info = []
info.append(None)
sheet = pygame.image.load('Sprites/Info/Info2.png')
info.append(game.load_sheet(sheet, 110, 20, 10))
sheet = pygame.image.load('Sprites/Info/Info3.png')
info.append(game.load_sheet(sheet, 65, 14, 6))
step = 0

# Setting up game
level, player = game.start_game(10)

# Main loop
while True:
    # Checking events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN and not transition:
            if level.level == 0:
                transition = 1
                level.level += 1
            if event.key == pygame.K_r:
                transition = 1
            if event.key == pygame.K_p:
                level.clear = not level.clear

    screen.fill((30, 60, 90))

    # Checking key presses
    player.dx = 0
    keys = pygame.key.get_pressed()
    if player.alive:
        if keys[pygame.K_SPACE]:
            player.sword.throw()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player.jump()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player.dx -= 5
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player.dx += 5
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player.y += 1
            if player.collision(0, 0):
                player.y -= 1

    player.move()  # Move the player
    player.switch_on = not level.clear

    for goal in level.goals:
        goal.player_location = player.collision_box  # Tell goals where the player is
        goal.next_step()  # Updating goal sprite

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

    image = level.draw_switch()
    surface.blit(image, (0, 0))

    image = level.draw_enemies()
    surface.blit(image, (0, 0))

    image = level.draw_goals()
    surface.blit(image, (0, 0))

    image = player.draw_player()
    surface.blit(image, (0, 0))

    # Seeing if information should be displayed, and displaying it
    if current == 1:
        step += 1 if step != 199 else -199
        image = info[1][int(step / 20)]
        surface.blit(image, (30, 170))
    elif current == 2:
        step += 1 if step != 119 else -119
        image = info[2][int(step / 20)]
        surface.blit(image, (30, 170))

    # Drawing transition if needed
    if transition:
        if wait == 0:
            transition += 1
            for x in range(30):
                for y in range(20):
                    surface.blit(transition_tiles[int(transition // 5)], (x * 10, y * 10))

            if transition == 159:  # Break at end of animation
                transition = 0
            elif transition == 75:  # Set up game (again)
                level, player = game.start_game(level.level)
                player.move()  # To prevent sword breaking game
                '''DEVELOPMENT!!!'''
                if 4 > level.level > current:
                    current += 1
                    step = 0

        else:
            wait -= 1

    elif player.won:
        wait = 90
        transition = 1
        level.level += 1
    elif not player.alive:
        wait = 30
        transition = 1

    # Placing image onto screen
    surface = pygame.transform.scale_by(surface, (size, size))
    screen.blit(surface, (0, 0))

    pygame.display.flip()
    clock.tick(60)
