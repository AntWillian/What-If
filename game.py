import pygame
from obj import *
from config import *
from maps.map1 import *
import sys


class Game:

    def __init__(self):
        #carregagando save (por enquando sera um fixo mas aqui ele deve pegar de um txt)
        self.faseIniciar = 'fase1'  # recebe fase1 como padrao sera trocado de acordo com o salvo no arquivo de saves

        self.bkpfases = {
            # iniciada , finalizada
            "fase1": [True, True],
            "fase2": [True, True],
            "fase3": [False, False],
            "fase4": [False, False],
            "fase5": [False, False],
            "fase6": [False, False],
            "fase7": [False, False],
        }

        #Player characters
        self.player_walk_left = Spritesheet("assets/player/andando_esquerda.png")
        self.player_walk_right = Spritesheet("assets/player/andando_direita.png")
        self.player_walk_back_right = Spritesheet("assets/player/frente_e_costa.png")


        #Personagens
        self.padre = Spritesheet("assets/personagens/Padre.png")
        self.coveiro = Spritesheet("assets/personagens/coveiro.png")
        self.aluna = Spritesheet("assets/personagens/aluna.png")
        self.professora = Spritesheet("assets/personagens/professora.png")


        self.terrain_spritesheet = Spritesheet("assets/terrain.png")

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.cracks = pygame.sprite.LayeredUpdates()

        self.fenda1 = pygame.sprite.LayeredUpdates()
        self.fenda2 = pygame.sprite.LayeredUpdates()
        self.fenda3 = pygame.sprite.LayeredUpdates()

        #variavel que verifica se mudou de tela
        self.change_scene = False

        self.fases =[True, False, False, False, False, False, False, False]

        #grava qual mapa da fase sera carregado
        self.fase_iniciar = ""

        self.createTilemap()

    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                if column == ".":
                    Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "P":
                   self.player = Player(self, j, i)
                if column == "C":
                    Crack(self, j, i)
                if column == "1":
                    personagen_padre(self, j, i)
                if column == "2":
                    personagen_coveiro(self, j, i)
                if column == "3":
                    personagen_aluna(self, j, i)
                if column == "4":
                    personagen_professora(self, j, i)


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False


    def eventsDialogo(self, events):
        self.player.events(events)

    def update(self):
        self.all_sprites.update()


    def draw(self, window):
        window.fill((47, 129, 54))
        self.all_sprites.draw(window)


    def game_over(self):
        pass

    def intro_screen(self):
        pass


