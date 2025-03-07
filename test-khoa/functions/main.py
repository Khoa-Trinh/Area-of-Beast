import pygame as py
from constants.setting import width, height
from functions.scenes.sceneManager import SceneManager
from functions.scenes.startScene import StartScene


class Main:
    def __init__(self):
        py.init()
        self.screen = py.display.set_mode((width, height))
        self.clock = py.time.Clock()
        self.running = True
        self.scene_manager = SceneManager(self)
        self.scene_manager.set_scene(StartScene(self))

    def run(self):
        while self.running:
            for e in py.event.get():
                if e.type == py.QUIT:
                    self.running = False

            self.scene_manager.render(self.screen)

            py.display.flip()
            self.clock.tick(60)
        py.quit()
