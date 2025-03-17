import pygame as py

from functions.helpers.font import Font
from constants.setting import width, height
from constants.colors import green


class Screen:
    def __init__(self, clock: py.time.Clock = 0):
        self.surface = py.display.set_mode((width, height))
        self.font = Font(12)
        self.clock = clock

    # Methods
    def fill(self, color: tuple):
        self.surface.fill(color)

    def blit(self, surface: py.Surface, position: tuple):
        self.surface.blit(surface, position)

    def flip(self):
        py.display.flip()

    # AfterBurner
    def get_AfterBurner(self):
        fps = int(self.clock.get_fps())

        texts = [
            f"FPS: {fps}",
        ]

        for i, text in enumerate(texts):
            text = self.font.draw(text, green)
            self.surface.blit(text, (10, 10 + i * 20))
