import pygame as py

from functions.scenes.sceneStart import StartScene
from functions.scenes.sceneManager import SceneManager


class Main:
    def __init__(self):
        py.init()
        scene = StartScene()
        self.manager = SceneManager(scene)

    def run(self):
        self.manager.run()
