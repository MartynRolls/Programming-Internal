import pygame
from random import randint

pygame.init()


class Player:
    def __init__(self):
        self.sword = Sword()
        self.collision_box = pygame.Rect(0, 0, 30, 45)
        self.level_map = []
        self.enemy_list = []
        self.switch_on = False
        self.airborne = False
        self.airtime = 0
        self.alive = True
        self.death_details = [randint(-5, 5), randint(-16, -8)]

        self.x, self.y = 0, 0
        self.dx, self.dy = 0, 0

        self.facing_left = False
        self.step = 0

        self.sprites = []
        sheet = pygame.image.load('Sprites/Player.png')
        self.sprites = load_sheet(sheet, 10, 15, 3)

        self.jump_effect = pygame.mixer.Sound("Sound Effects/Jump.mp3")
        self.death_effect = pygame.mixer.Sound("Sound Effects/Player Death.mp3")
        self.hit_effect = pygame.mixer.Sound("Sound Effects/Thud.mp3")

    def move(self):
        if self.alive:
            # X movement
            self.x += self.dx
            while self.collision(0, 0):  # If there is a collision, shift the player over
                self.x += 1 if self.dx < 0 else -1

            # Y movement
            if self.airborne:  # If the player is falling, fall
                self.fall()
            elif not self.collision(0, 1):  # If the player should be falling, fall
                self.airborne = True

        else:  # If dead
            self.death_details[1] += 0.5  # Gravity
            self.x += self.death_details[0]
            self.y += self.death_details[1]

        # Handling the swords movement
        if self.sword.equipped:  # Place the sword on the player if it's meant to be there
            self.sword.x = self.x
            self.sword.y = self.y
        else:  # Otherwise, move the sword accordingly
            self.sword.move()

    def jump(self):
        if ((self.collision(0, 5) and not self.airborne) or  # Jump if not airborne, and touching the ground
                (self.airtime < 3 and self.dy > 0) or  # Or jump if player hasn't been falling for very long
                (self.airtime < 8)):  # Or reset velocity if player hasn't been airborne very long

            self.dy = -9  # Giving the player velocity

            if not self.airborne:
                self.airborne = True
                self.switch_on = not self.switch_on  # Switching switch blocks
                self.sword.switch_on = self.switch_on

            if self.collision(0, 0):  # Making sure player shouldn't die from the switch blocks
                self.alive = False
            elif self.airtime == 0:  # Otherwise, play the jump effect
                pygame.mixer.Sound.play(self.jump_effect)

    def fall(self):
        self.airtime += 1
        if self.collision(0, self.dy):  # If there is a collision, try to stop it
            pygame.mixer.Sound.play(self.hit_effect)
            while self.collision(0, self.dy):  # While colliding, back up
                self.y += 1 if self.dy < 0 else -1

            if self.dy >= 0:  # If the players landed on the floor, they're not falling anymore
                self.airborne = False
                self.airtime = 0

            self.y += self.dy
            self.dy = 0
        else:  # If there's no collision, fall
            self.y += self.dy
            self.dy += 1

    def collision(self, dx, dy):
        self.collision_box.topleft = self.x + dx, self.y + dy
        for y in range(int(self.y / 30 - 1), int(self.y / 30 + 4)):
            for x in range(int(self.x / 30), int(self.x / 30 + 2)):
                if self.collision_box.colliderect(pygame.Rect(x * 30, y * 30, 30, 30)):  # If collision
                    if (self.level_map[y][x] == 1 or  # Colliding with Block
                       (self.level_map[y][x] == 2 and self.y - dy + 45 < y*30) or  # Or Falling through Platform
                       (self.level_map[y][x] == 5 and self.switch_on) or  # Or Colliding with an
                       (self.level_map[y][x] == 6 and not self.switch_on)):  # Activated Switch Blcok
                        return True

                    # Checking for death
                    collide = self.collision_box.colliderect(pygame.Rect(x * 30 + 12, y * 30 + 3, 24, 18))
                    if self.level_map[y][x] == 3 and collide:  # Colliding with Spikes
                        self.alive = False
                        pygame.mixer.Sound.play(self.death_effect)

        collide = self.collision_box.colliderect(self.sword.collision_box)  # Checking collision with sword
        if collide and self.y - dy + 45 < self.sword.y:
            return True

        # Checking for death
        for enemy in self.enemy_list:
            if self.collision_box.colliderect(enemy):  # Checking collision with enemy
                self.alive = False
                pygame.mixer.Sound.play(self.death_effect)

        return False

    def draw_player(self):
        surface = pygame.Surface((300, 200), pygame.SRCALPHA)

        if self.dx < 0:  # Make the player face the correct way
            self.facing_left = True
        elif self.dx > 0:
            self.facing_left = False

        if self.sword.equipped:  # Make the sword face the right way (if applicable)
            self.sword.facing_left = self.facing_left

        if self.dx != 0 and self.dy == 0:  # Move to the next part of the players animation
            self.step += 1 if self.step < 14 else -14

            # Fetch the correct sprite for the player
            if self.step > 7:
                sprite = self.sprites[1]
            else:
                sprite = self.sprites[2]
        else:
            sprite = self.sprites[0]

        if self.facing_left:  # Flip the player sprite if required
            sprite = pygame.transform.flip(sprite, True, False)

        x, y = int(self.x / 3), int(self.y / 3)
        surface.blit(sprite, (x, y))

        return surface


