SIZE = 5
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)


class Qix:
    def __init__(self):
        super().__init__()
        self.width = SIZE
        self.height = SIZE
        self.cell = (0, 0)

    def move(self, dir, grid):
        x, y = self.cell
        if dir == "UP":
            x -= 2
        elif dir == "DOWN":
            x += 2
        elif dir == "LEFT":
            y -= 2
        else:
            y += 2
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
