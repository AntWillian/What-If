from fase1 import *
from fase2 import *
from fase3 import *
from fase4 import *
from fase5 import *
from fase6 import *
from fase7 import *
from fase1 import *
from game import Game
from config import *


class Main:

    def __init__(self):

        self.window = pygame.display.set_mode([WIN_WIDTH, WIN_HEIGHT])
        self.title = pygame.display.set_caption("What If?")

        self.loop = True
        self.fps = pygame.time.Clock()

        self.game = Game()
        self.fase1 = Fase1()
        self.fase2 = Fase2()
        self.fase3 = Fase3()
        self.fase4 = Fase4()
        self.fase5 = Fase5()
        self.fase6 = Fase6()
        self.fase7 = Fase7()

    def draw(self):
        if self.game.fases[0]:
            self.game.draw(self.window)
            self.game.update()
        elif self.game.fases[1]:
            self.window.fill((31, 141, 224))
            self.fase1.draw(self.window)
            self.fase1.update()
        elif self.game.fases[2]:
            self.window.fill((113, 108, 205))
            self.fase2.draw(self.window)
            self.fase2.update()
        elif self.game.fases[3]:
            self.window.fill((31, 141, 224))
            self.fase3.draw(self.window)
            self.fase3.update()
        elif self.game.fases[4]:
            self.window.fill((31, 141, 224))
            self.fase4.draw(self.window)
            self.fase4.update()
        elif self.game.fases[5]:
            self.window.fill((31, 141, 224))
            self.fase5.draw(self.window)
            self.fase5.update()
        elif self.game.fases[6]:
            self.window.fill((31, 141, 224))
            self.fase6.draw(self.window)
            self.fase6.update()
        elif self.game.fases[7]:
            self.window.fill((31, 141, 224))
            self.fase7.draw(self.window)
            self.fase7.update()

    def events(self):
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                self.loop = False
            self.fase1.events(events)
            self.fase2.events(events)
            self.fase3.events(events)
            self.fase4.events(events)
            self.fase5.events(events)
            self.fase6.events(events)
            self.fase7.events(events)
            self.game.eventsDialogo(events)

    def update(self):
        while self.loop:
            self.fps.tick(FPS)
            self.draw()
            self.events()
            pygame.display.update()

Main().update()