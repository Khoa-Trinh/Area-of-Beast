import pygame as py


class Font:
    def __init__(self, size: int):
        self.font = py.font.Font(py.font.match_font("cascadia code"), size)

    def draw(self, text: str, color: tuple):
        return self.font.render(text, True, color)
