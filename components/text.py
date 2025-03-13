import pygame as py

from constants.index import black, white


class Text:
    def __init__(self, rect, text, size):
        self.rect = py.Rect(rect)
        self.text = text
        self.font = py.font.Font(py.font.match_font("roboto"), size)
        self.bg_color = white
        self.text_color = black

    def draw(self, screen: py.Surface):
        py.draw.rect(screen, self.bg_color, self.rect)
        text = self.font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
