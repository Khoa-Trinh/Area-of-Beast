import pygame as py

from functions.font import Font
from constants.index import green, red, white, black


class Health:
    def __init__(self, position):
        self.rect = py.Rect(position, (260, 30))
        self.health = 100
        self.color = None
        self.font = Font(16)

    def draw(self, screen: py.Surface, health: int):
        rect_background = self.rect.inflate(-2, -2)
        rect_health = rect_background.copy()
        rect_health.width = rect_background.width * health / 100

        self.color = green if health > 30 else red

        py.draw.rect(screen, black, self.rect)
        py.draw.rect(screen, white, rect_background)
        py.draw.rect(screen, self.color, rect_health)

        text = self.font.render(f"{health}%", black)
        text_rect = text.get_rect(right=self.rect.right - 6, centery=self.rect.centery)
        screen.blit(text, text_rect)
