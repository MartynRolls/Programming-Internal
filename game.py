import pygame
from random import randint


class Player:
    def __init__(self, position, goal_location):
        self.sword = Sword()
        self.goal = Goal(goal_location)
        self.collision_box = pygame.Rect(0, 0, 30, 45)
        self.level_map = []
        self.enemy_list = []
        self.airborne = False
        self.alive = True
        self.death_details = [0, 0, 0]

        self.x, self.y = position
        self.dx, self.dy = 0, 0

        self.facing_left = False
        self.step = 0

        self.sprites = []
        sheet = pygame.image.load('Sprites/Player.png').convert_alpha()
        for x in range(3):
            image = pygame.Surface((10, 15), pygame.SRCALPHA)
            image.blit(sheet, (0, 0), (x * 10, 0, x * 10 + 10, 15))
            self.sprites.append(image)

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

            if self.death_collision(0, 0):  # Handling a death
                self.alive = False
                self.death_details = [0, randint(-5, 5), randint(-16, -8)]

        else:  # If dead
            self.death_details[0] += 1  # Add one to timer
            self.death_details[2] += 0.5  # Gravity
            self.x += self.death_details[1]
            self.y += self.death_details[2]

        # Handling the swords movement
        if self.sword.airborne:  # Move the sword if it's flying
            self.sword.move()
        elif self.sword.equipped:  # Place the sword on the player if it's meant to be there
            self.sword.x = self.x
            self.sword.y = self.y

        # Updating goal sprite
        self.goal.next_step()

    def jump(self):
        if self.collision(0, 5) and not self.airborne:  # Jump if not airborne, and touching the ground
            self.airborne = True
            self.dy = -14

    def fall(self):
        if self.collision(0, self.dy):  # If there is a collision, try to stop it
            while self.collision(0, self.dy):
                self.y += 1 if self.dy < 0 else -1

            if self.dy >= 0:  # If the players landed on the floor, they're not falling anymore
                self.airborne = False

            self.y += self.dy
            self.dy = 0
        else:
            self.y += self.dy
            self.dy += 1

    def collision(self, dx, dy):
        self.collision_box.topleft = self.x + dx, self.y + dy
        for y in range(int(self.y / 30 - 1), int(self.y / 30 + 4)):
            for x in range(int(self.x / 30), int(self.x / 30 + 2)):
                collide = self.collision_box.colliderect(pygame.Rect(x * 30, y * 30, 30, 30))
                if collide:
                    if self.level_map[y][x] == 1:
                        return True
                    if self.level_map[y][x] == 2 and self.y - dy + 45 < y*30:
                        return True

        collide = self.collision_box.colliderect(self.sword.collision_box)
        if collide and self.y - dy + 45 < self.sword.y:
            return True

        return False

    def death_collision(self, dx, dy):
        self.collision_box.topleft = self.x + dx, self.y + dy
        y = self.y // 30 + 1
        for x in range(int(self.x / 30), int(self.x / 30 + 2)):
            if self.level_map[y][x] == 3:
                collide = self.collision_box.colliderect(pygame.Rect(x * 30 + 12, y * 30 + 3, 24, 18))
                if collide:
                    return True

        for enemy in self.enemy_list:
            collide = self.collision_box.colliderect(enemy)
            if collide:
                return True

        return False

    def draw_player(self):
        surface = pygame.Surface((300, 200), pygame.SRCALPHA)

        if self.sword.equipped:  # Make the sword face the right way
            if self.dx < 0:
                self.sword.facing_left = True
            elif self.dx > 0:
                self.sword.facing_left = False

        if self.dx < 0:  # Make the player face the correct way
            self.facing_left = True
        elif self.dx > 0:
            self.facing_left = False

        if self.dx != 0 and self.dy == 0:  # Move to the next part of the players animation
            self.step += 1
        if self.step > 14:
            self.step = 0

        if self.dx != 0 and self.dy == 0 and self.alive:  # Fetch the correct sprite for the player
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
        self.level_map = []
        self.sprite = [pygame.image.load('Sprites/Sword.png'), pygame.image.load('Sprites/FlyingSword.png')]
        self.collision_box = pygame.Rect(0, 0, 45, 9)
        self.x = 0
        self.y = 0
        self.facing_left = False

    def throw(self):
        if self.equipped:  # If the sword is equipped, throw it.
            self.equipped = False
            self.airborne = True
            self.y += 15

    def move(self):
        self.x -= 9 if self.facing_left else -9
        if self.collision():
            self.airborne = False
            while self.collision():
                self.x += 1 if self.facing_left else -1

    def collision(self):
        self.collision_box.topleft = self.x, self.y
        y = int(self.y / 30)
        for x in range(int(self.x / 30), int(self.x / 30 + 3)):
            if self.level_map[y][x] == 1:
                collide = self.collision_box.colliderect(pygame.Rect(x * 30, y * 30, 30, 30))
                if collide:
                    return True
            elif self.level_map[y][x] == 2:
                collide = self.collision_box.colliderect(pygame.Rect(x * 30, y * 30, 30, 9))
                if collide:
                    return True
        return False

    def draw_sword(self):
        surface = pygame.Surface((300, 200), pygame.SRCALPHA)
        sprite = self.sprite[0 if self.equipped else 1]

        if self.facing_left:
            sprite = pygame.transform.flip(sprite, True, False)

        x, y = int(self.x / 3), int(self.y / 3)

        if self.equipped or self.facing_left:
            x -= 3
        if not self.equipped:
            y -= 2

        surface.blit(sprite, (x, y))

        return surface


