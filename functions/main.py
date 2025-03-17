import pygame as py

from functions.screens.start import StartScene
from functions.screens.manager import SceneManager


class Main:
    def __init__(self):
        py.init()
        self.manager = SceneManager()
        scene = StartScene(self.manager)
        self.manager.active = scene
        self.manager.run()
