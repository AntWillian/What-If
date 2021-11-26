import os, sys

dirpath = os.getcwd()
sys.path.append(dirpath)

if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)

    ######

from fase1 import *
from fase2 import *
from fase3 import *
from fase4 import *
from fase5 import *
from fase6 import *
from fase7 import *
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

        #voltar a fase para a inicial

        if self.fase1.voltarFase or self.fase2.voltarFase or self.fase3.voltarFase or self.fase4.voltarFase or self.fase5.voltarFase or self.fase6.voltarFase or self.fase7.voltarFase:
            self.game.fases[0] = True

            self.fase1.voltarFase, self.fase2.voltarFase,self.fase3.voltarFase,self.fase4.voltarFase,self.fase5.voltarFase,self.fase6.voltarFase,self.fase7.voltarFase = False, False, False, False, False, False, False

            print("aqui")

        #restart fases
        if self.fase1.restartFase:
            self.game.fases[1] = True
            self.fase1 = Fase1()

            self.fase1.restartFase = False

        if self.fase2.restartFase:
            self.game.fases[2] = True
            self.fase2 = Fase2()
            self.fase2.restartFase = False

        if self.fase3.restartFase:
            self.game.fases[3] = True
            self.fase3 = Fase3()
            self.fase3.restartFase = False

        if self.fase4.restartFase:
            self.game.fases[4] = True
            self.fase4 = Fase4()

            self.fase4.restartFase = False

        if self.fase5.restartFase:
            self.game.fases[5] = True
            self.fase5 = Fase5()

            self.fase5.restartFase = False

        if self.fase6.restartFase:
            self.game.fases[6] = True
            self.fase6 = Fase6()

            self.fase6.restartFase = False

        if self.fase7.restartFase:
            self.game.fases[7] = True
            self.fase7 = Fase7()

            self.fase7.restartFase = False


        #entar na fase
        if self.game.fases[0]:
            self.game.draw(self.window)
            self.game.update()
        elif self.game.fases[1]:


            if self.fase1.reentradaFase:
                self.fase1 = Fase1()
                self.fase1.reentradaFase = False

            self.window.fill((31, 141, 224))
            self.fase1.draw(self.window)
            self.fase1.update()
        elif self.game.fases[2]:
            if self.game.fase2:
                self.fase2 = Fase2()
                self.game.fase2 = False
            if self.fase2.reentradaFase:
                self.fase2 = Fase2()
                self.fase2.reentradaFase = False

            self.window.fill((113, 108, 205))
            self.fase2.draw(self.window)
            self.fase2.update()
        elif self.game.fases[3]:

            if self.game.fase3:
                self.fase3 = Fase3()
                self.game.fase3 = False
            if self.fase3.reentradaFase:
                self.fase3 = Fase3()
                self.fase3.reentradaFase = False

            self.window.fill((31, 141, 224))
            self.fase3.draw(self.window)
            self.fase3.update()
        elif self.game.fases[4]:

            if self.game.fase4:
                self.fase4 = Fase4()
                self.game.fase4 = False
            if self.fase4.reentradaFase:
                self.fase4 = Fase4()
                self.fase4.reentradaFase = False

            self.window.fill((31, 141, 224))
            self.fase4.draw(self.window)
            self.fase4.update()
        elif self.game.fases[5]:

            if self.game.fase5:
                self.fase5 = Fase5()
                self.game.fase5 = False
            if self.fase5.reentradaFase:
                self.fase5 = Fase5()
                self.fase5.reentradaFase = False

            self.window.fill((113, 108, 205))
            self.fase5.draw(self.window)
            self.fase5.update()
        elif self.game.fases[6]:

            if self.game.fase6:
                self.fase6 = Fase6()
                self.game.fase6 = False
            if self.fase6.reentradaFase:
                self.fase6 = Fase6()
                self.fase6.reentradaFase = False

            self.window.fill((31, 141, 224))
            self.fase6.draw(self.window)
            self.fase6.update()
        elif self.game.fases[7]:

            if self.game.fase7:
                self.fase7 = Fase7()
                self.game.fase7 = False
            if self.fase7.reentradaFase:
                self.fase7 = Fase7()
                self.fase7.reentradaFase = False

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

    def update(self):
        while self.loop:
            self.fps.tick(FPS)
            self.draw()
            self.events()
            pygame.display.update()

Main().update()