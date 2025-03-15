import pygame as py
import psutil as ps

from constants.index import height, width, green
from functions.font import Font


class Screen:
    def __init__(self, clock: py.time.Clock = 0):
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

    # AfterBurner
    def get_AfterBurner(self):
        # Cpu
        cpu = int(ps.cpu_percent())

        # Memory
        memory = int(ps.virtual_memory().percent)

        # FPS
        fps = int(self.clock.get_fps())

        # Render text
        texts = [
            f"CPU: {cpu}%",
            f"Memory: {memory}%",
            f"FPS: {fps}",
        ]

        for i, text in enumerate(texts):
            text = self.font.render(text, green)
            self.screen.blit(text, (10, 10 + 20 * i))
