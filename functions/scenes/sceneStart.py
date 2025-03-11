import pygame as py

from functions.screen import Screen
from constants.index import white, width, height
from components.button import Button


class StartScene:
    def __init__(self):
        # Initialize clock and screen
        self.clock = py.time.Clock()
        self.screen = Screen(self.clock)
        py.display.set_caption("Start Scene")

        # Running
        self.running = True
        self._next_scene = self

        # Button
        self.button = Button((height / 2 - 50, width / 2 - 50, 100, 50), "Start game", self.start)

        # Screen
        self.screen.fill(white)

        # Draw
        self.button.draw(self.screen.screen)
        self.screen.flip()

    def start(self):
        from functions.scenes.sceneGame import GameScene

        self._next_scene = GameScene()

    def handle_events(self, events):
        for e in events:
            if e.type == py.QUIT:
                self.running = False
            self.button.handle_event(e)

    def update(self):
        # Update screen
        pass

    def render(self):
        self.screen.flip()

    def next_scene(self):
        return self._next_scene
