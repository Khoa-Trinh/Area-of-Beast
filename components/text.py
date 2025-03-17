import pygame as py

from functions.helpers.font import Font
from constants.colors import white, black


class Text:
    def __init__(self, rect, size):
        self.rect = py.Rect(rect)
        self.text = ""
        self.font = Font(size)
        self.bg = white
        self.text = black

    def draw(self, screen: py.Surface):
        py.draw.rect(screen, self.bg_color, self.rect)
        text = self.font.render(self.text, self.text_color)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def change_text(self, screen: py.Surface, text):
        self.text = text
        self.draw(screen)
