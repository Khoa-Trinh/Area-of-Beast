import pygame as py
from constants.setting import white, black, width, height


class StartScene:
    def __init__(self, game):
        self.game = game
        self.font = py.font.SysFont("Cascadia Code", 30)

    def process_events(self):
        pass

    def update(self):
        pass

    def render(self, screen):
        screen.fill(white)
        text = self.font.render("Start Scene", True, black)
        screen.blit(
            text,
            (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2),
        )
