import pygame


class Level:
    def __init__(self):
        self.level_map = []
        self.game_objects = {}
        self.level = 1
        self.set_level(self.level)

    def set_level(self, level):
        directory = 'Levels/Level' + str(level) + '.txt'
        file = open(directory, "r")
        self.level_map = file.readlines()
        self.game_objects = {'Walls': []}
        for y, line in enumerate(self.level_map):
            for x in range(30):
                if line[x] == "1":
                    self.game_objects['Walls'].append((x, y))

    '''
    0 = Empty Space
    1 = Wall
    '''
    def draw_level(self, surface):
        for y, line in enumerate(self.level_map):
            for x in range(30):
                if line[x] == "1":
                    pygame.draw.rect(surface, 'black', (x*25, y*25, 25, 25))
