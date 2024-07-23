import pygame
import game

# Initialising game
pygame.init()

# Defining Variables
size = 5
width, height = size * 300, size * 200
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption('Moon kNight')

sheet = pygame.image.load('Sprites/Transition.png')
transition_tiles = game.load_sheet(sheet, 10, 10, 32)
transition = 0
wait = 0

info = []
sheet = pygame.image.load('Sprites/Info/Info1.png')
info.append(pygame.transform.scale_by(sheet, (2, 2)))
sheet = pygame.image.load('Sprites/Info/Info2.png')
info.append(game.load_sheet(sheet, 110, 20, 10))
sheet = pygame.image.load('Sprites/Info/Info3.png')
info.append(game.load_sheet(sheet, 65, 14, 6))
step = 0

pygame.mixer.music.load('Sound Effects/Music.mp3')
pygame.mixer.music.play(-1)
win_effect = pygame.mixer.Sound("Sound Effects/Win.mp3")

# Setting up game
level, player = game.start_game(0)
current = level.level

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
            elif event.key == pygame.K_r:
                transition = 1

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
    level.clear = not player.switch_on

    player.enemy_list = []  # Clear enemy positions
    for enemy in level.enemies:
        enemy.sword_location = player.sword.collision_box  # Telling enemies where the sword is
        enemy.switch_on = not level.clear  # Telling enemies if switch-blocks are on
        enemy.move((player.sword.dy or player.sword.airborne))  # Move all the enemies
        player.enemy_list.append(enemy.collision_box)  # Tell player enemy locations

    for goal in level.goals:
        goal.player_location = player.collision_box  # Tell goals where the player is
        goal.enemy_list = player.enemy_list  # Tell goals where enemies are
        goal.next_step()  # Updating goal sprite

    # Drawing sprites
    surface = pygame.Surface((300, 200), pygame.SRCALPHA)

    if not (player.sword.dy or player.sword.airborne or player.sword.equipped):
        image = player.sword.draw_sword()
        surface.blit(image, (0, 0))

    image = level.image
    surface.blit(image, (0, 0))

    image = level.draw_switch()
    surface.blit(image, (0, 0))

    image = level.draw_goals()
    surface.blit(image, (0, 0))

    image = level.draw_enemies()
    surface.blit(image, (0, 0))

    if player.sword.dy or player.sword.airborne or player.sword.equipped:
        image = player.sword.draw_sword()
        surface.blit(image, (0, 0))

    image = player.draw_player()
    surface.blit(image, (0, 0))

    # Seeing if information should be displayed, and displaying it
    if current == 0:
        image = info[0]
        surface.blit(image, (50, 20))
    elif current == 1:
        step += 1 if step != 199 else -199
        image = info[1][int(step / 20)]
        surface.blit(image, (30, 170))
    elif current == 2:
        step += 1 if step != 119 else -119
        image = info[2][int(step / 20)]
        surface.blit(image, (30, 170))

    # Drawing transition if needed
    if transition:
        if wait:
            wait -= 1
        else:
            transition += 1
            for x in range(30):
                for y in range(20):
                    surface.blit(transition_tiles[int(transition // 5)], (x * 10, y * 10))

            if transition == 159:  # Break at end of animation
                transition = 0
            elif transition == 75:  # Set up game (again)
                level, player = game.start_game(level.level)
                player.move()  # To prevent sword breaking game
                current = max(current, level.level)
                step = 0

    elif all(goal.got for goal in level.goals) and level.goals:
        wait = 90
        transition = 1
        level.level += 1
        pygame.mixer.Sound.play(win_effect)
    elif not player.alive:
        wait = 30
        transition = 1

    # Placing image onto screen
    surface = pygame.transform.scale_by(surface, (size, size))
    screen.blit(surface, (0, 0))

    pygame.display.flip()
    clock.tick(60)
