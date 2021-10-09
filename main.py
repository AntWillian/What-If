import pygame
from game import Game
from config import *

class Main:

    def __init__(self):

        self.window = pygame.display.set_mode([WIN_WIDTH, WIN_HEIGHT])
        self.title = pygame.display.set_caption("What If?")

        self.loop = True
        self.fps = pygame.time.Clock()

        self.game = Game()

    def draw(self):
        self.game.draw(self.window)
        self.game.update()

    def events(self):
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                self.loop = False
            #self.game.player.events(events)

    def update(self):
        while self.loop:
            self.fps.tick(FPS)
            self.draw()
            self.events()
            pygame.display.update()

Main().update()