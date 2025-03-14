import pygame as py

from constants.index import black, white
from functions.font import Font


class Text:
    def __init__(self, rect, size):
        self.rect = py.Rect(rect)
        self.text = ''
        self.font = Font(size)
        self.bg_color = white
        self.text_color = black

    def draw(self, screen: py.Surface):
        py.draw.rect(screen, self.bg_color, self.rect)
        text = self.font.render(self.text, self.text_color)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def change_text(self, screen: py.Surface, text):
        self.text = text
        self.draw(screen)
