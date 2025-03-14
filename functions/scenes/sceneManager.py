import pygame as py
import sys

from functions.scenes.sceneBase import Scene


class SceneManager:
    def __init__(self):
        self.active: Scene = None
        self.data = {}

    def run(self):
        while self.active.running:
            events = py.event.get()

            try:
                self.active.handle_events(events)
                self.active.update()
                self.active.render()
                self.active = self.active.next_scene()

            except Exception as e:
                print(e)

        py.quit()
        sys.exit()
