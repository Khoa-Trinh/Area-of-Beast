import pygame as py

from constants.setting import width, height

class Image:
    def __init__(self, image: str, position: tuple[int, int]):
        self.image = py.image.load(image).convert_alpha()
        self.image = py.transform.scale(self.image, (width, height))
        self.position = position

    def draw(self, screen: py.Surface):
        screen.blit(self.image, self.position)
