import pygame
import pygame.sprite

from obj import *
from config import *
from maps.map1 import *
import sys


class Cena3:

    def __init__(self):

        # player

        self.all_sprites = pygame.sprite.LayeredUpdates()

        self.cena = terceiraCena(self, 0, 15, "assets/cenas/cena3.jpeg")

        self.passarCena = True

    def update(self):
        self.all_sprites.update()

    def draw(self, window):
        self.all_sprites.draw(window)
