import pygame
from obj import *
from config import *
from maps.map1 import *
import sys


class Game:

    def __init__(self):

        #Player characters
        self.player_walk_left = Spritesheet("assets/player/andando_esquerda.png")
        self.player_walk_right = Spritesheet("assets/player/andando_direita.png")
        self.player_walk_back_right = Spritesheet("assets/player/frente_e_costa.png")


        self.terrain_spritesheet = Spritesheet("assets/terrain.png")

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.cracks = pygame.sprite.LayeredUpdates()

        #variavel que verifica se mudou de tela
        self.change_scene = False

        self.createTilemap()

    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "P":
                    Player(self, j, i)
                if column == "C":
                    Crack(self, j, i)


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()

    def draw(self, window):
        self.all_sprites.draw(window)

    def game_over(self):
        pass

    def intro_screen(self):
        pass


