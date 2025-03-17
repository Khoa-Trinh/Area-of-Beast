import pygame as py
import sys
import traceback as tr

from functions.screens.base import Base


class SceneManager:
    def __init__(self):
        self.active: Base = None
        self.data = {}

    def run(self):
        while self.active.running:
            events = py.event.get()

            try:
                self.active.handle_events(events)
                self.active.update()
                self.active.render()
                self.active = self.active.next_scene()

            except Exception as _:
                tr.print_exc()

        py.quit()
        sys.exit()
