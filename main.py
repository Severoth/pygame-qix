from Qix import Qix
from Spark import Spark
import pygame
from Map import Polygon
from Player import Player
from utils import reach_wall
from copy import deepcopy
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DIRS = ["UP", "DOWN", "LEFT", "RIGHT"]
YELLOW = (255, 255, 0)

# Initialize pygame
pygame.init()

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [380, 400]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("Array Backed Grid")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
p = Polygon()
player = Player()
qix = Qix()
spark = Spark()

# -------- Main Program Loop -----------
while not done:
    qix.move(random.choice(DIRS), p.grid)
    spark.move(random.choice(DIRS), p.grid, player.cell[0], player.cell[1] )
    if qix.cell in player.cells:
        done = True
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move("LEFT", p.grid)
            if event.key == pygame.K_RIGHT:
                player.move("RIGHT", p.grid)
            if event.key == pygame.K_UP:
                player.move("UP", p.grid)
            if event.key == pygame.K_DOWN:
                player.move("DOWN", p.grid)
    for cell in player.cells:
        p.grid[cell[0]][cell[1]] = 1
    p.grid[player.cell[0]][player.cell[1]] = 2
    p.grid[qix.cell[0]][qix.cell[1]] = 3
    p.grid[spark.cell[0]][spark.cell[1]] = 3
    if player.should_invoke_fill(p.conquered_set):
        best_points = player.calc_best_point(p.grid)
        bad_points = []
        for point in best_points:
            grid = deepcopy(p.grid)
            try:
                p.flood_fill(grid, point[0], point[1])
            except RecursionError:
                bad_points.append(point)
        for point in best_points:
            if point not in bad_points:
                p.flood_fill(p.grid, point[0], point[1])
                break

    p.update_mask()
    p.grid[qix.cell[0]][qix.cell[1]] = 0
    p.grid[spark.cell[0]][spark.cell[1]] = 0

    # Set the screen background
    screen.fill(BLACK)
    screen.blit(p.image, p.image.get_rect())

    # Limit to 60 frames per second
    clock.tick(10)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
