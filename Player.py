from utils import reach_wall
import pygame

# Constants
SCREEN_HEIGHT = 380
SCREEN_WIDTH = 400
SIZE = 5
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
T = 3

RIGHT = 1
LEFT = 2
UP = 3
DOWN = 4


class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.width = SIZE
        self.height = SIZE
        self.pos = (SCREEN_WIDTH - SIZE, SCREEN_HEIGHT - SIZE)
        self.cell = self.get_cell()
        self.touch_wall = 0
        self.cells = [self.cell]

    def get_cell(self):
        return (self.pos[0] // SIZE, self.pos[1] // SIZE)

    def calc_pos(self, cell):
        return (cell[0] * SIZE, cell[1] * SIZE)

    def move(self, dir, grid):
        x, y = self.cell
        if dir == "UP":
            x -= 1
        elif dir == "DOWN":
            x += 1
        elif dir == "LEFT":
            y -= 1
        else:
            y += 1
        x = self.clamp(x, 0, 79)
        y = self.clamp(y, 0, 75)
        if grid[x][y] == 1 or reach_wall((x, y)):
            self.touch_wall += 1
        self.cell = (x, y)
        self.cells.append(self.cell)

    def clamp(self, value, min_val, max_val):
        if value <= min_val:
            return min_val
        elif value >= max_val:
            return max_val
        else:
            return value

    def should_invoke_fill(self, conquered_set):
        if self.touch_wall >= 2:
            self.touch_wall = 1
            return True
        return False

    def calc_best_point(self, grid):
        lp = self.cells[-1]
        abv = (lp[0] - 1, lp[1] - 1)
        bel = (lp[0] + 1, lp[1] + 1)
        l = (lp[0] + 1, lp[1] - 1)
        r = (lp[0] - 1, lp[1] + 1)
        try:
            abv_val = grid[abv[0]][abv[1]]
        except IndexError:
            abv_val = -1
        try:
            bel_val = grid[bel[0]][bel[1]]
        except IndexError:
            bel_val = -1
        try:
            l_val = grid[l[0]][l[1]]
        except IndexError:
            l_val = -1
        try:
            r_val = grid[r[0]][r[1]]
        except IndexError:
            r_val = -1
        res = []
        if abv_val == 0:
            res.append(abv)
        if bel_val == 0:
            res.append(bel)
        if l_val == 0:
            res.append(l)
        if r_val == 0:
            res.append(r)
        return res
