import pygame


class Player:
    def __init__(self):
        self.level = []
        self.x = 0
        self.y = 0

    def set_level(self, level):
        self.level = level

    def move_x(self, dx):
        pass


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
    def draw_level(self, tile_size):
        image = pygame.Surface((tile_size*30, tile_size*20))
        pygame.draw.rect(image, 'white', (0, 0, 30 * tile_size, 20 * tile_size))
        for y, line in enumerate(self.level_map):
            for x, tile in enumerate(line):
                if tile == 1:
                    pygame.draw.rect(image, 'black', (x*tile_size, y*tile_size, tile_size, tile_size))

        return image
