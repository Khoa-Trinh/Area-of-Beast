import pygame as py

from constants.index import black, white
from functions.font import Font
from functions.helper import capitalize


class Box:
    def __init__(self, rect, text: tuple[str, str, str, str], plr_pos, image=None):
        # Define button properties
        self.rect = py.Rect(rect)
        self.image = image
        self.text = text
        self.pos = plr_pos
        self.font = Font(12)
        self.border_color = black
        self.bg_color = white
        self.text_color = black

    def draw(self, screen: py.Surface):
        py.draw.rect(screen, self.border_color, self.rect)
        py.draw.rect(screen, self.bg_color, self.rect.inflate(-4, -4))

        texts = [
            self.font.render(text, self.text_color)
            for text in [
                capitalize(self.text[0]),
                self.text[1],
                f"Skill 1({'C' if self.pos == 'left' else '<'}): {self.text[2]}",
                f"Skill 2({'V' if self.pos == 'left' else '>'}): {self.text[3]}",
            ]
        ]
        rects = [
            texts[0].get_rect(
                topleft=(self.rect.topleft[0] + 10, self.rect.topleft[1] + 10)
            ),
            texts[1].get_rect(
                topleft=(self.rect.topleft[0] + 10, self.rect.topleft[1] + 40)
            ),
            texts[2].get_rect(
                topleft=(self.rect.topleft[0] + 10, self.rect.topleft[1] + 70)
            ),
            texts[3].get_rect(
                topleft=(self.rect.topleft[0] + 10, self.rect.topleft[1] + 100)
            ),
        ]

        for text, rect in zip(texts, rects):
            screen.blit(text, rect)

    def change_text(
        self, screen: py.Surface, text: tuple[str, str, str, str], image=None
    ):
        self.text = text
        self.draw(screen)
