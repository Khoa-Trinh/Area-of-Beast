import pygame as py

from functions.scenes.sceneStart import StartScene
from functions.scenes.sceneManager import SceneManager


class Main:
    def __init__(self):
        py.init()
        self.manager = SceneManager()
        scene = StartScene(self.manager)
        self.manager.active = scene

    def run(self):
        self.manager.run()