class Goal:
    def __init__(self, collision_box):
        self.collision_box = collision_box
        self.x, self.y = collision_box.topleft
        self.sprites = []
        sheet = pygame.image.load('Sprites/Goal.png').convert_alpha()
        for x in range(20):
            image = pygame.Surface((10, 10), pygame.SRCALPHA)
            image.blit(sheet, (0, 0), (x * 10, 0, x * 10 + 10, 10))
            self.sprites.append(image)

        self.frame = 0
        self.step = 0

    def next_step(self):
        self.frame += 1 if self.frame != 199 else -199

        if self.frame % 10 == 0:
            self.step += 1 if self.step != 19 else -19

    def draw_goal(self):
        surface = pygame.Surface((300, 200), pygame.SRCALPHA)

        sprite = self.sprites[self.step]

        x, y = int(self.x / 3), int(self.y / 3)
        surface.blit(sprite, (x, y))

        return surface


class Enemy:
    def __init__(self, x, y, level):
        self.collision_box = pygame.Rect(x * 30, y * 30, 30, 30)
        self.x = x * 30
        self.y = y * 30
        self.facing_left = True
        self.step = 0
        self.level_map = level
        self.sword_location = []
        self.alive = True
        self.death_details = [0, 0]

        self.animation_step = 0
        self.sprites = []
        sheet = pygame.image.load('Sprites/Enemy.png').convert_alpha()
        for x in range(3):
            image = pygame.Surface((10, 10), pygame.SRCALPHA)
            image.blit(sheet, (0, 0), (x * 10, 0, x * 10 + 10, 10))
            self.sprites.append(image)

    def move(self, sword_killing):
        if self.alive:
            self.step += 1
            if self.step == 5:
                self.step = 0

                self.x += -3 if self.facing_left else 3
                if self.collision():
                    self.facing_left = not self.facing_left
                    self.x += -6 if self.facing_left else 6

                self.animation_step += 1
                if self.animation_step == 3:
                    self.animation_step = 0

            collide = self.collision_box.colliderect(self.sword_location)
            if collide and sword_killing:
                self.alive = False
                self.death_details = [0, randint(-5, 5), randint(-16, -8)]

        else:  # If dead
            self.death_details[2] += 0.5  # Gravity
            self.x += self.death_details[1]
            self.y += self.death_details[2]
            self.collision_box.topleft = 0, 0

    def collision(self):
        self.collision_box.topleft = self.x, self.y
        y = int(self.y / 30)
        for x in range(int(self.x / 30), int(self.x / 30 + 2)):
            if 4 > self.level_map[y][x] > 0 or self.level_map[y + 1][x] == 0:
                return True
        return False

    def draw_enemy(self):
        surface = pygame.Surface((300, 200), pygame.SRCALPHA)

        sprite = self.sprites[self.animation_step]

        if self.facing_left:
            sprite = pygame.transform.flip(sprite, True, False)

        x, y = int(self.x / 3), int(self.y / 3)
        surface.blit(sprite, (x, y))

        return surface


