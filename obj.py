import pygame
from config import *
import math
import random
from dialogos import *



class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite


class Player(pygame.sprite.Sprite):

    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = "down"
        self.animation_loop = 1

        self.image = self.game.player_walk_back_right.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.falasTotal = len(dialogoCoveiro)
        self.falasDitas = 0
        self.destroy = False

        self.tempoFala = 400

        self.dialogoinicial= False #fase 1

        self.dialogoMultiploFazendeiros = False #dialogo entre hernandez e neto #fase 2
        self.dialogoNetoHernan = False

        self.dialogoMiguel = False #fase 3
        self.dialogoMultiploMiguelNeto = False #dialogo com a neta de miguel

        self.dialogoProfessora = False #dialogo principal #fase 4
        self.dialogoSecundarioProfessora = False  # dialogo secundario


        self.dialogoCoveiro = False #fase 5
        self.dialogoSecundarioCoveiro = False


        self.dialogoPadre = False #fase 6
        self.dialogoSecundarioPadre = False

        self.dialogoPrefeito = False  # fase 7
        self.dialogoSecundarioPrefeito = False
        self.faseFinal = False

        self.dialogoAtivo = False
        self.dialogoAtivoSecundario = False

        self.finalizarDialogoProfessora = False

        self.dialogoQuestFinal = False


        self.falasDialogo = ""
        self.falaAtiva = True

        self.nomePersonagem = ""


        # ajustar para entrega Final
        #if self.game.bkpfases['fase1'][1]:
            #if self.game.bkpfases['fase1'][3] >= 10:
               # self.cratera.kill()
           # else:
               # self.cratera = Crack(self.game, (self.x + 13), (self.y - 24))

    def update(self):
        self.movement()
        self.animate()
        self.collide_enemy()
        self.collide_crack()
        self.colisao_personagem1()
        self.colisao_personagem2()
        self.colisao_personagem2Secundario()
        self.colisao_personagem3()
        self.colisao_personagem3Secundario()
        self.colisao_personagem4()
        self.colisao_personagem5()
        self.colisao_personagem6()
        self.colisao_personagem7()
        self.colisao_personagemFinal()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0


        #dialogos

        if self.dialogoinicial: # fase 1
            self.falasDialogo = dialogoInicial
            self.nomePersonagem = 'Senhor perdido'
            self.dialogoAtivo = True

        if self.dialogoNetoHernan: # dialogo secundario segunda fase
            self.falasDialogo = dialogoNetoDoHernandez
            self.nomePersonagem = 'Neto de Hernandez'
            self.dialogoAtivoSecundario = True

        if self.dialogoMiguel: #fase 3
            self.falasDialogo = dialogoMiguel
            self.nomePersonagem = 'Miguel'
            self.dialogoAtivo = True

        if self.dialogoProfessora:
            self.falasDialogo = dialogoProfessora
            self.nomePersonagem = 'Professora'
            self.dialogoAtivo = True

        if self.dialogoSecundarioProfessora:
            self.falasDialogo = dialogoProfessoraSecumdario
            self.nomePersonagem = 'Professora'
            self.dialogoAtivoSecundario = True

        if self.dialogoCoveiro:
            self.falasDialogo = dialogoCoveiro
            self.nomePersonagem = 'Coveiro'
            self.dialogoAtivo = True

        if self.dialogoSecundarioCoveiro:
            self.falasDialogo = dialogoSecundarioCoveiro
            self.nomePersonagem = 'Coveiro'
            self.dialogoAtivoSecundario = True

        if self.dialogoPadre:
            self.falasDialogo = dialogoPadre
            self.nomePersonagem = 'Padre'
            self.dialogoAtivo = True

        if self.dialogoSecundarioPadre:
            self.falasDialogo = dialogoPadreSecundario
            self.nomePersonagem = 'Padre'
            self.dialogoAtivoSecundario = True

        if self.dialogoPrefeito:
            self.falasDialogo = dialogoPrefeito
            self.nomePersonagem = 'Prefeito'
            self.dialogoAtivo = True

        if self.dialogoSecundarioPrefeito:
            self.falasDialogo = dialogoSecundarioPrefeito
            self.nomePersonagem = 'Prefeito'
            self.dialogoAtivoSecundario = True

        if self.dialogoQuestFinal:
            self.falasDialogo = dialogoEnviadoDoTempo
            self.nomePersonagem = 'Enviado da Agencia'
            self.dialogoAtivoSecundario = True



        if self.dialogoAtivo:
            if self.falasDitas >= len(self.falasDialogo):
                self.dialogoCaixaFalas.kill()
                self.dialogoinicial = False  # fase 1

                self.dialogoNetoHernan = False

                self.dialogoMiguel = False  # fase 3

                self.dialogoProfessora = False  # dialogo principal #fase 4
                self.dialogoSecundarioProfessora = False  # dialogo secundario

                self.dialogoCoveiro = False  # fase 5
                self.dialogoSecundarioCoveiro = False

                self.dialogoPadre = False  # fase 6
                self.dialogoSecundarioPadre = False

                self.dialogoPrefeito = False #fase 7

                self.dialogoAtivo = False
                self.falasDitas = 0
                self.cratera = Crack(self.game, (self.x + 50), (self.y - 25))
            else:
                if self.tempoFala >= 0:
                    if self.falaAtiva:
                        self.dialogoCaixaFalas = Dialogo(self.game, (self.x + 60), (self.y + 100), self.falasDialogo[self.falasDitas], "jorge")
                        self.falaAtiva = False
                    self.tempoFala -= 1
                else:
                    self.dialogoCaixaFalas.kill()
                    self.tempoFala = 400
                    self.falasDitas += 1
                    self.falaAtiva = True

        #Dialogos secundarios
        if self.dialogoAtivoSecundario:
            if self.falasDitas >= len(self.falasDialogo):
                self.dialogoCaixaFalas.kill()
                self.dialogoNetoHernan = False #fase 1

                self.dialogoSecundarioProfessora = False  # dialogo secundario fase 4

                self.dialogoSecundarioCoveiro = False #fase 5

                self.dialogoSecundarioPadre = False #fase 6

                self.dialogoSecundarioPrefeito = False #fase 7

                self.dialogoAtivoSecundario = False

                if self.dialogoQuestFinal:
                    self.dialogoQuestFinal = False
                    self.game.fases = [False, False, False, False, False, False, False, False, True]

                self.falasDitas = 0
            else:
                if self.tempoFala >= 0:
                    if self.falaAtiva:
                        self.dialogoCaixaFalas = Dialogo(self.game, (self.x + 60), (self.y + 100),
                                                         self.falasDialogo[self.falasDitas], self.nomePersonagem)
                        self.falaAtiva = False
                    self.tempoFala -= 1
                else:
                    self.dialogoCaixaFalas.kill()
                    self.tempoFala = 400
                    self.falasDitas += 1
                    self.falaAtiva = True

        if self.dialogoMultiploFazendeiros:

            if self.falasDitas >= len(dialogoFazendeiro1):
                self.dialogoCaixaFalas.kill()
                self.dialogoMultiploFazendeiros = False
                self.falasDitas = 0
                self.cratera = Crack(self.game, (self.x + 50), (self.y - 25))
            else:
                if self.tempoFala >= 0:
                    if self.falaAtiva:
                        if self.falasDitas == 0 or self.falasDitas == 4 or self.falasDitas == 9 or self.falasDitas == 13:
                            self.nomePersonagem = 'Hernandez'
                        elif self.falasDitas == 1 or self.falasDitas == 6 or self.falasDitas == 11:
                            self.nomePersonagem = 'Neto de Hernandez'

                        self.dialogoCaixaFalas = Dialogo(self.game, (self.x + 60), (self.y + 100), dialogoFazendeiro1[self.falasDitas], self.nomePersonagem)
                        self.falaAtiva = False
                    self.tempoFala -= 1
                else:
                    self.dialogoCaixaFalas.kill()
                    self.tempoFala = 300
                    self.falasDitas += 1
                    self.falaAtiva = True

        #dialogo com a neta de miguel
        if self.dialogoMultiploMiguelNeto:

            if self.falasDitas >= len(dialogoNetaMiguel):
                self.dialogoCaixaFalas.kill()
                self.dialogoMultiploMiguelNeto = False
                self.falasDitas = 0
            else:
                if self.tempoFala >= 0:
                    if self.falaAtiva:
                        if self.falasDitas == 2:
                            self.nomePersonagem = 'Miguel'
                        elif self.falasDitas == 0 or self.falasDitas == 6:
                            self.nomePersonagem = 'Neta de Miguel'

                        self.dialogoCaixaFalas = Dialogo(self.game, (self.x + 60), (self.y + 100), dialogoNetaMiguel[self.falasDitas], self.nomePersonagem)
                        self.falaAtiva = False
                    self.tempoFala -= 1
                else:
                    self.dialogoCaixaFalas.kill()
                    self.tempoFala = 300
                    self.falasDitas += 1
                    self.falaAtiva = True

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'

        if keys[pygame.K_d]:
            self.x_change += PLAYER_SPEED
            self.facing = 'right'

        if keys[pygame.K_w]:
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'

        if keys[pygame.K_s]:
            self.y_change += PLAYER_SPEED
            self.facing = 'down'

    def events(self, events):
        pass

    # Fu??a?? que verifica colisao com os blocos
    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def animate(self):
        down_animations = [self.game.player_walk_back_right.get_sprite(0, 0, self.width, self.height),
                           self.game.player_walk_back_right.get_sprite(32, 0, self.width, self.height),
                           self.game.player_walk_back_right.get_sprite(64, 0, self.width, self.height)]

        up_animations = [self.game.player_walk_back_right.get_sprite(32, 32, self.width, self.height),
                         self.game.player_walk_back_right.get_sprite(32, 64, self.width, self.height),
                         self.game.player_walk_back_right.get_sprite(0, 64, self.width, self.height)]

        left_animations = [self.game.player_walk_left.get_sprite(0, 0, self.width, self.height),
                           self.game.player_walk_left.get_sprite(32, 0, self.width, self.height),
                           self.game.player_walk_left.get_sprite(0, 32, self.width, self.height),
                           self.game.player_walk_left.get_sprite(0, 64, self.width, self.height)]

        right_animations = [self.game.player_walk_right.get_sprite(0, 0, self.width, self.height),
                            self.game.player_walk_right.get_sprite(32, 0, self.width, self.height),
                            self.game.player_walk_right.get_sprite(0, 32, self.width, self.height),
                            self.game.player_walk_right.get_sprite(0, 64, self.width, self.height)]

        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.player_walk_back_right.get_sprite(0, 0, self.width, self.height)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.player_walk_back_right.get_sprite(32, 32, self.width, self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.player_walk_left.get_sprite(0, 0, self.width, self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.player_walk_right.get_sprite(0, 0, self.width, self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

    # colisao com os inimigos
    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)

        if hits:
            self.kill()
            self.game.playing = False

    # colisao com os portais
    def collide_crack(self):
        hits = pygame.sprite.spritecollide(self, self.game.cracks, False)

        if hits:
            self.game.fases = [False, False, False, False, False, False, False, False]

            self.game.fase1 = False
            self.game.fase2 = False
            self.game.fase3 = False
            self.game.fase4 = False
            self.game.fase5 = False
            self.game.fase6 = False
            self.game.fase7 = False


            if self.game.faseIniciar == "fase1":
                self.game.fases[1] = True
                self.game.fase1 = True
            if self.game.faseIniciar == "fase2":
                self.game.fases[2] = True
                self.game.fase2 = True

            if self.game.faseIniciar == "fase3":
                self.game.fases[3] = True
                self.game.fase3 = True

            if self.game.faseIniciar == "fase4":
                self.game.fases[4] = True
                self.game.fase4 = True

            if self.game.faseIniciar == "fase5":
                self.game.fases[5] = True
                self.game.fase5 = True

            if self.game.faseIniciar == "fase6":
                self.game.fases[6] = True
                self.game.fase6 = True

            if self.game.faseIniciar == "fase7":
                self.game.fases[7] = True
                self.game.fase7 = True


            hits[0].kill()

    # colisao personagens
    def colisao_personagem1(self):

        hits = pygame.sprite.spritecollide(self, self.game.fenda1, False)
        if hits:
            if not self.game.bkpfases['fase1'][1]:
                self.game.bkpfases['fase1'][0] = False # tira o simbolo de quest
                self.game.bkpfases['fase1'][1] = True
                self.game.faseIniciar = "fase1"
                self.dialogoinicial = True

    def colisao_personagem2(self):

        hits = pygame.sprite.spritecollide(self, self.game.fenda2, False)
        if hits:
            #verifica se a fase 1 foi finalizada
            if self.game.bkpfases['fase1'][2]:
                if not self.game.bkpfases['fase2'][1]: # vefica se a fase ja foi iniciada
                    self.game.bkpfases['fase2'][0] = True  # tira o simbolo de quest
                    self.game.bkpfases['fase2'][1] = True
                    self.game.faseIniciar = "fase2"
                    self.dialogoMultiploFazendeiros = True

    def colisao_personagem2Secundario(self):

        hits = pygame.sprite.spritecollide(self, self.game.fenda2Secunario, False)
        if hits:
            # verifica se a fase 2 foi finalizada
            if not self.game.bkpfases['fase2'][3]:
                    self.dialogoNetoHernan = True
                    self.game.bkpfases['fase2'][3] = True
                    self.game.bkpfases['fase3'][0] = True

    def colisao_personagem3(self):

        hits = pygame.sprite.spritecollide(self, self.game.fenda3, False)
        if hits:
            #verifica se a fase 2 foi finalizada
            if self.game.bkpfases['fase2'][2]:
                if not self.game.bkpfases['fase3'][1]:  # vefica se a fase ja foi iniciada
                    self.game.bkpfases['fase3'][0] = False  # tira o simbolo de quest
                    self.game.bkpfases['fase3'][1] = True
                    self.game.faseIniciar = "fase3"
                    self.dialogoMiguel = True

    def colisao_personagem3Secundario(self):

        hits = pygame.sprite.spritecollide(self, self.game.fenda3Secundario, False)
        if hits:
            # verifica se a fase 3 foi finalizada
            if not self.game.bkpfases['fase3'][3]:
                self.dialogoMultiploMiguelNeto = True
                self.game.bkpfases['fase3'][3] = True
                self.game.bkpfases['fase4'][0] = True

    def colisao_personagem4(self):

        hits = pygame.sprite.spritecollide(self, self.game.fenda4, False)
        if hits:
            #verifica se a fase 3 foi finalizada
            if self.game.bkpfases['fase3'][2]:
                if not self.game.bkpfases['fase4'][1]:  # vefica se a fase ja foi iniciada
                    self.game.bkpfases['fase4'][0] = False  # tira o simbolo de quest
                    self.game.bkpfases['fase4'][1] = True
                    self.game.faseIniciar = "fase4"
                    self.dialogoProfessora = True

            # verifica se a fase 4 foi finalizada
            if self.game.bkpfases['fase4'][2] and not self.finalizarDialogoProfessora:
                self.dialogoSecundarioProfessora = True
                self.game.bkpfases['fase4'][3] = True
                self.game.bkpfases['fase5'][0] = True
                self.finalizarDialogoProfessora = True

    def colisao_personagem5(self):

        hits = pygame.sprite.spritecollide(self, self.game.fenda5, False)
        if hits:
            #verifica se a fase 3 foi finalizada
            if self.game.bkpfases['fase4'][2]:
                if not self.game.bkpfases['fase5'][1]:  # vefica se a fase ja foi iniciada
                    self.game.bkpfases['fase5'][0] = False  # tira o simbolo de quest
                    self.game.bkpfases['fase5'][1] = True
                    self.game.faseIniciar = "fase5"
                    self.dialogoCoveiro = True

            # verifica se a fase 4 foi finalizada
            if self.game.bkpfases['fase5'][2] and not self.game.bkpfases['fase6'][0] :
                self.dialogoSecundarioCoveiro = True
                self.game.bkpfases['fase5'][3] = True
                self.game.bkpfases['fase6'][0] = True

    def colisao_personagem6(self):

        hits = pygame.sprite.spritecollide(self, self.game.fenda6, False)
        if hits:
            #verifica se a fase 3 foi finalizada
            if self.game.bkpfases['fase5'][2]:
                if not self.game.bkpfases['fase6'][1]:  # vefica se a fase ja foi iniciada
                    self.game.bkpfases['fase6'][0] = False  # tira o simbolo de quest
                    self.game.bkpfases['fase6'][1] = True
                    self.game.faseIniciar = "fase6"
                    self.dialogoPadre = True

            # verifica se a fase 4 foi finalizada
            if self.game.bkpfases['fase6'][2] and not self.game.bkpfases['fase7'][0] :
                self.dialogoSecundarioPadre = True
                self.game.bkpfases['fase6'][3] = True
                self.game.bkpfases['fase7'][0] = True


    def colisao_personagem7(self):

        hits = pygame.sprite.spritecollide(self, self.game.fenda7, False)
        if hits:
            #verifica se a fase 3 foi finalizada
            if self.game.bkpfases['fase6'][2]:
                if not self.game.bkpfases['fase7'][1]:  # vefica se a fase ja foi iniciada
                    self.game.bkpfases['fase7'][0] = False  # tira o simbolo de quest
                    self.game.bkpfases['fase7'][1] = True
                    self.game.faseIniciar = "fase7"
                    self.dialogoPrefeito = True

            # verifica se a fase 7 foi finalizada
            if self.game.bkpfases['fase7'][2] and not self.faseFinal:
                self.dialogoSecundarioPrefeito = True
                self.game.bkpfases['fase7'][3] = True
                self.game.bkpfases['fase7'][4] = True
                self.faseFinal = True
                personagen_final(self.game, (self.x+30), (self.y))
                self.game.questFinal = True

    def colisao_personagemFinal(self):

        hits = pygame.sprite.spritecollide(self, self.game.personagenFinal, False)
        if hits:
            # verifica se a fase 3 foi finalizada
            if self.game.questFinal:
                if self.game.bkpfases['fase7'][1]:  # vefica se a fase ja foi iniciada
                    self.game.questFinal = False  # tira o simbolo de quest
                    self.dialogoQuestFinal = True


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right'])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(7, 30)

        self.image = self.game.enemies_spritesheet.get_sprite(3, 2, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        if self.facing == 'left':
            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'right'

        if self.facing == 'right':
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'left'

    def animate(self):

        left_animations = [self.game.enemies_spritesheet.get_sprite(3, 98, self.width, self.height),
                           self.game.enemies_spritesheet.get_sprite(35, 98, self.width, self.height),
                           self.game.enemies_spritesheet.get_sprite(68, 98, self.width, self.height)]

        right_animations = [self.game.enemies_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.enemies_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.enemies_spritesheet.get_sprite(68, 66, self.width, self.height)]

        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.enemies_spritesheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.enemies_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(960, 448, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(64, 352, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Crack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.cracks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.portal.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.facing = "left"
        self.ticks = 1

    def update(self):
        self.anim()

    def anim(self):
        self.ticks += 1
        self.image = pygame.image.load("assets/portal/Portal_" + str(self.ticks) + ".png")

        if self.ticks >= 9:
            self.ticks = 1

#personagem fase 1
class personagen_padre(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.fenda1
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.padre.get_sprite(0, 32, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        if self.game.bkpfases['fase1'][0]:
           self.quest = quest(self.game, (self.rect.x+13), (self.rect.y - 24), True)

    def update(self):
        if not self.game.bkpfases['fase1'][0]:
            self.quest.kill()

#personagem fase 2
class personagen_hernandez(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.fenda2
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.fazendeiro1.get_sprite(0, 32, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.questAtiva = False

        self.ativarAQuest = True



    def update(self):

        if self.game.bkpfases['fase1'][2]:

            if self.ativarAQuest:
                self.questAtiva = True
                self.ativarAQuest = False
                self.quest = quest(self.game, (self.x + 13), (self.y - 24), True)
                #self.quest = quest(self.game, 0,0, True)

        if self.questAtiva:
            if self.game.bkpfases['fase2'][0]:
                self.quest.kill()

#personagem secundario fase 2
class personagen_neto_hernandez(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.fenda2Secunario
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.fazendeiro2.get_sprite(0, 32, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.questAtiva = False

        self.ativarAQuest = True


    def update(self):

        if self.game.bkpfases['fase2'][2]:
            if self.ativarAQuest:
                self.questAtiva = True
                self.ativarAQuest = False
                self.quest = quest(self.game, (self.rect.x + 13), (self.rect.y - 24), False)

        if self.questAtiva:
            if self.game.bkpfases['fase2'][3]:
                self.quest.kill()

#personagem miguel fase 3
class personagen_miguel(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.fenda3
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.fazendeiro3.get_sprite(0, 32, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.questAtiva = False

        self.ativarAQuest = True



    def update(self):

        if self.game.bkpfases['fase3'][0]:
            if self.ativarAQuest:
                self.questAtiva = True
                self.ativarAQuest = False
                self.quest = quest(self.game, (self.rect.x + 13), (self.rect.y - 24), True)

        if self.questAtiva:
            if not self.game.bkpfases['fase3'][0]:
                self.quest.kill()

#personagem secundario fase 3
class personagen_netaMiguel(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.fenda3Secundario
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.aluna.get_sprite(0, 32, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


        self.questAtiva = False

        self.ativarAQuest = True

    def update(self):

        if self.game.bkpfases['fase3'][2]:
            if self.ativarAQuest:
                self.questAtiva = True
                self.ativarAQuest = False
                self.quest = quest(self.game, (self.rect.x + 13), (self.rect.y - 24), False)

        if self.questAtiva:
            if self.game.bkpfases['fase3'][3]:
                self.quest.kill()

#personagem fase 4
class personagen_professora(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.fenda4
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.professora.get_sprite(0, 32, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.questAtiva = False

        self.ativarAQuest = True
        self.ativarAQuestSecundaria = True

        self.questSecundaria = False

    def update(self):

        if self.game.bkpfases['fase4'][0]:
            if self.ativarAQuest:
                self.questAtiva = True
                self.ativarAQuest = False
                self.quest = quest(self.game, (self.x + 13), (self.y - 24), True)
                # self.quest = quest(self.game, 0,0, True)

        if self.game.bkpfases['fase4'][2]:
            if self.ativarAQuestSecundaria:
                self.questAtiva = True
                self.ativarAQuestSecundaria = False
                self.questSecundaria = True
                self.quest = quest(self.game, (self.x + 13), (self.y - 24), False)
                # self.quest = quest(self.game, 0,0, True)

        if self.questAtiva:
            if not self.questSecundaria:
                if not self.game.bkpfases['fase4'][0]:
                    self.quest.kill()
            else:
                if self.game.bkpfases['fase5'][0]:
                    self.quest.kill()

#personagem fase 5
class personagen_coveiro(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.fenda5
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.coveiro.get_sprite(0, 32, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.questAtiva = False

        self.ativarAQuest = True
        self.ativarAQuestSecundaria = True

        self.questSecundaria = False

    def update(self):

        if self.game.bkpfases['fase5'][0]:
            if self.ativarAQuest:
                self.questAtiva = True
                self.ativarAQuest = False
                self.quest = quest(self.game, (self.x + 13), (self.y - 24), True)
                # self.quest = quest(self.game, 0,0, True)

        if self.game.bkpfases['fase5'][2]:
            if self.ativarAQuestSecundaria:
                self.questAtiva = True
                self.ativarAQuestSecundaria = False
                self.questSecundaria = True
                self.quest = quest(self.game, (self.x + 13), (self.y - 24), False)
                # self.quest = quest(self.game, 0,0, True)

        if self.questAtiva:
            if not self.questSecundaria:
                if not self.game.bkpfases['fase5'][0]:
                    self.quest.kill()
            else:
                if self.game.bkpfases['fase6'][0]:
                    self.quest.kill()

#personagem fase 6
class personagen_padre2(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.fenda6
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.padre.get_sprite(0, 32, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.questAtiva = False

        self.ativarAQuest = True
        self.ativarAQuestSecundaria = True

        self.questSecundaria = False

    def update(self):

        if self.game.bkpfases['fase6'][0]:
            if self.ativarAQuest:
                self.questAtiva = True
                self.ativarAQuest = False
                self.quest = quest(self.game, (self.x + 13), (self.y - 24), True)
                # self.quest = quest(self.game, 0,0, True)

        if self.game.bkpfases['fase6'][2]:
            if self.ativarAQuestSecundaria:
                self.questAtiva = True
                self.ativarAQuestSecundaria = False
                self.questSecundaria = True
                self.quest = quest(self.game, (self.x + 13), (self.y - 24), False)
                # self.quest = quest(self.game, 0,0, True)

        if self.questAtiva:
            if not self.questSecundaria:
                if not self.game.bkpfases['fase6'][0]:
                    self.quest.kill()
            else:
                if self.game.bkpfases['fase7'][0]:
                    self.quest.kill()

#personagem fase 7
class personagen_prefeito(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.fenda7
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.prefeito.get_sprite(0, 32, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.questAtiva = False

        self.ativarAQuest = True

        self.ativarAQuestSecundaria = True

        self.questSecundaria = False

    def update(self):
        if self.game.bkpfases['fase7'][0]:
            if self.ativarAQuest:
                self.questAtiva = True
                self.ativarAQuest = False
                self.quest = quest(self.game, (self.x + 13), (self.y - 24), True)
                # self.quest = quest(self.game, 0,0, True)

        if self.game.bkpfases['fase7'][2]:
            if self.ativarAQuestSecundaria:
                self.questAtiva = True
                self.ativarAQuestSecundaria = False
                self.questSecundaria = True
                self.quest = quest(self.game, (self.x + 13), (self.y - 24), False)
                # self.quest = quest(self.game, 0,0, True)

        if self.questAtiva:
            if not self.questSecundaria:
                if not self.game.bkpfases['fase7'][0]:
                    self.quest.kill()
            else:
                if self.game.bkpfases['fase7'][4]:
                    self.quest.kill()


#personagem final
class personagen_final(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.personagenFinal
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.indio.get_sprite(0, 32, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.questAtiva = False

        self.ativarAQuest = True

        self.ativarAQuestSecundaria = True

        self.questSecundaria = False

    def update(self):
        if self.game.questFinal:
            if self.ativarAQuest:
                self.questAtiva = True
                self.ativarAQuest = False
                self.quest = quest(self.game, (self.x + 13), (self.y - 24), True)
                # self.quest = quest(self.game, 0,0, True)


        if self.questAtiva:
            if not self.game.questFinal:
                self.quest.kill()


class quest(pygame.sprite.Sprite):
    def __init__(self, game, x, y, p):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = 10
        self.height = 42

        self.p = p

        if self.p:
            self.image = self.game.img_quest.get_sprite(0, 0, self.width, self.height)
        else:
            self.image = self.game.img_questSecundaria.get_sprite(0, 0, self.width, self.height)


        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.tempAniY = 10

        self.descer = False

    def update(self):
        if not self.descer:
            if self.tempAniY >= 0:
                self.rect.y -= 1
                self.tempAniY -= 1
            else:
                self.descer = True
                self.tempAniY = 10
        else:
            if self.tempAniY >= 0:
                self.rect.y += 1
                self.tempAniY -= 1
            else:
                self.descer = False
                self.tempAniY = 10


class Dialogo(pygame.sprite.Sprite):

    def __init__(self, game, x, y, dialogo, personagem):

        self.game = game
        self._layer = TEXT_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.nomePersonagem = personagem

        self.width = 570
        self.height = 100

        self.x = x
        self.y = y

        self.poder = Spritesheet("assets/caixaDialogo.png")

        self.image = self.poder.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


        pygame.font.init()

        self.font = pygame.font.Font("font/NORTHFOREST.ttf", 20)


        self.dialogo = dialogo
        self.posisaoTexto = 30

        self.posisaoTexto1 = 10

        self.falaReender =  ""
        self.falaDitas = 1

        self.cont = 0


        self.dialogo = self.dialogo.split("/")

        self.qtdFalas = len(self.dialogo)

        self.render = self.font.render(self.nomePersonagem + " :", False, (24, 25, 26))
        self.image.blit(self.render, (10, 10))

        if self.qtdFalas >= 2:
            while self.falaDitas <= self.qtdFalas:

                self.falaReender = str(self.dialogo[self.cont])

                self.render = self.font.render(self.falaReender, False, (24, 25, 26))
                self.image.blit(self.render, (self.posisaoTexto1, self.posisaoTexto))

                self.cont += 1
                self.posisaoTexto += 15
                self.falaDitas += 1
        else:
            self.render = self.font.render(self.dialogo[self.cont], False, (24, 25, 26))
            self.image.blit(self.render, (10, 30))


######## Blocos do mapa #############

class Bloco_rua(pygame.sprite.Sprite):
    def __init__(self, game, x, y, name):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        if name == "A":
            self.image = self.game.terrain_spritesheet.get_sprite(288, 64, self.width, self.height)
        elif name == "K":
            self.image = self.game.terrain_spritesheet.get_sprite(320, 64, self.width, self.height)
        elif name == "D":
            self.image = self.game.terrain_spritesheet.get_sprite(352, 64, self.width, self.height)
        elif name == "E":
            self.image = self.game.terrain_spritesheet.get_sprite(288, 96, self.width, self.height)
        elif name == "F":
            self.image = self.game.terrain_spritesheet.get_sprite(320, 96, self.width, self.height)
        elif name == "G":
            self.image = self.game.terrain_spritesheet.get_sprite(352, 96, self.width, self.height)
        elif name == "H":
            self.image = self.game.terrain_spritesheet.get_sprite(288, 128, self.width, self.height)
        elif name == "I":
            self.image = self.game.terrain_spritesheet.get_sprite(320, 128, self.width, self.height)
        elif name == "J":
            self.image = self.game.terrain_spritesheet.get_sprite(352, 128, self.width, self.height)


        elif name == "L":
            self.image = self.game.terrain_spritesheet.get_sprite(320, 0, self.width, self.height)
        elif name == "M":
            self.image = self.game.terrain_spritesheet.get_sprite(352, 0, self.width, self.height)
        elif name == "N":
            self.image = self.game.terrain_spritesheet.get_sprite(320, 32, self.width, self.height)
        elif name == "O":
            self.image = self.game.terrain_spritesheet.get_sprite(352, 32, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Blocos_farm(pygame.sprite.Sprite):
    def __init__(self, game, x, y, name):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        if name == "L":
            self.image = self.game.terrain_spritesheet_farm.get_sprite(32, 32, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


################################## FENDA 1 #########################################

class Block_crack1(pygame.sprite.Sprite):
    def __init__(self, game, x, y, name, img):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.plataforma, self.game.BlocosGerais
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE_CRACK1
        self.y = y * TILESIZE_CRACK1
        self.width = TILESIZE_CRACK1
        self.height = TILESIZE_CRACK1

        self.terrain_spritesheet = img

        if name == 'B':
            self.image = self.terrain_spritesheet.get_sprite(0, 0, self.width, self.height)
        elif name == 'G':
            self.image = self.terrain_spritesheet.get_sprite(0, 32, self.width, self.height)
        elif name == 'N':
            self.image = self.terrain_spritesheet.get_sprite(0, 66, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class bloco_invisivel(pygame.sprite.Sprite):
    def __init__(self, game, x, y, img):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.bloco_invisivel
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE_CRACK1
        self.y = y * TILESIZE_CRACK1
        self.width = TILESIZE_CRACK1
        self.height = TILESIZE_CRACK1

        self.terrain_spritesheet = img


        self.image = self.terrain_spritesheet.get_sprite(150, 150, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Block_plataforma_baixo(pygame.sprite.Sprite):
    def __init__(self, game, x, y, name, img):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.plataforma_baixo, self.game.BlocosGerais
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE_CRACK1
        self.y = y * TILESIZE_CRACK1
        self.width = TILESIZE_CRACK1
        self.height = TILESIZE_CRACK1

        self.terrain_spritesheet = img


        if name == 'G':
            self.image = self.terrain_spritesheet.get_sprite(0, 32, self.width, self.height)
        if name == '$':
            self.image = self.terrain_spritesheet.get_sprite(0, 0, self.width, self.height)
        if name == 'N':
            self.image = self.terrain_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Block_plataforma_solido(pygame.sprite.Sprite):
    def __init__(self, game, x, y, name, img):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.plataforma_solido, self.game.BlocosGerais
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE_CRACK1
        self.y = y * TILESIZE_CRACK1
        self.width = TILESIZE_CRACK1
        self.height = TILESIZE_CRACK1

        self.terrain_spritesheet = img


        if name == '$':
            self.image = self.terrain_spritesheet.get_sprite(0, 32, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Ground_crak1(pygame.sprite.Sprite):
    def __init__(self, game, x, y, name, img):

        self.game = game
        self._layer = SCREEN_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE_CRACK1
        self.y = y * TILESIZE_CRACK1
        self.width = TILESIZE_CRACK1
        self.height = TILESIZE_CRACK1

        self.terrain_spritesheet = img

        if name == "-":
            self.image = self.terrain_spritesheet.get_sprite(194, 33, self.width, self.height)
        elif name == ".":
            self.image = self.terrain_spritesheet.get_sprite(161, 34, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Troncos(pygame.sprite.Sprite):
    def __init__(self, game, x, y, name, img):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.troncos
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE_CRACK1
        self.y = y * TILESIZE_CRACK1
        self.width = TILESIZE_CRACK1
        self.height = TILESIZE_CRACK1

        self.terrain_spritesheet = img

        if name == "T":
            self.image = self.terrain_spritesheet.get_sprite(0, 131, self.width, self.height)
        elif name == "L":
            self.image = self.terrain_spritesheet.get_sprite(0, 99, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Block_crack_efect(pygame.sprite.Sprite):
    def __init__(self, game, x, y, name, img):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocoQuebraveis, self.game.BlocosGerais
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE_CRACK1
        self.y = y * TILESIZE_CRACK1
        self.width = TILESIZE_CRACK1
        self.height = TILESIZE_CRACK1

        self.terrain_spritesheet = img

        if name == "F":
            self.image = self.terrain_spritesheet.get_sprite(0, 66, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Bloco_solido(pygame.sprite.Sprite):
    def __init__(self, game, x, y, name, img):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.troncos, self.game.BlocosGerais
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE_CRACK1
        self.y = y * TILESIZE_CRACK1
        self.width = TILESIZE_CRACK1
        self.height = TILESIZE_CRACK1

        self.terrain_spritesheet = img

        if name == "O":
            self.image = self.terrain_spritesheet.get_sprite(96, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Bloco_solido_moeda(pygame.sprite.Sprite):
    def __init__(self, game, x, y, img):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.bloco_solido_moeda, self.game.BlocosGerais
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE_CRACK1
        self.height = TILESIZE_CRACK1

        self.terrain_spritesheet = img


        self.image = self.terrain_spritesheet.get_sprite(160, 67, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Bloco_especial(pygame.sprite.Sprite):
    def __init__(self, game, x, y, name, img):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocoEspeciaisMoedas, self.game.BlocosGerais
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE_CRACK1
        self.y = y * TILESIZE_CRACK1
        self.width = TILESIZE_CRACK1
        self.height = TILESIZE_CRACK1

        self.terrain_spritesheet = img

        if name == "H":
            self.image = self.terrain_spritesheet.get_sprite(96, 66, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def colisao(self):
        self.image = self.terrain_spritesheet.get_sprite(96, 66, self.width, self.height)


class Inimigo_esquilo(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.inimigo_pulo
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.salto = 0
        self.descer = 0
        self.espera = True
        self.tempo = 60

        self.subir = True

        self.x = x * TILESIZE_CRACK1
        self.y = y * TILESIZE_CRACK1
        self.width = TILESIZE_CRACK1
        self.height = TILESIZE_CRACK1

        self.image = self.game.inimigo_esquilo.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x - 15
        self.rect.y = self.y + 50

    def update(self):
        self.saltar()

    def saltar(self):

        if self.salto > 40:
            #personagem desce
            self.rect.y += 3
            self.descer += 1
            self.subir = False

        if self.descer > 40:
            self.salto = 0
            if self.espera:
                self.descer = 0
                self.subir = True
            else:
                if self.tempo >= 0:
                    self.tempo -= 1
                else:
                    self.espera = True
                    self.tempo = 60

        if self.subir:
            self.salto += 1
            #personagem sobe
            self.rect.y -= 3
            self.espera = False


class Inimigo_urso(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.inimigo
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE_CRACK1
        self.y = y * TILESIZE_CRACK1
        self.width = TILESIZE_CRACK1
        self.height = TILESIZE_CRACK1

        self.image = self.game.inimigo_urso.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.facing = "left"
        self.animation_loop = 1

        self.vel = 4
        self.grav = 1

    def update(self):
        self.animate()
        self.colisao_troncos()
        self.movement()
        self.gravity()
        self.colisions_plataforma()
        self.colisao_bloco_invisivel()

        if self.rect.y >= 672:
            self.kill()

    def gravity(self):
        self.vel += self.grav
        self.rect[1] += self.vel

        if self.vel >= 12:
            self.vel = 12


    def movement(self):
        if self.facing == 'left':
            self.rect.x -= 1

        elif self.facing == 'right':
            self.rect.x += 1

    def colisao_troncos(self):

        hits = pygame.sprite.spritecollide(self,  self.game.troncos, False)

        if hits:
            if (self.rect.x + (self.rect.width - 10)) >= hits[0].rect.left:
                self.facing = 'left'

            if (self.rect.x + self.rect.width) >= hits[0].rect.right:
                self.facing = 'right'

    def colisao_bloco_invisivel(self):

        hits = pygame.sprite.spritecollide(self, self.game.bloco_invisivel, False)

        if hits:
            if (self.rect.x + (self.rect.width - 10)) >= hits[0].rect.left:
                self.facing = 'left'

            if (self.rect.x + self.rect.width) >= hits[0].rect.right:
                self.facing = 'right'


    def animate(self):
        right_animations = [self.game.inimigo_urso.get_sprite(0, 0, self.width, self.height),
                           self.game.inimigo_urso.get_sprite(32, 0, self.width, self.height),
                           self.game.inimigo_urso.get_sprite(66, 0, self.width, self.height),
                           self.game.inimigo_urso.get_sprite(0, 33, self.width, self.height)]

        left_animations = [self.game.inimigo_urso.get_sprite(32, 32, self.width, self.height),
                            self.game.inimigo_urso.get_sprite(32, 65, self.width, self.height),
                            self.game.inimigo_urso.get_sprite(0, 65, self.width, self.height),
                            self.game.inimigo_urso.get_sprite(65, 98, self.width, self.height)]

        if self.facing == "left":
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "right":
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

    def colisions_plataforma(self):
        hits = pygame.sprite.spritecollide(self, self.game.BlocosGerais, False)
        if hits:
            self.pulo = True
            self.rect.bottom = hits[0].rect.top


class Inimigo_coelho(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.inimigo
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE_CRACK1
        self.y = y * TILESIZE_CRACK1
        self.width = TILESIZE_CRACK1
        self.height = TILESIZE_CRACK1

        self.image = self.game.inimigo_coelho.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.facing = "left"
        self.animation_loop = 1

        self.vel = 4
        self.grav = 1


    def update(self):
        self.animate()
        self.colisao_troncos()
        self.movement()
        self.gravity()
        self.colisions_plataforma()
        self.colisao_bloco_invisivel()

        if self.rect.y >= 672:
            self.kill()


    def gravity(self):
        self.vel += self.grav
        self.rect[1] += self.vel

        if self.vel >= 12:
            self.vel = 12


    def movement(self):
        if self.facing == 'left':
            self.rect.x -= 1

        elif self.facing == 'right':
            self.rect.x += 1

    def colisao_troncos(self):

        hits = pygame.sprite.spritecollide(self, self.game.troncos, False)

        if hits:

            if (self.rect.x + (self.rect.width - 10)) >= hits[0].rect.left:
                self.facing = 'left'

            if (self.rect.x + self.rect.width) >= hits[0].rect.right:
                self.facing = 'right'

    def colisions_plataforma(self):
        hits = pygame.sprite.spritecollide(self, self.game.BlocosGerais, False)
        if hits:
            self.pulo = True
            self.rect.bottom = hits[0].rect.top

    def colisao_bloco_invisivel(self):

        hits = pygame.sprite.spritecollide(self, self.game.bloco_invisivel, False)

        if hits:
            if (self.rect.x + (self.rect.width - 10)) >= hits[0].rect.left:
                self.facing = 'left'

            if (self.rect.x + self.rect.width) >= hits[0].rect.right:
                self.facing = 'right'


    def animate(self):
        right_animations = [self.game.inimigo_coelho.get_sprite(0, 0, self.width, self.height),
                           self.game.inimigo_coelho.get_sprite(32, 0, self.width, self.height),
                           self.game.inimigo_coelho.get_sprite(66, 0, self.width, self.height),
                           self.game.inimigo_coelho.get_sprite(0, 33, self.width, self.height)]

        left_animations = [self.game.inimigo_coelho.get_sprite(32, 32, self.width, self.height),
                            self.game.inimigo_coelho.get_sprite(32, 65, self.width, self.height),
                            self.game.inimigo_coelho.get_sprite(0, 65, self.width, self.height),
                            self.game.inimigo_coelho.get_sprite(65, 98, self.width, self.height)]

        if self.facing == "left":
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "right":
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1


class Bloco_dePoder(pygame.sprite.Sprite):
    def __init__(self, game, x, y, img):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.bloco_dePoder_acao
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE_CRACK1
        self.y = y * TILESIZE_CRACK1
        self.width = TILESIZE_CRACK1
        self.height = TILESIZE_CRACK1

        self.terrain_spritesheet = img


        self.image = self.terrain_spritesheet.get_sprite(96, 66, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def colisao(self):
        self.image = self.terrain_spritesheet.get_sprite(96, 66, self.width, self.height)


class Moeda(pygame.sprite.Sprite):
    def __init__(self, game, x, y, p, temp):

        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites,  self.game.coletar_moeda
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.width = TILESIZE_CRACK1
        self.height = TILESIZE_CRACK1

        self.temp = temp

        if p:
            self.x = x * TILESIZE_CRACK1
            self.y = y * TILESIZE_CRACK1
        else:
            self.x = x
            self.y = y

        self.moeda = Spritesheet("assets/moeda.png")

        self.image = self.moeda.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.ticks = 0
        self.animation_loop = 1
        self.tempMoeda = 0

    def update(self):
        self.animate()

        if self.temp:
            self.tempMoeda += 1
            self.rect.y -= 1
            if self.tempMoeda >= 10:
                self.kill()


    def animate(self):
        animations = [self.moeda.get_sprite(0, 0, self.width, self.height),
                       self.moeda.get_sprite(0, 32, self.width, self.height),
                       self.moeda.get_sprite(0, 64, self.width, self.height),
                       self.moeda.get_sprite(0, 99, self.width, self.height)]

        self.image = animations[math.floor(self.animation_loop)]
        self.animation_loop += 0.1
        if self.animation_loop >= 4:
            self.animation_loop = 1


class Cristal(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.coletar_cristal
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE_CRACK1
        self.y = y * TILESIZE_CRACK1
        self.width = TILESIZE_CRACK1
        self.height = TILESIZE_CRACK1

        self.image = self.game.cristal.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.ticks = 0
        self.animation_loop = 1

    def update(self):
        self.animate()


    def animate(self):
        animations = [self.game.cristal.get_sprite(0, 0, self.width, self.height),
                       self.game.cristal.get_sprite(32, 0, self.width, self.height),
                       self.game.cristal.get_sprite(0, 32, self.width, self.height)]

        self.image = animations[math.floor(self.animation_loop)]
        self.animation_loop += 0.1
        if self.animation_loop >= 3:
            self.animation_loop = 1


class Poder(pygame.sprite.Sprite):
    def __init__(self, game, x, y, p):

        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.poder_coletavel
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.width = TILESIZE_CRACK1
        self.height = TILESIZE_CRACK1

        if p:
            self.x = x * TILESIZE_CRACK1
            self.y = y * TILESIZE_CRACK1
        else:
            self.x = x
            self.y = y

        self.poder = Spritesheet("assets/pina_colada.png")

        self.image = self.poder.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Tiro(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.tiro = Spritesheet("assets/tiro.png")

        self.x = x
        self.y = y

        self.image = self.tiro.get_sprite(0, 0, 1, 1)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.ticks = 0
        self.animation_loop = 1

        self.direcao = 'd'
        self.subir = 0

    def update(self):
        self.animate()
        self.movement()
        self.colisao_troncos()
        self.colisao_plataforma()
        self.colisao_inimigo()
        self.colisao_inimigoQpula()

    def colisao_troncos(self):

        hits = pygame.sprite.spritecollide(self, self.game.troncos, False)
        if hits:
            self.kill()
            self.game.tirosCriados -= 1

    def colisao_plataforma(self):

        hits = pygame.sprite.spritecollide(self, self.game.plataforma, False)
        if hits:
            if (self.rect.y + self.rect.height) >= hits[0].rect.top:
                   self.direcao = 's'
                   self.subir = 0
            else:
                self.kill()
                self.game.tirosCriados -= 1

    def colisao_inimigo(self):
        hits = pygame.sprite.spritecollide(self, self.game.inimigo, True)
        if hits:
            self.kill()

    def colisao_inimigoQpula(self):
        hits = pygame.sprite.spritecollide(self, self.game.inimigo_pulo, True)
        if hits:
            self.kill()

    def movement(self):

        if self.direcao == 'd':
            self.rect.x += 3
            self.rect.y += 3
        elif self.direcao == 's':

            self.rect.x += 3
            self.rect.y -= 3
            self.subir += 1
            if self.subir >= 10:
                self.direcao = 'd'

    def animate(self):
        animations = [self.tiro.get_sprite(0, 0, 9, 9),
                       self.tiro.get_sprite(9, 0, 9, 9),
                       self.tiro.get_sprite(0, 9, 9, 9),
                        self.tiro.get_sprite(9, 9, 9, 9)]

        self.image = animations[math.floor(self.animation_loop)]
        self.animation_loop += 0.1
        if self.animation_loop >= 3:
            self.animation_loop = 1


class portal_Voltar(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.portal_voltar
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.portal.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.facing = "left"
        self.ticks = 1

    def update(self):
        self.anim()

    def anim(self):
        self.ticks += 1
        self.image = pygame.image.load("assets/portal/Portal_" + str(self.ticks) + ".png")

        if self.ticks >= 9:
            self.ticks = 1


class Player_platform(pygame.sprite.Sprite):

    def __init__(self, game, x, y, p, boss):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = "down"
        self.animation_loop = 1

        self.image = self.game.player_walk_back_right.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.vel = 4
        self.grav = 1

        self.pulo = True

        self.movimentacao4lados = p

        self.moedasColetadas = 0
        self.cristaiscoletados = 0
        self.vidas = 3

        self.invulneravel = False
        self.tempoInvulneravel = 100

        self.poderAtivo = False
        self.tempoPoder = 400


        self.boss = boss

        # sons
        pygame.mixer.init()
        self.volumeMusic = 0.5

        self.audio_coin = pygame.mixer.Sound("assets/sounds/smb3_coin.wav")
        self.audio_jump = pygame.mixer.Sound("assets/sounds/smb3_frog_mario_walk.wav")
        self.audio_tiro = pygame.mixer.Sound("assets/sounds/smb3_fireball.wav")
        self.audio_cristal = pygame.mixer.Sound("assets/sounds/cristal.wav")
        self.audio_morte = pygame.mixer.Sound("assets/sounds/morte.wav")
        self.audio_perderVida = pygame.mixer.Sound("assets/sounds/perderVida.wav")
        self.audio_quebrarBloco = pygame.mixer.Sound("assets/sounds/smb3_break_brick_block.wav")
        self.audio_PegarPoder = pygame.mixer.Sound("assets/sounds/smb3_mushroom_appears.wav")

    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.collide_blocks()

        self.gravity()
        self.colisions_plataforma()
        self.colisao_blocosQuebraveis()
        self.colisao_blocoMoeda()
        self.colisao_blocoSolidoMoeda()
        self.colisao_Moeda()
        self.colisao_Cristal()
        self.colisao_Bloco_dePoder()
        self.colisao_Poder()
        self.colisao_Portal()

        self.collide_plataforma_baixo()
        self.collide_plataforma_solido()

        # tempo de ivulneral apos um hit em inimigos
        if not self.invulneravel:
            self.colisao_Inimigos()
            self.colisao_InimigosQPula()
        else:
            if self.tempoInvulneravel >= 0:
                self.tempoInvulneravel -= 1
            else:
                self.tempoInvulneravel = 100
                self.invulneravel = False

        #tempo ativo do poder
        if self.poderAtivo:
            if self.tempoPoder >= 0:
                self.tempoPoder -= 1
            else:
                self.tempoPoder = 400
                self.poderAtivo = False
                self.game.tirosCriados = 0

        self.x_change = 0
        self.y_change = 0

        if self.movimentacao4lados:
            if self.rect.y >= 672:
                for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED
        else:
            if self.rect.y >= 672:
                self.game.restartFase = True


    def gravity(self):
        self.vel += self.grav
        self.rect[1] += self.vel

        if self.vel >= 12:
            self.vel = 12

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            if self.movimentacao4lados:
                for sprite in self.game.all_sprites:
                    if self.rect.x < (WIN_WIDTH / 2):
                        sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'

        if keys[pygame.K_d]:
            for sprite in self.game.all_sprites:
                if not self.boss:
                    if self.rect.x >= (WIN_WIDTH / 2):
                        sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'

    def events(self, events):
        if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_SPACE:
                self.audio_jump.play()
                self.audio_jump.set_volume(self.volumeMusic)
                self.pulo = False
                self.vel *= -1.5
            if events.key == pygame.K_q:
                if self.poderAtivo:
                    self.audio_tiro.play()
                    self.audio_tiro.set_volume(self.volumeMusic)
                    self.game.tirosCriados += 1

                    if self.game.tirosCriados <= 3:
                        poder_tiro = Tiro(self.game, (self.rect.x + self.rect.width), (self.rect.y + 15))

    # Fu??a?? que verifica colisao com os troncos
    def collide_blocks(self):
        hits = pygame.sprite.spritecollide(self, self.game.troncos, False)

        if hits:
            if self.pulo:
                if (self.rect.x + self.rect.width) >= hits[0].rect.left:
                    if (self.rect.x + self.rect.width) <= hits[0].rect.right:
                        self.rect.x = hits[0].rect.left - self.rect.width
                    else:
                        self.rect.x = hits[0].rect.right

            else:
                if (self.rect.y + self.rect.height) >= hits[0].rect.top:
                    self.rect.y = hits[0].rect.top - (self.rect.height + 10)

    # Fu??a?? que verifica colisao com os blocos quebraveis
    def colisao_blocosQuebraveis(self):
        hits = pygame.sprite.spritecollide(self, self.game.blocoQuebraveis, False)

        if hits:

            if not self.pulo:
                # se esta a cima do bloco
                if (self.rect.y + self.rect.height) >= hits[0].rect.top:
                    #se esta a baixo do bloco
                    if (self.rect.y + self.rect.height) >= hits[0].rect.bottom:
                        #posisiona a cabe??a do boneco em baixo do bloco
                        self.rect.y = hits[0].rect.bottom
                        self.audio_quebrarBloco.play()
                        self.audio_quebrarBloco.set_volume(self.volumeMusic)
                        hits[0].kill()
                    else:
                        #posisiona as pernas do player em cima do bloco
                        self.rect.y = hits[0].rect.top - (self.rect.height)

            else:
                #se colidir com a esquerda do bloco
                if (self.rect.x + self.rect.width) >= hits[0].rect.left:

                    #se colidiu com direita do bloco
                    if (self.rect.x + self.rect.width) <= hits[0].rect.right:
                        if (self.rect.y + self.rect.height) >= hits[0].rect.bottom:
                            self.rect.x = hits[0].rect.left - self.rect.width

                    else:
                        self.rect.x = hits[0].rect.right

    # Fu??a?? que verifica colisao com os blocos de moedas
    def colisao_blocoMoeda(self):
        hits = pygame.sprite.spritecollide(self, self.game.blocoEspeciaisMoedas, False)

        if hits:

            if not self.pulo:
                # se esta a cima do bloco
                if (self.rect.y + self.rect.height) >= hits[0].rect.top:
                    # se esta a baixo do bloco
                    if (self.rect.y + self.rect.height) >= hits[0].rect.bottom:
                        # posisiona a cabe??a do boneco em baixo do bloco
                        self.rect.y = hits[0].rect.bottom
                        Moeda(self.game, (hits[0].rect.x+1), (hits[0].rect.y-26), False, True)
                        Bloco_solido_moeda(self.game, hits[0].rect.x, hits[0].rect.y, self.game.terrain_spritesheet)
                        self.audio_coin.play()
                        self.audio_coin.set_volume(self.volumeMusic)
                        self.moedasColetadas += 1
                        hits[0].kill()
                    else:
                        # posisiona as pernas do player em cima do bloco
                        self.rect.y = hits[0].rect.top - (self.rect.height)

            else:
                # se colidir com a esquerda do bloco
                if (self.rect.x + self.rect.width) >= hits[0].rect.left:

                    # se colidiu com direita do bloco
                    if (self.rect.x + self.rect.width) <= hits[0].rect.right:
                        if (self.rect.y + self.rect.height) >= hits[0].rect.bottom:
                            self.rect.x = hits[0].rect.left - self.rect.width
                    else:
                        self.rect.x = hits[0].rect.right

    def colisao_Bloco_dePoder(self):
        hits = pygame.sprite.spritecollide(self, self.game.bloco_dePoder_acao, False)

        if hits:

            if not self.pulo:
                # se esta a cima do bloco
                if (self.rect.y + self.rect.height) >= hits[0].rect.top:
                    # se esta a baixo do bloco
                    if (self.rect.y + self.rect.height) >= hits[0].rect.bottom:
                        # posisiona a cabe??a do boneco em baixo do bloco
                        self.rect.y = hits[0].rect.bottom
                        Poder(self.game, (hits[0].rect.x+1), (hits[0].rect.y-32), False)
                        Bloco_solido_moeda(self.game, hits[0].rect.x, hits[0].rect.y, self.game.terrain_spritesheet)
                        hits[0].kill()
                    else:
                        # posisiona as pernas do player em cima do bloco
                        self.rect.y = hits[0].rect.top - (self.rect.height)

            else:
                # se colidir com a esquerda do bloco
                if (self.rect.x + self.rect.width) >= hits[0].rect.left:

                    # se colidiu com direita do bloco
                    if (self.rect.x + self.rect.width) <= hits[0].rect.right:
                        if (self.rect.y + self.rect.height) >= hits[0].rect.bottom:
                            self.rect.x = hits[0].rect.left - self.rect.width
                    else:
                        self.rect.x = hits[0].rect.right

    def colisao_blocoSolidoMoeda(self):
        hits = pygame.sprite.spritecollide(self, self.game.bloco_solido_moeda, False)

        if hits:

            if not self.pulo:
                # se esta a cima do bloco
                if (self.rect.y + self.rect.height) >= hits[0].rect.top:
                    # se esta a baixo do bloco
                    if (self.rect.y + self.rect.height) >= hits[0].rect.bottom:
                        # posisiona a cabe??a do boneco em baixo do bloco
                        self.rect.y = hits[0].rect.bottom
                    else:
                        # posisiona as pernas do player em cima do bloco
                        self.rect.y = hits[0].rect.top - (self.rect.height)

            else:
                # se colidir com a esquerda do bloco
                if (self.rect.x + self.rect.width) >= hits[0].rect.left:

                    # se colidiu com direita do bloco
                    if (self.rect.x + self.rect.width) <= hits[0].rect.right:
                        if (self.rect.y + self.rect.height) >= hits[0].rect.bottom:
                            self.rect.x = hits[0].rect.left - self.rect.width
                    else:
                        self.rect.x = hits[0].rect.right

    def colisao_Moeda(self):
        hits = pygame.sprite.spritecollide(self,  self.game.coletar_moeda, False)

        if hits:
            self.audio_coin.play()
            self.audio_coin.set_volume(self.volumeMusic)
            self.moedasColetadas += 1
            hits[0].kill()

    def colisao_Cristal(self):
        hits = pygame.sprite.spritecollide(self,  self.game.coletar_cristal, False)

        if hits:
            self.audio_cristal.play()
            self.audio_cristal.set_volume(self.volumeMusic)
            self.cristaiscoletados += 1
            hits[0].kill()

    def colisao_Poder(self):
        hits = pygame.sprite.spritecollide(self,  self.game.poder_coletavel, False)

        if hits:
            self.audio_PegarPoder.play()
            self.audio_PegarPoder.set_volume(self.volumeMusic)
            self.poderAtivo = True
            hits[0].kill()

    def colisions_plataforma(self):

        hits = pygame.sprite.spritecollide(self, self.game.plataforma, False)
        if hits:
            if (self.rect.y + self.rect.height) >= hits[0].rect.top:
                # se esta a baixo do bloco
                if (self.rect.y + self.rect.height) >= hits[0].rect.bottom:
                    # posisiona a cabe??a do boneco em baixo do bloco
                    self.rect.y = hits[0].rect.bottom
                elif (self.rect.bottom >= hits[0].rect.top):
                    # posisiona as pernas do player em cima do bloco
                    self.rect.bottom = hits[0].rect.top
                    self.pulo = True

    def collide_plataforma_baixo(self):
        hits = pygame.sprite.spritecollide(self, self.game.plataforma_baixo, False)

        if hits:
            if self.pulo:
                if (self.rect.x + self.rect.width) >= hits[0].rect.left:
                    if (self.rect.x + self.rect.width) <= hits[0].rect.right:
                        self.rect.x = hits[0].rect.left - self.rect.width
                    else:
                        self.rect.x = hits[0].rect.right

            else:
                if (self.rect.y + self.rect.height) >= hits[0].rect.top:
                    self.rect.y = hits[0].rect.top - (self.rect.height + 10)


    def collide_plataforma_solido(self):
        hits = pygame.sprite.spritecollide(self, self.game.plataforma_solido, False)

        if hits:
            if not self.pulo:
                # se esta a cima do bloco
                if (self.rect.y + self.rect.height) >= hits[0].rect.top:
                    # se esta a baixo do bloco
                    if (self.rect.y + self.rect.height) >= hits[0].rect.bottom:
                        # posisiona a cabe??a do boneco em baixo do bloco
                        self.rect.y = hits[0].rect.bottom
                    else:
                        # posisiona as pernas do player em cima do bloco
                        self.rect.y = hits[0].rect.top - (self.rect.height)

            else:
                # se colidir com a esquerda do bloco
                if (self.rect.x + self.rect.width) >= hits[0].rect.left:

                    # se colidiu com direita do bloco
                    if (self.rect.x + self.rect.width) <= hits[0].rect.right:
                        if (self.rect.y + self.rect.height) >= hits[0].rect.bottom:
                            self.rect.x = hits[0].rect.left - self.rect.width
                    else:
                        self.rect.x = hits[0].rect.right

    def colisao_Inimigos(self):
        hits = pygame.sprite.spritecollide(self, self.game.inimigo, False)

        if hits:

            if not self.pulo:
                # se esta a cima do inikigo
                if (self.rect.y + self.rect.height) >= hits[0].rect.top:
                    hits[0].kill()

            else:

                if self.vidas <= 0:
                    self.audio_morte.play()
                    self.audio_morte.set_volume(self.volumeMusic)
                    self.kill()
                    self.game.restartFase = True
                else:
                    self.invulneravel = True
                    self.audio_perderVida.play()
                    self.audio_perderVida.set_volume(self.volumeMusic)
                    self.vidas -= 1

    def colisao_InimigosQPula(self):
        hits = pygame.sprite.spritecollide(self, self.game.inimigo_pulo, False)

        if hits:
            if self.vidas <= 0:
                self.audio_morte.play()
                self.audio_morte.set_volume(self.volumeMusic)
                self.kill()
                self.game.restartFase = True
            else:
                self.invulneravel = True
                self.audio_perderVida.play()
                self.audio_perderVida.set_volume(self.volumeMusic)
                self.vidas -= 1

    def animate(self):
        left_animations = [self.game.player_walk_left.get_sprite(0, 0, self.width, self.height),
                           self.game.player_walk_left.get_sprite(32, 0, self.width, self.height),
                           self.game.player_walk_left.get_sprite(0, 32, self.width, self.height),
                           self.game.player_walk_left.get_sprite(0, 64, self.width, self.height)]

        right_animations = [self.game.player_walk_right.get_sprite(0, 0, self.width, self.height),
                            self.game.player_walk_right.get_sprite(32, 0, self.width, self.height),
                            self.game.player_walk_right.get_sprite(0, 32, self.width, self.height),
                            self.game.player_walk_right.get_sprite(0, 64, self.width, self.height)]

        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.player_walk_left.get_sprite(0, 0, self.width, self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.player_walk_right.get_sprite(0, 0, self.width, self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

    def colisao_Portal(self):
        hits = pygame.sprite.spritecollide(self,  self.game.portal_voltar, False)

        if hits:
            self.game.voltarFase = True
            self.game.reentradaFase = True
            self.game.faseFinalizada = True
            #self.game.bkpfases[self.game.faseIniciar][3] = self.cristaiscoletados


class Text:

    def __init__(self, size, text, img):
        pygame.font.init()
        self._layer = TEXT_LAYER
        self.image = pygame.image.load(img)

        self.font = pygame.font.Font("font/HungryCharlie-Serif.ttf", size)
        self.render = self.font.render(text, False, (255, 255, 255))

    def draw(self, window, x, y):
        window.blit(self.image, (x, y))
        window.blit(self.render, (x+10, y))


    def text_update(self, text):
        self.render = self.font.render(text, False, (255, 255, 255))

###################### CENAS ########################


class primeiraCena(pygame.sprite.Sprite):
    def __init__(self, game, x, y, img):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.img = img
        self.image = pygame.image.load(self.img)
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = y

        self.x = x
        self.y = y

        self.dialogoMultiplo = True

        self.falaAtiva = True

        self.tempoFala = 300

        self.falasDitas = 0

        self.nomePersonagem = ""


    def update(self):

        if self.dialogoMultiplo:

            if self.falasDitas >= len(dialogoSenhoresDoTempo):
                self.dialogoCaixaFalas.kill()
                self.dialogoMultiplo = False
                self.falasDitas = 0
                self.game.passarCena = False
            else:
                if self.tempoFala >= 0:
                    if self.falaAtiva:
                        if self.falasDitas == 0 or self.falasDitas == 6 or self.falasDitas == 10:
                            self.nomePersonagem = '753'
                        elif self.falasDitas == 4 or self.falasDitas == 9 or self.falasDitas == 11:
                            self.nomePersonagem = '159'

                        self.dialogoCaixaFalas = Dialogo(self.game, (self.x + 335), (self.y + 500),
                                                         dialogoSenhoresDoTempo[self.falasDitas], self.nomePersonagem)
                        self.falaAtiva = False
                    self.tempoFala -= 1
                else:
                    self.dialogoCaixaFalas.kill()
                    self.tempoFala = 300
                    self.falasDitas += 1
                    self.falaAtiva = True

class segundaCena(pygame.sprite.Sprite):
    def __init__(self, game, x, y, img):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.img = img
        self.image = pygame.image.load(self.img)
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = y

        self.x = x
        self.y = y

        self.dialogoMultiplo = True

        self.falaAtiva = True

        self.tempoFala = 300

        self.falasDitas = 0

        self.nomePersonagem = ""


    def update(self):

        if self.dialogoMultiplo:

            if self.falasDitas >= len(dialogoSenhorDoTempoEestagiario):
                self.dialogoCaixaFalas.kill()
                self.dialogoMultiplo = False
                self.falasDitas = 0
                self.game.passarCena = False
            else:
                if self.tempoFala >= 0:
                    if self.falaAtiva:
                        self.nomePersonagem = 'Senhor do Tempo'

                        self.dialogoCaixaFalas = Dialogo(self.game, (self.x + 270), (self.y + 550),
                                                         dialogoSenhorDoTempoEestagiario[self.falasDitas], self.nomePersonagem)
                        self.falaAtiva = False
                    self.tempoFala -= 1
                else:
                    self.dialogoCaixaFalas.kill()
                    self.tempoFala = 400
                    self.falasDitas += 1
                    self.falaAtiva = True

class terceiraCena(pygame.sprite.Sprite):
    def __init__(self, game, x, y, img):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.img = img
        self.image = pygame.image.load(self.img)
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = y

        self.x = x
        self.y = y

        self.dialogoMultiplo = True

        self.falaAtiva = True

        self.tempoFala = 300

        self.falasDitas = 0

        self.nomePersonagem = ""


    def update(self):

        if self.dialogoMultiplo:

            if self.falasDitas >= len(dialogoFinal):
                self.dialogoCaixaFalas.kill()
                self.dialogoMultiplo = False
                self.falasDitas = 0
                self.game.passarCena = False

                self.image = pygame.image.load("assets/cenas/cena7.jpeg")
            else:
                if self.tempoFala >= 0:
                    if self.falaAtiva:
                        self.nomePersonagem = 'Narrador'

                        if self.falasDitas == 2:
                            self.image = pygame.image.load("assets/cenas/cena4.jpeg")

                        if self.falasDitas == 3:
                            self.image = pygame.image.load("assets/cenas/cena5.jpeg")

                        if self.falasDitas == 4:
                            self.image = pygame.image.load("assets/cenas/cena6.png")

                        self.dialogoCaixaFalas = Dialogo(self.game, (self.x + 270), (self.y + 550),
                                                         dialogoFinal[self.falasDitas], self.nomePersonagem)
                        self.falaAtiva = False
                    self.tempoFala -= 1
                else:
                    self.dialogoCaixaFalas.kill()
                    self.tempoFala = 400
                    self.falasDitas += 1
                    self.falaAtiva = True
