import pygame as py
import sys

from functions.player import Player
from constants.index import height, width, caption, white


class Main:
    def __init__(self):
        py.init()

        # Self variables
        self.screen = py.display.set_mode((height, width))
        self.caption = py.display.set_caption(caption)
        self.running = True

        # Screen
        self.screen.fill(white)

        # Player
        self.player = Player()
        self.player.draw(self.screen)
        py.display.flip()

    def run(self):
        while self.running:
            for e in py.event.get():
                if e.type == py.QUIT:
                    self.running = False

            self.screen.fill(white)
            self.player.move(self.screen)
            py.display.flip()

        py.quit()
        sys.exit()
