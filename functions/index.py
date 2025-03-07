import pygame as py
import sys

from functions.player import Player
from functions.screen import Screen
from constants.index import caption, white


class Main:
    def __init__(self):
        py.init()

        # Self setting
        self.clock = py.time.Clock()
        self.screen = Screen(self.clock)
        self.caption = py.display.set_caption(caption)

        # Running
        self.running = True

        # Screen
        self.screen.fill(white)

        # Player
        self.player = Player(self.clock)
        self.player.draw(self.screen.screen)
        self.screen.flip()

    def run(self):
        while self.running:
            self.dt = self.clock.tick(60) / 1000

            for e in py.event.get():
                if e.type == py.QUIT:
                    self.running = False

            self.screen.fill(white)
            self.player.action(self.screen.screen, self.dt)

            self.screen.get_FPS()

            self.screen.flip()

        py.quit()
        sys.exit()
