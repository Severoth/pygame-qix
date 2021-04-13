# -*- coding: utf-8 -*-
import pygame
from timeit import default_timer as timer
from collections import deque
from InversePolygon import InversePolygon
import random

# Constants
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WALL_WIDTH = 20
T = 3

RIGHT = 1
LEFT = 2
UP = 3
DOWN = 4


class Polygon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 800
        self.height = 600
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        # Draw initial conquered area
        pygame.draw.rect(self.image, GREEN, (0, 0, self.width, WALL_WIDTH))
        pygame.draw.rect(self.image, GREEN, (0, 0, WALL_WIDTH, self.height))
        pygame.draw.rect(self.image, GREEN, (0, self.height - WALL_WIDTH, self.width, WALL_WIDTH))
        pygame.draw.rect(self.image, GREEN, (self.width - WALL_WIDTH, 0, WALL_WIDTH, self.height))
        # Using an object that is the inverse of the polygon shape for "ghost" balls
        self.polygon_inverse = InversePolygon(self, pygame.mask.from_surface(self.image).invert())
        self.remain_area = self.height * self.width
        self.update_mask()

    def update_mask(self):
        self.mask = pygame.mask.from_surface(self.image)
        mask_inverse = pygame.mask.from_surface(self.image)
        mask_inverse.invert()
        self.polygon_inverse.update_mask(mask_inverse)

    def add(self, points):
        rect = pygame.draw.polygon(self.image, GREEN, points, -1)
        rect_area = rect.height * rect.width
        if rect_area <= self.remain_area / 2:
            pygame.draw.polygon(self.image, GREEN, points)
        else:
            self.image.fill(GREEN)
            pygame.draw.polygon(self.image, BLACK, points)
        self.remain_area -= rect_area
        self.update_mask()

    def contains(self, sprite):  # Completely contain a sprite by determining the polygon's mask in its coordinates
        self.update_mask()
        return self.mask.get_at((sprite.rect.left, sprite.rect.top)) and \
               self.mask.get_at((sprite.rect.right, sprite.rect.top)) and \
               self.mask.get_at((sprite.rect.left, sprite.rect.bottom)) and \
               self.mask.get_at((sprite.rect.right, sprite.rect.bottom))

    def contains_partially(self, sprite):
        self.update_mask()
        return self.mask.get_at((sprite.rect.left, sprite.rect.top)) or \
               self.mask.get_at((sprite.rect.right, sprite.rect.top)) or \
               self.mask.get_at((sprite.rect.left, sprite.rect.bottom)) or \
               self.mask.get_at((sprite.rect.right, sprite.rect.bottom))

    #--------------------------------------
    # Flood fill (the general idea is from Wikipedia)
    # It basically adds points to color to a stack until it reaches a border (and then the stack will get empty)
    def fill_wiki(self, x, y, color):
        self.pixels = pygame.PixelArray(self.image)
        old_color = self.pixels[x, y]

        if old_color == color:
            return  # nothing to do

        stack = [(x, y)]
        w = self.width
        h = self.height

        while stack:
            cur_point = stack.pop()
            x1, y1 = cur_point

            while x1 >= 0 and self.pixels[x1, y1] == old_color:
                x1 -= 1
            x1 += 1

            above = False
            below = False

            while x1 < w and self.pixels[x1, y1] == old_color:
                self.pixels[x1, y1] = color

                if not above and y1 > 0 and self.pixels[x1, y1 - 1] == old_color:
                    stack.append((x1, y1 - 1))
                    above = True
                elif above and y1 < h - 1 and self.pixels[x1, y1 - 1] != old_color:
                    above = False

                if not below and y1 < h - 1 and self.pixels[x1, y1 + 1] == old_color:
                    stack.append((x1, y1 + 1))
                    below = True
                elif below and y1 < h - 1 and self.pixels[x1, y1 + 1] != old_color:
                    below = False

                x1 += 1
        self.pixels = None  # Releasing pixels array
        self.update_mask()

    def check_open_sides(self, points, line_width, vertical):
        # Return most preferred point to start flood-filling from
        try:
            point = self.mid(points[0], points[1])
        except:
            return
        sides = [(line_width, 0), (-line_width, 0), (0, -line_width), (0, line_width)]
        fill_points = [side for side in sides if not self.mask.get_at((int(point[0] + side[0]), int(point[1] + side[1])))]
        fill_points1 = [p for p in fill_points if p[0] > 0 or p[1] > 0]
        # else:
        #     fill_points1 = [p for p in fill_points if p[0] < 0 or p[1] < 0]
        if len(fill_points1) > 0:
            fill_point = fill_points1[0]
        else:
            return self.check_open_sides(points[1: -1], line_width, vertical)
        return point[0] + fill_point[0], point[1] + fill_point[1]


    # find the place where the trail divides up the screen (in different sections)
    def find_line(self, points, point, vertical):
        for i in range(len(points) - 1):
                if vertical:
                    if min(points[i][1], points[i+1][1]) <= point[1] <= max(points[i][1], points[i+1][1]):
                        return points[i][0]
                else:
                    if min(points[i][0], points[i+1][0]) <= point[0] <= max(points[i][0], points[i+1][0]):
                        return points[i][1]
        if vertical:
            return random.choice(points)[0]
        else:
            return random.choice(points)[1]

    def mid(self, p1, p2):
        return (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2