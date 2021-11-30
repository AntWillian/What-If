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
            #missao ativa, iniciada , finalizada, quest Secundaria
            "fase1": [True, False, False, False],
            "fase2":  [False, False, False, False],
            "fase3": [False, False, False, False],
            "fase4": [False, False, False, False],
            "fase5":  [False, False, False, False],
            "fase6":  [False, False, False, False],
            "fase7": [False, False, False, False, False], #end Game
        }

        self.fase1 = 0
        self.fase2 = 0
        self.fase3 = 0
        self.fase4 = 0
        self.fase5 = 0
        self.fase6 = 0
        self.fase7 = 0

        #passar para ultima cena do jogo
        self.passarCena = False


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
        self.fazendeiro1 = Spritesheet("assets/personagens/fazendeiro_1.png")
        self.fazendeiro2 = Spritesheet("assets/personagens/fazendeiro_2.png")
        self.fazendeiro3 = Spritesheet("assets/personagens/fazendeiro_3.png")
        self.prefeito = Spritesheet("assets/personagens/Prefeito.png")
        self.indio = Spritesheet("assets/personagens/Indio.png")
        self.img_quest = Spritesheet("assets/quest.png")
        self.img_questSecundaria = Spritesheet("assets/questSecundaria.png")


        self.terrain_spritesheet = Spritesheet("assets/terrain.png")
        self.terrain_spritesheet_farm = Spritesheet("assets/Farm.png")

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.cracks = pygame.sprite.LayeredUpdates()

        self.fenda1 = pygame.sprite.LayeredUpdates()
        self.fenda2 = pygame.sprite.LayeredUpdates()
        self.fenda2Secunario = pygame.sprite.LayeredUpdates()
        self.fenda3 = pygame.sprite.LayeredUpdates()
        self.fenda3Secundario = pygame.sprite.LayeredUpdates()
        self.fenda4 = pygame.sprite.LayeredUpdates()
        self.fenda5 = pygame.sprite.LayeredUpdates()
        self.fenda6 = pygame.sprite.LayeredUpdates()
        self.fenda7 = pygame.sprite.LayeredUpdates()

        #personagem final
        self.personagenFinal = pygame.sprite.LayeredUpdates()
        self.questFinal = False

        #variavel que verifica se mudou de tela
        self.change_scene = False


        self.fases =[True, False, False, False, False, False, False, False, False]


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


                if column == "1":
                    personagen_padre(self, j, i)
                if column == "2":
                    personagen_hernandez(self, j, i)
                if column == "@":
                    personagen_neto_hernandez(self, j, i)
                if column == "3":
                    personagen_miguel(self, j, i)
                if column == "$":
                    personagen_netaMiguel(self, j, i)
                if column == "4":
                    personagen_professora(self, j, i)
                if column == "5":
                    personagen_coveiro(self, j, i)
                if column == "6":
                    personagen_padre2(self, j, i)
                if column == "7":
                    personagen_prefeito(self, j, i)


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