class Sword:
    def __init__(self):
        self.equipped = True
        self.airborne = False
        self.dy = 0
        self.level_map = []
        self.sprite = [pygame.image.load('Sprites/Sword.png'), pygame.image.load('Sprites/FlyingSword.png')]
        self.throw_effect = pygame.mixer.Sound("Sound Effects/Throw.mp3")
        self.hit_effect = pygame.mixer.Sound("Sound Effects/Thud.mp3")
        self.collision_box = pygame.Rect(0, 0, 45, 9)
        self.x = 0
        self.y = 0
        self.facing_left = False
        self.switch_on = False

    def throw(self):
        if self.equipped:  # If the sword is equipped, throw it.
            self.equipped = False
            self.airborne = True
            self.y += 15
            pygame.mixer.Sound.play(self.throw_effect)

    def move(self):
        if self.airborne:  # If the sword has been thrown
            self.x -= 9 if self.facing_left else -9
            if self.collision():
                pygame.mixer.Sound.play(self.hit_effect)
            for _ in range(24):  # Try to get the sword out of the wall
                if self.collision():
                    self.airborne = False
                    self.x += 1 if self.facing_left else -1
                    
        elif self.dy:  # If the sword should be falling
            self.y += self.dy
            self.dy += 1
            self.collision_box.topleft = self.x, self.y
            
        else:  # If the sword is embedded in the wall
            self.x -= 1 if self.facing_left else -1
            if not self.collision():  # Making sure the sword is still in a wall
                self.dy += 1
            self.x += 1 if self.facing_left else -1
            if self.collision():  # Making sure the sword isn't inside an active switch block
                self.dy += 1

    def collision(self):
        self.collision_box.topleft = self.x, self.y
        y = int(self.y / 30)
        for x in range(int(self.x / 30), int(self.x / 30 + 3)):
            if (self.level_map[y][x] == 1 or  # Colliding with Wall
               (self.level_map[y][x] == 5 and self.switch_on) or  # Or colliding with an active
               (self.level_map[y][x] == 6 and not self.switch_on)):  # switch block
                if self.collision_box.colliderect(pygame.Rect(x * 30, y * 30, 30, 30)):
                    return True

            elif self.level_map[y][x] == 2:  # If colliding (and alligned) with a platform
                if self.collision_box.colliderect(pygame.Rect(x * 30, y * 30, 30, 9)):
                    return True

        return False

    def draw_sword(self):
        surface = pygame.Surface((300, 200), pygame.SRCALPHA)
        sprite = self.sprite[0 if self.equipped else 1]  # Find correct sprite

        if self.facing_left:  # Flip sprite if facing left
            sprite = pygame.transform.flip(sprite, True, False)

        x, y = int(self.x / 3), int(self.y / 3)

        if self.equipped or self.facing_left:  # Adjust swords position correctly
            x -= 3
        if not self.equipped:
            y -= 2

        surface.blit(sprite, (x, y))

        return surface


class Goal:
    def __init__(self, x, y):
        self.collision_box = pygame.Rect(x, y, 30, 30)
        self.x, self.y = x, y
        self.player_location = None
        self.enemy_list = []
        self.got = False

        sheet = pygame.image.load('Sprites/Goal.png')
        self.sprites1 = load_sheet(sheet, 10, 10, 20)

        sheet = pygame.image.load('Sprites/GoalGot.png')
        self.sprites2 = load_sheet(sheet, 16, 30, 18)

        self.frame = 0
        self.step1 = 0
        self.step2 = 0

    def next_step(self):
        self.frame += 1

        if self.frame == 10:  # Every ten frames:
            self.frame = 0
            self.step1 += 1 if self.step1 != 19 else -19  # Move to next sprite
            if self.got and self.step2 != 17:  # If captured
                self.step2 += 1  # Change cover sprite aswell

        if self.collision_box.colliderect(self.player_location):  # If touching the player, has been caught
            self.got = True

        for enemy in self.enemy_list:  # If touching an enemy, has been caught
            if self.collision_box.colliderect(enemy):
                self.got = True

    def draw_goal(self):
        surface = pygame.Surface((300, 200), pygame.SRCALPHA)

        x, y = int(self.x / 3), int(self.y / 3)
        if not self.got or self.step2 < 5:  # Draw first sprite
            sprite = self.sprites1[self.step1]
            surface.blit(sprite, (x, y))

        if self.got:  # Draw second sprite
            sprite = self.sprites2[self.step2]
            surface.blit(sprite, (x - 3, y - 17))

        return surface


