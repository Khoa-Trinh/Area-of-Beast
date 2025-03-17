import pygame as py

from functions.screens.base import Base
from components.button import Button
from constants.characters import text, text_character, position

class CharacterScene(Base):
    def __init__(self, manager):
        super().__init__(manager)
        py.display.set_caption("Character Scene")

        # UI
        # Buttons
        self.button_left = self.create_buttons(position[0:10], "left")
        self.button_right = self.create_buttons(position[10:20], "right")

        self.active_button_left = self.button_left[0]
        self.active_button_right = self.button_right[0]
        self.active_button_left.activate()
        self.active_button_right.activate()

    def create_buttons(self, positions, side):
        return [
            Button(
                pos,
                text,
                lambda s=side: self.lock_in(s),
                lambda s=side: self.move(-1, s),
                lambda s=side: self.move(1, s),
                boxtext,
                side,
            )
            for pos, text, boxtext in zip(positions, text, text_character)
        ]

    def handle_events(self, events):
        super().handle_events(events)

    def update(self):
        super().update()

        for item in self.button_left + self.button_right:
            item.draw(self.screen.surface)

    def render(self):
        super().render()

    def next_scene(self):
        return super().next_scene()
