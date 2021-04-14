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


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        self.width = SIZE
        self.height = SIZE
        self.cell = (0, 0)