class Level:
    def __init__(self, level):
        self.level_map = []
        self.level = level
        self.set_level(self.level)

        self.enemies = []

        self.wall_tiles = []
        self.platform_tiles = []
        self.spike_tile = None
        self.image = None
        self.load_tiles()

    def set_level(self, level):
        directory = 'Levels/Level' + str(level) + '.txt'
        file = open(directory, "r")
        lines = file.readlines()
        self.level_map = [[int(char) for char in line.strip()] for line in lines]

    def load_tiles(self):
        sheet = pygame.image.load('Sprites/Walls.png').convert_alpha()
        for y in range(3):
            for x in range(3):
                image = pygame.Surface((10, 10), pygame.SRCALPHA)
                image.blit(sheet, (0, 0), (x * 10, y * 10, x * 10 + 10, y * 10 + 10))
                self.wall_tiles.append(image)

        sheet = pygame.image.load('Sprites/Platforms.png').convert_alpha()
        for x in range(3):
            image = pygame.Surface((10, 10), pygame.SRCALPHA)
            image.blit(sheet, (0, 0), (x * 10, 0, x * 10 + 10, 10))
            self.platform_tiles.append(image)

        image = pygame.image.load('Sprites/Spikes.png').convert_alpha()
        self.spike_tile = image

    def draw_enemies(self):
        surface = pygame.Surface((300, 200), pygame.SRCALPHA)
        for enemy in self.enemies:
            surface.blit(enemy.draw_enemy(), (0, 0))

        return surface

    '''
    0 = Empty Space
    1 = Wall
    2 = Platform
    3 = Spikes
    4 = Enemies
    
    9 = Player Starting Pos
    '''
    def draw_level(self):
        cords = (0, 0)
        goal = pygame.Rect(0, 0, 30, 30)
        level = pygame.Surface((300, 200), pygame.SRCALPHA)

        for y, line in enumerate(self.level_map):
            for x, tile in enumerate(line):
                if tile == 9:
                    cords = (x * 30, y * 30 - 15)
                elif tile == 8:
                    goal.topleft = x * 30, y * 30 - 15
                elif tile == 4:
                    self.enemies.append(Enemy(x, y, self.level_map))
                elif tile > 0:
                    image = self.find_tile(x, y)
                    level.blit(image, (x*10, y*10))

        self.image = level
        return cords, goal

    def find_tile(self, x, y):
        tile = self.level_map[y][x]
        if tile == 1:
            tile_number = 4  # Starting Position
            if y > 0 and self.level_map[y - 1][x] != 1:  # Move position up if above tile's empty
                tile_number -= 3
            if y < 19 and self.level_map[y + 1][x] != 1:  # Move down if below tile's empty
                tile_number += 3
            if x > 0 and self.level_map[y][x - 1] != 1:  # Move left if empty
                tile_number -= 1
            if x < 29 and self.level_map[y][x + 1] != 1:  # Move right if empty
                tile_number += 1

            image = self.wall_tiles[tile_number]

        elif tile == 2:
            tile_number = 1
            if x > 0 and self.level_map[y][x - 1] < 1:  # Move left if empty
                tile_number -= 1
            if x < 29 and self.level_map[y][x + 1] < 1:  # Move right if empty
                tile_number += 1

            image = self.platform_tiles[tile_number]

        else:  # if tile == 3
            image = self.spike_tile

        return image
