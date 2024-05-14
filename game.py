import pygame


class Player:
    def __init__(self):
        self.sword = Sword()
        self.collision_box = pygame.Rect(0, 0, 30, 45)
        self.level_map = []
        self.airborne = False
        self.x = 350
        self.y = 300
        self.dx = 0
        self.dy = 0
        self.sprites = []
        sheet = pygame.image.load('Sprites/Player.png').convert_alpha()
        for x in range(3):
            image = pygame.Surface((10, 15), pygame.SRCALPHA)
            image.blit(sheet, (0, 0), (x * 10, 0, x * 10 + 10, 15))
            self.sprites.append(image)

    def set_level(self, level):
        self.level_map = level

    def move(self):
        self.x += self.dx

        while self.collision(0, 0):
            self.x += 1 if self.dx < 0 else -1

        if self.airborne:
            self.fall()
        elif not self.collision(0, 1):
            self.airborne = True

        self.collision_box.topleft = self.x, self.y

    def jump(self):
        if self.collision(0, 5) and not self.airborne:
            self.airborne = True
            self.dy = -14

    def fall(self):
        if self.collision(0, self.dy):
            if self.dy < 0:
                while self.collision(0, self.dy):
                    self.dy += 1
            else:
                while self.collision(0, self.dy):
                    self.dy -= 1
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
        return False

    def death_collision(self, dx, dy):
        self.collision_box.topleft = self.x + dx, self.y + dy
        y = self.y // 30 + 1
        for x in range(int(self.x / 30), int(self.x / 30 + 2)):
            if self.level_map[y][x] == 3:
                collide = self.collision_box.colliderect(pygame.Rect(x * 30 + 12, y * 30 + 3, 24, 18))
                if collide:
                    return True
        return False


class Sword:
    def __init__(self):
        self.equipped = True




class Level:
    def __init__(self):
        self.level_map = []
        self.level = 1
        self.set_level(self.level)

        self.wall_tiles = []
        self.platform_tiles = []
        self.spike_tile = None
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

    '''
    0 = Empty Space
    1 = Wall
    2 = Platform
    3 = Spikes
    '''
    def draw_level(self):
        level = pygame.Surface((300, 200), pygame.SRCALPHA)
        for y, line in enumerate(self.level_map):
            for x, tile in enumerate(line):
                if tile > 0:
                    image = self.find_tile(x, y)
                    level.blit(image, (x*10, y*10))

        return level

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
