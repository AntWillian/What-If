import pygame
from config import *
import math
import random


class Obj(pygame.sprite.Sprite):
    def __init__(self, x, y, layer, image, cut_x, cut_y, *groups):

        self._layer = layer
        pygame.sprite.Sprite.__init__(self, *groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = "down"
        self.animation_loop = 1

        self.image = image.get_sprite(cut_x, cut_y, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite

class Player(Obj):
    def __init__(self, x, y, layer, image, cut_x, cut_y, *groups):
        super().__init__(x, y, layer, image, cut_x, cut_y, *groups)

        self.right = False
        self.left = False
        self.down = False
        self.up = False

    def events(self, events):
        if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_d:
                self.right = True
            elif events.key == pygame.K_a:
                self.left = True
            elif events.key == pygame.K_w:
                self.up = True
            elif events.key == pygame.K_s:
                self.down = True

        elif events.type == pygame.KEYUP:
            if events.key == pygame.K_d:
                self.right = False
            elif events.key == pygame.K_a:
                self.left = False
            elif events.key == pygame.K_w:
                self.up = False
            elif events.key == pygame.K_s:
                self.down = False

    def moviments(self):
        if self.right:
            self.x_change += PLAYER_SPEED
            self.facing = 'right'

        elif self.left:
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'

        if self.up:
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'

        elif self.down:
            self.y_change += PLAYER_SPEED
            self.facing = 'down'

    def colisions(self, group, kill, name, direction):

        col = pygame.sprite.spritecollide(self, group, kill)

        if col and name == "platform":
            if direction == "x":
                if self.x_change > 0:
                    self.rect.x = col[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = col[0].rect.right

            if direction == "y":
                if self.y_change > 0:
                    self.rect.y = col[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = col[0].rect.bottom



