import pygame as py

from functions.helpers.map_to_int import match_map
from constants.colors import black


class Ground:
    def __init__(self, map: str, width: int, height: int):
        self.map = match_map(map)
        self.width = width
        self.height = height
        self.direction = 1
        self.ground = 500

        if self.map == 0:
            self.ground = 400

    def draw(self, screen: py.Surface, fps: float):
        fps = max(1, fps)
        if self.map == 0:
            self.ground += self.direction * 100 / fps

            if self.ground >= 500:
                self.ground = 500
                self.direction = -1
            elif self.ground <= 400:
                self.ground = 400
                self.direction = 1
        py.draw.rect(
            screen, black, (0, self.ground, self.width, self.height - self.ground + 1)
        )
