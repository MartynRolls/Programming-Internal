import pygame


class Player:
    def __init__(self):
        self.collision_box = pygame.Rect(0, 0, 25, 25)
        self.level_map = []
        self.x = 350
        self.y = 250
        self.dx = 0
        self.dy = 0
        self.airborne = False

    def set_level(self, level):
        self.level_map = level

    def move(self):
        self.x += self.dx

        '''while self.collision_wall():
            self.x += 1 if self.dx < 0 else -1'''

        if self.airborne:
            self.fall()

        if not self.collision(0, 1):
            self.airborne = True

        self.collision_box.topleft = self.x, self.y

    def jump(self):
        if self.collision(0, 5) and not self.airborne:
            self.airborne = True
            self.dy = -12

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
        for y in range(int(self.y / 25), int(self.y / 25 + 3)):
            for x in range(int(self.x / 25), int(self.x / 25 + 3)):
                collide = self.collision_box.colliderect(pygame.Rect(x * 25, y * 25, 25, 25))
                if collide:
                    if self.level_map[y][x] == 1:
                        return True
                    if self.level_map[y][x] == 2 and self.y - dy + 25 < y*25:
                        return True
        return False

    def collision_wall(self):
        self.collision_box.topleft = self.x, self.y
        for y in range(int(self.y / 25), int(self.y / 25 + 3)):
            for x in range(int(self.x / 25), int(self.x / 25 + 3)):
                collide = self.collision_box.colliderect(pygame.Rect(x * 25, y * 25, 25, 25))
                if collide and self.level_map[y][x] == 1:
                    return True
        return False


class Level:
    def __init__(self):
        self.level_map = []
        self.level = 1
        self.set_level(self.level)

    def set_level(self, level):
        directory = 'Levels/Level' + str(level) + '.txt'
        file = open(directory, "r")
        lines = file.readlines()
        self.level_map = [[int(char) for char in line.strip()] for line in lines]

    '''
    0 = Empty Space
    1 = Wall
    2 = Platform
    '''
    def draw_level(self):
        image = pygame.Surface((750, 500))
        pygame.draw.rect(image, 'white', (0, 0, 750, 500))
        for y, line in enumerate(self.level_map):
            for x, tile in enumerate(line):
                colour = 'white'
                if tile == 1:
                    colour = 'black'
                elif tile == 2:
                    colour = 'blue'
                pygame.draw.rect(image, colour, (x * 25, y * 25, 25, 25))

        return image
