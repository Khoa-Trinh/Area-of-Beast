import pygame as py

from functions.screen import Screen
from constants.index import white
from components.button import Button


class StartScene:
    def __init__(self, manager):
        # Initialize clock and screen
        self.clock = py.time.Clock()
        self.screen = Screen(self.clock)
        py.display.set_caption("Start Scene")

        # Manager
        self.manager = manager

        # Running
        self.running = True
        self._next_scene = self

        # Button
        self.button = Button(
            (
                self.screen.screen.get_width() / 2 - 50,
                self.screen.screen.get_height() / 2 - 25,
                100,
                50,
            ),
            "Start game",
            self.start,
        )

    def start(self):
        from functions.scenes.scenePickMode import PickModeScene

        self._next_scene = PickModeScene(self.manager)

    def handle_events(self, events):
        for e in events:
            if e.type == py.QUIT:
                self.running = False
            self.button.handle_event(e)

    def update(self):
        self.screen.fill(white)
        self.button.draw(self.screen.screen)
        self.screen.flip()

    def render(self):
        self.screen.flip()

    def next_scene(self):
        return self._next_scene
