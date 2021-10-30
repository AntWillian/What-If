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
        self.crack = Crack1()

    def draw(self):
        if not self.game.change_scene:
            self.game.draw(self.window)
            self.game.update()
        elif not self.crack.change_scene:
            self.window.fill((0, 0, 0))
            self.crack.draw(self.window)
            self.crack.update()

    def events(self):
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                self.loop = False
            self.crack.events(events)

    def update(self):
        while self.loop:
            self.fps.tick(FPS)
            self.draw()
            self.events()
            pygame.display.update()

Main().update()