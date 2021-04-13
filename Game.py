# -*- coding: utf-8 -*-
import pygame
import random
from Polygon import Polygon
from Player import Player

pygame.init()   # initializing pygame
pygame.font.init()
pygame.event.set_blocked([pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.ACTIVEEVENT, pygame.WINDOWENTER, pygame.WINDOWLEAVE])
# Constants
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GOLD = (235, 177, 52)
BLACK = (0,0,0 )

# Loading fonts
BIG_FONT =  pygame.font.SysFont("Arial", 60)
SMALL_FONT = pygame.font.SysFont("Arial", 20)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

ARROW_KEYS = [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN]  # list of keys

class Game:
    def __init__(self):
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.lives = 3


        self.polygon = Polygon()  # Conquered area
        self.bg_color = BLACK
        self.SURFACE = self.polygon.mask.count()  # Number of conquered pixel after initialization
        self.goal = 90  # Goal percentage of the user (in order to complete the level)
        # self.level = 1  # Current level
        self.min_vel = 20  # Minimum velocity
        self.dvel = 2  # Delta of velocity (to create a range of velocities between min and max)
        self.player = Player()


    def percentage(self):  # Calculate percentage of current conquered area
        return (self.polygon.mask.count() - self.SURFACE)/(SCREEN_WIDTH*SCREEN_HEIGHT - self.SURFACE)*100



    def lose(self):  # Reset needed values in order to lose a lide
        self.player = Player()
        self.lives -= 1
        g.player.change_movement(0)
        pygame.time.delay(1000)

    def is_win(self):  # complete a level if the player passed the goal
        return self.percentage() >= self.goal

    def is_over(self):
        return self.lives == 0

    def add_life(self):  # Limit adding lives to 3
        if self.lives <= 2:
            self.lives += 1


    
    def exit(self):
        pygame.quit()

    def reset(self):  # Initializing values
        self.lives = 3
        self.polygon = Polygon()
        self.SURFACE = self.polygon.mask.count()
        self.goal = 60
        self.level = 1
        self.min_vel = 5
        self.dvel = 2
        self.player = Player()



g = Game()
size = (g.width, g.height)
screen = pygame.display.set_mode(size)
g.polygon.update_mask()


# screen.fill(BLACK)

# Allowing the user to close the window...
carryOn = True
clock = pygame.time.Clock()
while carryOn:
    screen.blit(g.polygon.image, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False
        elif event.type == pygame.KEYDOWN:
            if event.key in ARROW_KEYS:
                old_movement = g.player.movement
                new_movement = ARROW_KEYS.index(event.key) + 1  # movement in terms of Player class
                if not g.player.in_conquered:
                    # Player can't go on opposite direction
                    if abs(old_movement - new_movement) == 1 and \
                        (min(old_movement, new_movement) == 1 or min(old_movement, new_movement) == 3):
                        g.lose()
                        break
                    g.player.add_point()  # Add a point to a list of player's trail points
                g.player.change_movement(new_movement)


        # Overlay texts and hearts
        over_text = BIG_FONT.render("GAME OVER", True, (255, 0, 0))

        if g.is_over():  # Game over
            screen.blit(over_text, (SCREEN_WIDTH / 2 - over_text.get_width() / 2,
                                    SCREEN_HEIGHT / 2 - over_text.get_height() / 2))
            pygame.display.flip()
            pygame.time.delay(2100)
            pygame.quit()

        # Updating player and drawing them
        g.player.update(g.polygon)

        # Changing last point to player's position and displaying its trail
        if len(g.player.points) > 1:
            g.player.points[-1] = list(g.player.rect.center)
            for i in range(len(g.player.points) - 1):
                pygame.draw.line(screen, (255, 0, 0), g.player.points[i], g.player.points[i+1], 3)
        screen.blit(g.player.image, g.player.rect)
    pygame.display.flip()
    # if g.is_win():
    #     b = True
    clock.tick(80)
pygame.quit()