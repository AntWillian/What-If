import pygame
import pygame.sprite

from obj import *
from config import *
from maps.map1 import *
import sys


class Cena1:

    def __init__(self):

        # player

        self.all_sprites = pygame.sprite.LayeredUpdates()

        self.cena = primeiraCena(self, -100, 100, "assets/cenas/cena1.jpeg")

        self.passarCena = True


    def events(self, events):
        pass

    def mapa_carregar(self, mapa):
        self.mapa = mapa

    def update(self):
        self.all_sprites.update()

    def draw(self, window):

        self.all_sprites.draw(window)
