import pygame as py


class Image:
    def __init__(self, image: str, position: tuple[int, int]):
        self.image = py.image.load(image).convert_alpha()
        self.position = position

    def draw(self, screen: py.Surface):
        screen.blit(self.image, self.position)
