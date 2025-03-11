import pygame as py
import sys

from functions.scenes.sceneBase import Scene


class SceneManager:
    def __init__(self, init: Scene):
        self.active = init

    def run(self):
        while self.active.running:
            events = py.event.get()

            self.active.handle_events(events)
            self.active.update()
            self.active.render()
            self.active = self.active.next_scene()

        py.quit()
        sys.exit()