class Enemy:
    def __init__(self, x, y, level):
        self.collision_box = pygame.Rect(x * 30, y * 30, 30, 30)
        self.x = x * 30
        self.y = y * 30
        self.dy = 0
        self.facing_left = True
        self.step = 0
        self.level_map = level
        self.switch_on = False
        self.sword_location = None
        self.alive = True
        self.death_details = [0, randint(-5, 5), randint(-16, -8)]

        self.animation_step = 0
        sheet = pygame.image.load('Sprites/Enemy.png')
        self.sprites = load_sheet(sheet, 10, 10, 3)

        self.death_effect = pygame.mixer.Sound("Sound Effects/Enemy Death.mp3")

    def move(self, sword_killing):
        if self.alive:
            collide = self.collision_box.colliderect(self.sword_location)
            if (collide and sword_killing) or (self.collision() and not self.dy):   # Make sure the enemy shouldn't be dead
                self.alive = False
                self.collision_box.topleft = 0, 0
                pygame.mixer.Sound.play(self.death_effect)

            self.fall()

            self.step += 1
            if self.step == 5:  # Every five frames:
                self.step = 0

                self.x += -3 if self.facing_left else 3  # Move forward
                if self.collision():  # Turn around if colliding
                    self.facing_left = not self.facing_left
                    self.x += -6 if self.facing_left else 6

                self.animation_step += 1  # Move onto next animation step
                if self.animation_step == 3:
                    self.animation_step = 0

            if self.alive:  # If the enemy hasn't died
                self.collision_box.topleft = self.x, self.y  # Move collision box

        else:  # If dead
            self.death_details[2] += 0.5  # Gravity
            self.x += self.death_details[1]  # Move
            self.y += self.death_details[2]

    def fall(self):
        self.dy += 1
        self.y += self.dy + 28

        for _ in range(self.dy):
            y = int(self.y / 30)
            for x in range(int(self.x / 30), int(self.x / 30 + 2)):
                if (0 < self.level_map[y][x] < 3
                   or (self.level_map[y][x] == 5 and self.switch_on)
                   or (self.level_map[y][x] == 6 and not self.switch_on)):
                    self.y -= 1
                    self.dy = 0

        self.y -= 28

    def collision(self):
        y = int(self.y / 30)
        for x in range(int(self.x / 30), int(self.x / 30 + 2)):
            if (4 > self.level_map[y][x] > 0 or  # Colliding with walls, platforms, or spikes
               self.level_map[y + 1][x] == 0 or  # Or no floor ahead
               self.level_map[y][x] == 5 and self.switch_on or  # Or colliding with an
               self.level_map[y][x] == 6 and not self.switch_on):  # active switch block
                return True
        return False

    def draw_enemy(self):
        surface = pygame.Surface((300, 200), pygame.SRCALPHA)

        sprite = self.sprites[self.animation_step]  # Fetch sprite

        if self.facing_left:  # Flip sprite if facing left
            sprite = pygame.transform.flip(sprite, True, False)

        x, y = int(self.x / 3), int(self.y / 3)
        surface.blit(sprite, (x, y))

        return surface


