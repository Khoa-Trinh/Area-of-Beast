import pygame as py

from constants.index import black, white


class Button:
    def __init__(self, rect, text, callback):
        self.rect = py.Rect(rect)
        self.text = text
        self.callback = callback
        self.font = py.font.Font(py.font.match_font("roboto"), 24)
        self.bg_color = black
        self.text_color = white

    def draw(self, screen: py.Surface):
        py.draw.rect(screen, self.bg_color, self.rect)
        text = self.font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == py.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()
