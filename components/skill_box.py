import pygame as py

from functions.font import Font
from constants.index import white, black, gray


class SkillBox:
    def __init__(self, position, text: tuple[str, str]):
        self.rect = py.Rect(position, (120, 30))
        self.text = text
        self.font = Font(16)

    def draw(self, screen: py.Surface, percent: float):
        rect_left = self.rect.copy()
        rect_left.width *= 0.25

        rect_right = self.rect.copy()
        rect_right.width *= 0.75
        rect_right.left += rect_left.width
        rect_right.inflate_ip(-2, -2)

        rect_cooldown = rect_right.copy()
        rect_cooldown.width *= 1 - percent

        py.draw.rect(screen, black, self.rect)
        py.draw.rect(screen, white, rect_right)
        py.draw.rect(screen, gray, rect_cooldown)

        text_1 = self.font.render(self.text[0], white)
        text_2 = self.font.render(self.text[1], black)
        text_1_rect = text_1.get_rect(center=rect_left.center)
        text_2_rect = text_2.get_rect(
            left=rect_right.left + 6, centery=rect_right.centery
        )
        screen.blit(text_1, text_1_rect)
        screen.blit(text_2, text_2_rect)
