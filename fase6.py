import pygame
import pygame.sprite

from obj import *
from config import *
from maps.map1 import *
import sys


class Fase6:

    def __init__(self):

        # player
        self.player_walk_left = Spritesheet("assets/player/andando_esquerda.png")
        self.player_walk_right = Spritesheet("assets/player/andando_direita.png")
        self.player_walk_back_right = Spritesheet("assets/player/frente_e_costa.png")
        self.inimigo_esquilo = Spritesheet("assets/inimigos/Esquilo_fofinho.png")
        self.inimigo_urso = Spritesheet("assets/inimigos/Ursinho_fofinho.png")
        self.inimigo_coelho = Spritesheet("assets/inimigos/coelho_fofinho.png")
        self.cristal = Spritesheet("assets/crystal.png")

        self.terrain_spritesheet = Spritesheet("assets/tilemapsMario.png")

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.troncos = pygame.sprite.LayeredUpdates()
        self.plataforma = pygame.sprite.LayeredUpdates()
        self.bloco_solido_moeda = pygame.sprite.LayeredUpdates()
        self.coletar_moeda = pygame.sprite.LayeredUpdates()
        self.coletar_cristal = pygame.sprite.LayeredUpdates()
        self.poder_coletavel = pygame.sprite.LayeredUpdates()
        self.bloco_dePoder_acao = pygame.sprite.LayeredUpdates()
        self.BlocosGerais = pygame.sprite.LayeredUpdates()

        #inimigo
        self.inimigo = pygame.sprite.LayeredUpdates()
        self.inimigo_pulo = pygame.sprite.LayeredUpdates()

        self.blocoQuebraveis = pygame.sprite.LayeredUpdates()
        self.blocoEspeciaisMoedas = pygame.sprite.LayeredUpdates()

        # variavel que verifica se mudou de tela
        self.change_scene = False

        #pontos
        self.scoreCristais = Text(25, "0", "assets/cristalScore.png")
        self.scoreMoedas = Text(25, "0", "assets/moedaScore.png")
        self.scoreVidas = Text(25, "0", "assets/vidaScore.png")

        self.createTilemap()


        self.tirosCriados = 0

        self.moedasColetadas = 0


    def createTilemap(self):
        for i, row in enumerate(fase6):
            for j, column in enumerate(row):
                #Ground_crak1(self, j, i, ".")
                if column == ".":
                    Ground_crak1(self, j, i, ".")
                if column == "B":
                    Block_crack1(self, j, i, "B")
                if column == "G":
                    Block_crack1(self, j, i, "G")
                if column == "N":
                    Block_crack1(self, j, i, "N")
                if column == "T":  # LADO Esquerdo do tronco
                    Troncos(self, j, i, "T")
                if column == "L":  # LADO Direito do tronco
                    Troncos(self, j, i, "L")
                if column == "F":
                    Block_crack_efect(self, j, i, "F")
                if column == "H":
                    self.blocoMoedas = Bloco_especial(self, j, i, "H")
                if column == "O":
                    Bloco_solido(self, j, i, "O")
                if column == "#":
                    Bloco_dePoder(self, j, i)

                #Coletaveis
                if column == "M":
                    Moeda(self, j, i, True, False)
                if column == "A":
                    Cristal(self, j, i)
                if column == "I":
                    Poder(self, j, i, False)

                if column == "P":
                   self.player = Player_platform(self, j, i)

                ## Inimigos
                if column == "E":
                    Inimigo_esquilo(self, j, i)
                if column == "U":
                    Inimigo_urso(self, j, i)
                if column == "C":
                    Inimigo_coelho(self, j, i)

    def events(self, events):
        self.player.events(events)

    def mapa_carregar(self, mapa):
        self.mapa = mapa

    def update(self):
        self.scoreCristais.text_update("  x "+str(self.player.cristaiscoletados))
        self.scoreMoedas.text_update("  x "+str(self.player.moedasColetadas))
        self.scoreVidas.text_update("  x "+str(self.player.vidas))
        self.all_sprites.update()

    def draw(self, window):
        self.scoreCristais.draw(window, 20, 20)
        self.scoreMoedas.draw(window, 95, 20)
        self.scoreVidas.draw(window, 170, 20)
        self.all_sprites.draw(window)
