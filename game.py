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

        while self.collision():
            self.x += 1 if self.dx < 0 else -1

        if self.airborne:
            self.fall()

        self.y += 1
        if self.collision():
            self.y -= 1
        else:
            self.airborne = True

        self.collision_box.topleft = self.x, self.y

    def jump(self):
        self.y += 5
        if self.collision():
            self.airborne = True
            self.dy = -12
        self.y -= 5

    def fall(self):
        self.y += self.dy
        self.dy += 1
        if self.collision():
            self.y = int(self.y)

            if self.dy < 0:
                while self.collision():
                    self.y += 1
            else:
                while self.collision():
                    self.y -= 1
                self.airborne = False

            self.dy = 0

    def collision(self):
        self.collision_box.topleft = self.x, self.y
        for y in range(int(self.y / 25), int(self.y / 25 + 3)):
            for x in range(int(self.x / 25), int(self.x / 25 + 3)):
                collide = self.collision_box.colliderect(pygame.Rect(x * 25, y * 25, 25, 25))
                if collide:
                    if ((self.level_map[y][x] == 1) or
                            (self.level_map[y][x] == 2 and self.dy >= 0)):

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
