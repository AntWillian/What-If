import pygame
from obj import *
from config import *
from maps.map1 import *
import sys


class Game:

    def __init__(self):
        #carregagando save (por enquando sera um fixo mas aqui ele deve pegar de um txt)
        self.faseIniciar = 'fase6'  # recebe fase1 como padrao sera trocado de acordo com o salvo no arquivo de saves

        self.bkpfases = {
            #missao ativa, iniciada , finalizada, cristais a coletar
            "fase1": [True, False, False, 0],
            "fase2": [False, False, False, 0],
            "fase3": [False, False, False, 0],
            "fase4": [False, False, False, 0],
            "fase5": [False, False, False, 0],
            "fase6": [False, False, False, 0],
            "fase7": [False, False, False, 0],
        }


        #Player characters
        self.player_walk_left = Spritesheet("assets/player/andando_esquerda.png")
        self.player_walk_right = Spritesheet("assets/player/andando_direita.png")
        self.player_walk_back_right = Spritesheet("assets/player/frente_e_costa.png")

        self.portal = Spritesheet("assets/portal/Portal_1.png")


        #Personagens
        self.padre = Spritesheet("assets/personagens/Padre.png")
        self.coveiro = Spritesheet("assets/personagens/coveiro.png")
        self.aluna = Spritesheet("assets/personagens/aluna.png")
        self.professora = Spritesheet("assets/personagens/professora.png")
        self.img_quest = Spritesheet("assets/quest.png")


        self.terrain_spritesheet = Spritesheet("assets/terrain.png")
        self.terrain_spritesheet_farm = Spritesheet("assets/Farm.png")

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.cracks = pygame.sprite.LayeredUpdates()

        self.fenda1 = pygame.sprite.LayeredUpdates()
        self.fenda2 = pygame.sprite.LayeredUpdates()
        self.fenda3 = pygame.sprite.LayeredUpdates()
        self.fenda4 = pygame.sprite.LayeredUpdates()

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
                if column == "A":
                    Bloco_rua(self, j, i, "A")
                if column == "K":
                    Bloco_rua(self, j, i, "K")
                if column == "D":
                    Bloco_rua(self, j, i, "D")
                if column == "E":
                    Bloco_rua(self, j, i, "E")
                if column == "F":
                    Bloco_rua(self, j, i, "F")
                if column == "G":
                    Bloco_rua(self, j, i, "G")
                if column == "H":
                    Bloco_rua(self, j, i, "H")
                if column == "I":
                    Bloco_rua(self, j, i, "I")
                if column == "J":
                    Bloco_rua(self, j, i, "J")

                if column == "L":
                    Bloco_rua(self, j, i, "L")
                if column == "M":
                    Bloco_rua(self, j, i, "M")
                if column == "N":
                    Bloco_rua(self, j, i, "N")
                if column == "O":
                    Bloco_rua(self, j, i, "O")


                if column == "#":
                    quest(self, j, i)



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


