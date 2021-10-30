import pygame
from config import *
import math
import random


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

    def update(self):
        self.movement()
        self.animate()
        self.collide_enemy()
        self.collide_crack()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            for sprite in self.game.all_sprites:
                if self.rect.x < (WIN_WIDTH / 2):
                    sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'

        if keys[pygame.K_d]:
            for sprite in self.game.all_sprites:
                if self.rect.x >= (WIN_WIDTH / 2):
                    sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'

        if keys[pygame.K_w]:
            for sprite in self.game.all_sprites:
                if self.rect.y < (WIN_HEIGHT / 2):
                    sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'

        if keys[pygame.K_s]:
            for sprite in self.game.all_sprites:
                if self.rect.y > (WIN_HEIGHT / 2):
                    sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            self.facing = 'down'

    # Fuçaõ que verifica colisao com os blocos
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
            self.game.change_scene = True


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

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(864, 160, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


################################## FENDA 1 #########################################

class Block_crack1(pygame.sprite.Sprite):
    def __init__(self, game, x, y, name):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.plataforma
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE_CRACK1
        self.y = y * TILESIZE_CRACK1
        self.width = TILESIZE_CRACK1
        self.height = TILESIZE_CRACK1

        if name == 'B':
            self.image = self.game.terrain_spritesheet.get_sprite(0, 0, self.width, self.height)
        elif name == 'G':
            self.image = self.game.terrain_spritesheet.get_sprite(0, 32, self.width, self.height)
        elif name == 'N':
            self.image = self.game.terrain_spritesheet.get_sprite(0, 66, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Ground_crak1(pygame.sprite.Sprite):
    def __init__(self, game, x, y, name):

        self.game = game
        self._layer = SCREEN_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE_CRACK1
        self.y = y * TILESIZE_CRACK1
        self.width = TILESIZE_CRACK1
        self.height = TILESIZE_CRACK1

        if name == "-":
            self.image = self.game.terrain_spritesheet.get_sprite(194, 33, self.width, self.height)
        elif name == ".":
            self.image = self.game.terrain_spritesheet.get_sprite(161, 34, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Troncos(pygame.sprite.Sprite):
    def __init__(self, game, x, y, name):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.troncos
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE_CRACK1
        self.y = y * TILESIZE_CRACK1
        self.width = TILESIZE_CRACK1
        self.height = TILESIZE_CRACK1

        if name == "T":
            self.image = self.game.terrain_spritesheet.get_sprite(0, 131, self.width, self.height)
        elif name == "L":
            self.image = self.game.terrain_spritesheet.get_sprite(0, 99, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Block_crack_efect(pygame.sprite.Sprite):
    def __init__(self, game, x, y, name):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocoQuebraveis
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE_CRACK1
        self.y = y * TILESIZE_CRACK1
        self.width = TILESIZE_CRACK1
        self.height = TILESIZE_CRACK1

        if name == "F":
            self.image = self.game.terrain_spritesheet.get_sprite(0, 66, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Bloco_solido(pygame.sprite.Sprite):
    def __init__(self, game, x, y, name):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.troncos
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE_CRACK1
        self.y = y * TILESIZE_CRACK1
        self.width = TILESIZE_CRACK1
        self.height = TILESIZE_CRACK1

        if name == "O":
            self.image = self.game.terrain_spritesheet.get_sprite(96, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Bloco_especial(pygame.sprite.Sprite):
    def __init__(self, game, x, y, name):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocoEspeciaisMoedas
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE_CRACK1
        self.y = y * TILESIZE_CRACK1
        self.width = TILESIZE_CRACK1
        self.height = TILESIZE_CRACK1

        if name == "H":
            self.image = self.game.terrain_spritesheet.get_sprite(96, 66, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def colisao(self):
        self.image = self.game.terrain_spritesheet.get_sprite(96, 66, self.width, self.height)

class Inimigo_esquilo(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites
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
        self.rect.y = self.y + 33

    def update(self):
        self.saltar()

    def saltar(self):

        if self.salto > 30:
            #personagem desce
            self.rect.y += 3
            self.descer += 1
            self.subir = False

        if self.descer > 30:
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
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE_CRACK1
        self.y = y * TILESIZE_CRACK1
        self.width = TILESIZE_CRACK1
        self.height = TILESIZE_CRACK1

        self.image = self.game.inimigo_urso.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.facing = "right"
        self.animation_loop = 1

    def update(self):
        self.animate()
        self.colisao_troncos()
        self.movement()



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

class Inimigo_coelho(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE_CRACK1
        self.y = y * TILESIZE_CRACK1
        self.width = TILESIZE_CRACK1
        self.height = TILESIZE_CRACK1

        self.image = self.game.inimigo_coelho.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.facing = "right"
        self.animation_loop = 1

    def update(self):
        self.animate()
        self.colisao_troncos()
        self.movement()



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


class Player_platform(pygame.sprite.Sprite):

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

        self.vel = 4
        self.grav = 1

        self.pulo = True

    def update(self):
        self.movement()
        self.animate()
        self.collide_enemy()
        self.collide_crack()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.collide_blocks()

        self.gravity()
        self.colisions_plataforma()
        self.colisao_brocosQuebraveis()
        self.colisao_brocoMoeda()

        self.x_change = 0
        self.y_change = 0

    def gravity(self):
        self.vel += self.grav
        self.rect[1] += self.vel

        if self.vel >= 12:
            self.vel = 12

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'

        if keys[pygame.K_d]:
            for sprite in self.game.all_sprites:
                if self.rect.x >= (WIN_WIDTH / 2):
                    sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'

    def events(self, events):
        if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_SPACE:
                self.pulo = False
                self.vel *= -1.5


    # Fuçaõ que verifica colisao com os troncos
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

    # Fuçaõ que verifica colisao com os blocos quebraveis
    def colisao_brocosQuebraveis(self):
        hits = pygame.sprite.spritecollide(self, self.game.blocoQuebraveis, False)

        if hits:

            if not self.pulo:
                # se esta a cima do bloco
                if (self.rect.y + self.rect.height) >= hits[0].rect.top:
                    #se esta a baixo do bloco
                    if (self.rect.y + self.rect.height) >= hits[0].rect.bottom:
                        #posisiona a cabeça do boneco em baixo do bloco
                        self.rect.y = hits[0].rect.bottom
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

    # Fuçaõ que verifica colisao com os blocos de moedas
    def colisao_brocoMoeda(self):
        hits = pygame.sprite.spritecollide(self, self.game.blocoEspeciaisMoedas, False)

        if hits:

            if not self.pulo:
                # se esta a cima do bloco
                if (self.rect.y + self.rect.height) >= hits[0].rect.top:
                    # se esta a baixo do bloco
                    if (self.rect.y + self.rect.height) >= hits[0].rect.bottom:
                        # posisiona a cabeça do boneco em baixo do bloco
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


    def colisions_plataforma(self):

        hits = pygame.sprite.spritecollide(self, self.game.plataforma, False)
        if hits:
            self.pulo = True
            self.rect.bottom = hits[0].rect.top

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

    # colisao com os inimigos
    def collide_enemy(self):
        pass

    # colisao com os portais
    def collide_crack(self):
        pass
