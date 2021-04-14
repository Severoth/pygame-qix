import pygame
from collections import deque

# Constants
SIZE = 5
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
QIX_COLOR = (56, 50, 168)
T = 3

RIGHT = 1
LEFT = 2
UP = 3
DOWN = 4


class Polygon(pygame.sprite.Sprite):
    def __init__(self):
        self.width = 380
        self.height = 400
        self.image = pygame.Surface((self.width, self.height))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.grid = [[0 for _ in range(76)] for _ in range(80)]
        self.conquered = self.count(self.grid, 1)
        self.conquered_set = set()
        self.update_mask()

    def update_mask(self):
        for row in range(80):
            for column in range(76):
                if self.grid[row][column] == 0:
                    color = BLACK
                elif self.grid[row][column] == 1:
                    self.conquered_set.add((row, column))
                    color = GREEN
                elif self.grid[row][column] == 2:
                    self.conquered_set.add((row, column))
                    color = RED
                elif self.grid[row][column] == 3:
                    color = QIX_COLOR
                pygame.draw.rect(self.image,
                                 color,
                                 [(SIZE) * column,
                                  (SIZE) * row,
                                     SIZE,
                                     SIZE], 0)
        #pygame.draw.rect(self.image, WHITE, [0, 0, 5, 400])
        #pygame.draw.rect(self.image, WHITE, [0, 0, 380, 5])
        #pygame.draw.rect(self.image, WHITE, [375, 0, 5, 400])
        #pygame.draw.rect(self.image, WHITE, [0, 395, 380, 5])

    def count(self, grid, v):
        c = 0
        for row in range(80):
            for column in range(76):
                if grid[row][column] == v:
                    c += 1
        return c

    def flood_fill(self, grid, x, y):

        if grid[x][y] == 0:
            grid[x][y] = 1
            # recursively invoke flood fill on all surrounding cells:
            if x > 0:
                self.flood_fill(grid, x - 1, y)
            if x < 79:
                self.flood_fill(grid, x + 1, y)
            if y > 0:
                self.flood_fill(grid, x, y - 1)
            if y < 75:
                self.flood_fill(grid, x, y + 1)