class Level:
    def __init__(self, level):
        self.level_map = []
        self.level = level
        self.set_level(self.level)
        self.step = 0
        self.clear = True

        self.enemies = []
        self.goals = []

        self.wall_tiles = []
        self.platform_tiles = []
        self.spike_tile = None
        self.switch_clear_tiles = []
        self.image = pygame.Surface((300, 200), pygame.SRCALPHA)
        self.load_tiles()

    def set_level(self, level):
        directory = 'Levels/Level' + str(level) + '.txt'
        file = open(directory, "r")  # Open text file
        lines = file.readlines()  # Read it
        self.level_map = [[int(char) for char in line.strip()] for line in lines]  # Convert it into a list

    def load_tiles(self):
        # Load all tile sheets
        sheet = pygame.image.load('Sprites/Walls.png')
        self.wall_tiles = load_sheet(sheet, 10, 10, 9)

        sheet = pygame.image.load('Sprites/Platforms.png')
        self.platform_tiles = load_sheet(sheet, 10, 10, 3)

        image = pygame.image.load('Sprites/Spikes.png').convert_alpha()
        self.spike_tile = image

        sheet = pygame.image.load('Sprites/SwitchClear.png')
        sheet = load_sheet(sheet, 90, 10, 4)
        self.switch_clear_tiles = [load_sheet(sheet[i], 10, 10, 9) for i in range(4)]

    def draw_enemies(self):
        surface = pygame.Surface((300, 200), pygame.SRCALPHA)
        for enemy in self.enemies:  # Draw all enemies
            surface.blit(enemy.draw_enemy(), (0, 0))

        return surface

    def draw_goals(self):
        surface = pygame.Surface((300, 200), pygame.SRCALPHA)
        for goal in self.goals:  # Draw all goals
            surface.blit(goal.draw_goal(), (0, 0))

        return surface

    def draw_switch(self):
        self.step += 1 if self.step != 39 else -39
        surface = pygame.Surface((300, 200), pygame.SRCALPHA)

        for y, line in enumerate(self.level_map):
            for x, tile in enumerate(line):
                for i in range(5, 7):
                    if tile == i:
                        tile_number = self.find_tile(x, y)  # Fetch tile number

                        if (i == 5 and self.clear) or (i == 6 and not self.clear):  # If using clear tiles
                            image = self.switch_clear_tiles[int(self.step / 10)][tile_number]
                        else:  # Else if using normal tiles
                            image = self.wall_tiles[tile_number]

                        surface.blit(image, (x * 10, y * 10))
        return surface

    '''
    0 = Empty Space
    1 = Wall
    2 = Platform
    3 = Spikes
    4 = Enemies
    5 = Switch Tiles (off)
    6 = Switch Tiles (on)
    8 = Goals
    9 = Player Starting Pos
    '''
    def draw_level(self):
        cords = (0, 0)  # Players starting position
        for y, line in enumerate(self.level_map):
            for x, tile in enumerate(line):
                if tile == 9:  # Players starting position
                    cords = (x * 30, y * 30 - 15)
                elif tile == 8:  # Goals
                    self.goals.append(Goal(x * 30, y * 30 - 15))
                elif tile == 4:  # Enemies
                    self.enemies.append(Enemy(x, y, self.level_map))
                elif 5 > tile > 0:  # Draw normal tiles to level image
                    image = self.find_tile(x, y)
                    self.image.blit(image, (x*10, y*10))
        return cords

    def find_tile(self, x, y):
        tile = self.level_map[y][x]
        if tile == 1 or tile == 5 or tile == 6:  # If Wall Tile or Switch Tile
            tile_number = 4  # Starting Position
            if y > 0 and self.level_map[y - 1][x] != tile:  # Move position up if above tile's empty
                tile_number -= 3
            if y < 19 and self.level_map[y + 1][x] != tile:  # Move down if below tile's empty
                tile_number += 3
            if x > 0 and self.level_map[y][x - 1] != tile:  # Move left if empty
                tile_number -= 1
            if x < 29 and self.level_map[y][x + 1] != tile:  # Move right if empty
                tile_number += 1

            # Return wall tile image if wall tile, else tile number for switch tiles
            return self.wall_tiles[tile_number] if tile == 1 else tile_number

        if tile == 2:  # If Platform Tile
            tile_number = 1
            if x > 0 and self.level_map[y][x - 1] < 1:  # Move left if empty
                tile_number -= 1
            if x < 29 and self.level_map[y][x + 1] < 1:  # Move right if empty
                tile_number += 1

            return self.platform_tiles[tile_number]

        if tile == 3:  # Spike Tile
            return self.spike_tile


def load_sheet(sheet, x, y, z):
    return_list = []
    for i in range(z):  # For every image in sprite sheet
        image = pygame.Surface((x, y), pygame.SRCALPHA)  # Create a new surface
        image.blit(sheet, (0, 0), (i * x, 0, (i + 1) * x, y))  # Paste next section of image onto it
        return_list.append(image)  # Add it to the list
    return return_list  # Return unpacked sprite sheet


def start_game(level):
    level = Level(level)
    cords = level.draw_level()

    player = Player()
    player.x, player.y = cords
    player.level_map = level.level_map
    player.sword.level_map = level.level_map

    return level, player
