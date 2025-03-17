import pygame as py

from functions.helpers.character_to_int import match_character
from functions.helpers.image_blit import Image


class Player:
    def __init__(
        self,
        position: tuple[int, int],
        size: tuple[int, int],
        clock: py.time.Clock,
        move_key: str,
        character: str,
    ):
        # Position
        self.x, self.y = position
        self.width, self.height = size
        self.clock = clock
        self.move_key = move_key

        # Character
        self.character = match_character(character)
        self.image = Image("../../assets/images/character1/idle.png", (self.x, self.y))

        # Movement
        self.can_move = True
        self.can_use_skill = True
        self.cooldown_percent = [1, 1]

    def draw(self, screen: py.Surface):
        self.image.draw(screen)

    def action(self):
        pass
