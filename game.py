from obj import Obj
import pygame


class Game:

    def __init__(self):
        self.all_sprites = pygame.sprite.Group()

        self.bg = Obj("assets/fundo.png", 0, 0, self.all_sprites)

    def draw(self, window):
        self.all_sprites.draw(window)

    def update(self):
        self.all_sprites.update()