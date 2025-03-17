import pygame as py

from functions.screens.base import Base
from functions.helpers.move import move
from components.button import Button
from constants.characters import text, text_character, position


class CharacterScene(Base):
    def __init__(self, manager):
        super().__init__(manager)
        py.display.set_caption("Character Scene")

        self.mode = self.manager.data["mode"]

        self.can_change_character = (True, True)

        # UI
        # Buttons
        self.button_left = self.create_buttons(position[0:10], "left")
        self.button_right = self.create_buttons(position[10:20], "right")

        self.active_button_left = self.button_left[0]
        self.active_button_right = self.button_right[0]
        self.active_button_left.activate()
        self.active_button_right.activate()

        # Texts

    def create_buttons(self, positions, side):
        return [
            Button(
                pos,
                text,
                lambda: self.lock_in(side),
                lambda: move(self, -1, side),
                lambda: move(self, 1, side),
                boxtext,
                side,
            )
            for pos, text, boxtext in zip(positions, text, text_character)
        ]

    def lock_in(self, side):
        if side == "left":
            self.can_change_character = (False, self.can_change_character[1])
        else:
            self.can_change_character = (self.can_change_character[0], False)

    def handle_events(self, events):
        super().handle_events(events)
        for e in events:
            if self.can_change_character[0]:
                self.active_button_left.handle_event(e)
            if self.mode == "h_h" and self.can_change_character[1]:
                self.active_button_right.handle_event(e)

    def update(self):
        super().update()

        for item in self.button_left + self.button_right:
            item.draw(self.screen.surface)

    def render(self):
        super().render()

    def next_scene(self):
        return super().next_scene()
