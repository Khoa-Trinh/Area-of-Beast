import pygame as py

from functions.screens.screen import Screen
from constants.colors import white

class Base:
    def __init__(self, manager):
        # Initialize screen and clock
        self.clock = py.time.Clock()
        self.screen = Screen(self.clock)
        self.width = self.screen.surface.get_width()
        self.height = self.screen.surface.get_height()

        # Running
        self.running = True
        self._next_scene = self

        # Manager
        self.manager = manager

    def start(self, scene):
        self._next_scene = scene(self.manager)

    def handle_events(self, events):
        for e in events:
            if e.type == py.QUIT:
                self.running = False

        keys = py.key.get_pressed()
        if keys[py.K_TAB] and keys[py.K_ESCAPE]:
            self.running = False

    def update(self):
        self.clock.tick(60)
        self.screen.fill(white)

    def render(self):
        self.screen.flip()

    def next_scene(self):
        return self._next_scene