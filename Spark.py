import math
SIZE = 5
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)


class Spark:
    def __init__(self):
        super().__init__()
        self.width = SIZE
        self.height = SIZE
        self.cell = (0, 0)

    def move(self, dir, grid, player_x, player_y):
        
        x, y = self.cell
        x_coeff = math.floor(abs(player_x - x)/10)
        y_coeff = math.floor(abs(player_y - y)/10)
        print(x_coeff, "    ", y_coeff)
        move_varx = 2
        mover_vary = 2
        if dir == "UP":
            if y == 0 or y == 75:
                x -= move_varx*x_coeff+1
        elif dir == "DOWN":
            if y == 0 or y == 75:
                x -= move_varx*x_coeff+1
        elif dir == "LEFT":
            if x == 0 or x == 79:
                y -= mover_vary*y_coeff+1
        elif dir == "RIGHT":
            if x == 0 or x == 79:
                y += mover_vary*y_coeff+1
        x = self.clamp(x, 0, 79)
        y = self.clamp(y, 0, 75)
        if grid[x][y] == 1:
            return
        else:
            self.cell = (x, y)

    def clamp(self, value, min_val, max_val):
        if value <= min_val:
            return min_val
        elif value >= max_val:
            return max_val
        else:
            return value
