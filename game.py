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
            self.x -= self.dx

        if self.airborne:
            self.fall()

        self.collision_box.bottomleft = self.x, self.y

    def jump(self):
        self.airborne = True
        self.dy = -10

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
        self.collision_box.bottomleft = self.x, self.y
        for y in range(int(self.y / 25 - 1), int(self.y / 25 + 1)):
            for x in range(int(self.x / 25 - 1), int(self.x / 25 + 1)):
                collide = self.collision_box.colliderect((x * 25, y * 25, 25, 25))
                try:
                    if collide and self.level_map[y][x] == 1:
                        return True
                except IndexError:
                    pass
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
    '''
    def draw_level(self):
        image = pygame.Surface((750, 500))
        pygame.draw.rect(image, 'white', (0, 0, 750, 500))
        for y, line in enumerate(self.level_map):
            for x, tile in enumerate(line):
                if tile == 1:
                    pygame.draw.rect(image, 'black', (x*25, y*25, 25, 25))

        return image
