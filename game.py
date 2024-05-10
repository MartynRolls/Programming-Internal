import pygame


class Player:
    def __init__(self):
        self.collision_box = pygame.Rect(0, 0, 30, 30)
        self.level_map = []
        self.airborne = False
        self.x = 350
        self.y = 300
        self.dx = 0
        self.dy = 0

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
        for y in range(int(self.y / 30 - 1), int(self.y / 30 + 3)):
            for x in range(int(self.x / 30), int(self.x / 30 + 2)):
                collide = self.collision_box.colliderect(pygame.Rect(x * 30, y * 30, 30, 30))
                if collide:
                    if self.level_map[y][x] == 1:
                        return True
                    if self.level_map[y][x] == 2 and self.y - dy + 30 < y*30:
                        return True
        return False


def prepare_sheet(directory, width, height):
    slices = []
    sheet = pygame.image.load(directory).convert_alpha()
    for i in range(sheet.get_width() // width):
        image = pygame.Surface((width, height + 8), pygame.SRCALPHA)
        image.blit(sheet, (0, 0), (i * width, 0, (i + 1) * width, height))
        slices.append(image)
    return slices

class Level:
    def __init__(self):
        self.level_map = []
        self.level = 1
        self.set_level(self.level)

        self.wall_tiles = []
        self.load_wall_tiles()

    def set_level(self, level):
        directory = 'Levels/Level' + str(level) + '.txt'
        file = open(directory, "r")
        lines = file.readlines()
        self.level_map = [[int(char) for char in line.strip()] for line in lines]

    def load_wall_tiles(self):
        sheet = pygame.image.load('Sprites/Walls.png').convert_alpha()
        for y in range(3):
            for x in range(3):
                image = pygame.Surface((15, 15), pygame.SRCALPHA)
                image.blit(sheet, (0, 0), (x * 15, y * 15, x * 15 + 15, y * 15 + 15))
                image = pygame.transform.scale_by(image, (2, 2))
                self.wall_tiles.append(image)

    '''
    0 = Empty Space
    1 = Wall
    2 = Platform
    '''
    def draw_level(self):
        image = pygame.Surface((900, 600))
        pygame.draw.rect(image, 'white', (0, 0, 900, 600))
        for y, line in enumerate(self.level_map):
            for x, tile in enumerate(line):
                if tile == 1:
                    tile_type = self.find_tile(x, y)
                    image.blit(self.wall_tiles[tile_type], (x * 30, y * 30))
                elif tile == 2:
                    pygame.draw.rect(image, 'blue', (x * 30, y * 30, 30, 30))

        return image

    def find_tile(self, x, y):
        tile_type = 4

        if y > 0 and self.level_map[y - 1][x] != 1:  # Check tile above
            tile_type -= 3
        if y < 19 and self.level_map[y + 1][x] != 1:  # Check tile below
            tile_type += 3
        if x > 0 and self.level_map[y][x - 1] != 1:  # Check tile to the left
            tile_type -= 1
        if x < 29 and self.level_map[y][x + 1] != 1:  # Check tile to the right
            tile_type += 1

        return tile_type
        
