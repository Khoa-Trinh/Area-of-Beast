import pygame as py

from constants.index import height, width, green
from functions.font import Font


class Screen:
    def __init__(self, clock: py.time.Clock):
        self.screen = py.display.set_mode((width, height))
        self.font = Font(12)
        self.clock = clock

    # Methods
    def fill(self, color):
        self.screen.fill(color)

    def blit(self, image, position):
        self.screen.blit(image, position)

    def flip(self):
        py.display.flip()

    # FPS
    def get_FPS(self):
        fps = str(int(self.clock.get_fps()))
        fps_text = self.font.render(f"FPS: {fps}", green)
        self.screen.blit(fps_text, (10, 10))
