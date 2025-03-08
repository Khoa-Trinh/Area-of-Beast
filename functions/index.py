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

        # Player 1
        self.player_1 = Player(self.clock, 'wasd')
        self.player_1.draw(self.screen.screen)

        # Player 2
        self.player_2 = Player(self.clock, 'arrow')
        self.player_2.draw(self.screen.screen)

        self.screen.flip()

    def run(self):
        while self.running:
            self.dt = self.clock.tick(60) / 1000

            for e in py.event.get():
                if e.type == py.QUIT:
                    self.running = False

            self.screen.fill(white)
            self.screen.get_FPS()

            self.player_1.action(self.screen.screen, self.dt)
            self.player_2.action(self.screen.screen, self.dt)

            self.screen.flip()

        py.quit()
        sys.exit()
