import pygame as py

from functions.screens.base import Base
from functions.helpers.move import move
from components.button import Button
from constants.index import button_size, button_margin


class ModeScene(Base):
    def __init__(self, manager):
        super().__init__(manager)
        py.display.set_caption("Mode Scene")

        # UI
        # Buttons
        self.buttons = [
            Button(
                (
                    button_margin[1],
                    (self.height - button_size[1]) / 2,
                    button_size[0],
                    button_size[1],
                ),
                "Human vs Human",
                lambda: self.start("h_h"),
                lambda: move(self, -1),
                lambda: move(self, 1),
            ),
            Button(
                (
                    self.width - button_size[0] - button_margin[1],
                    (self.height - button_size[1]) / 2,
                    button_size[0],
                    button_size[1],
                ),
                "Human vs AI",
                lambda: self.start("h_ai"),
                lambda: move(self, -1),
                lambda: move(self, 1),
            ),
        ]
        self.active_button = self.buttons[0]
        for btn in self.buttons:
            btn.deactivate()
        self.active_button.activate()

    def start(self, mode):
        from functions.screens.character import CharacterScene

        self.manager.data["mode"] = mode
        super().start(CharacterScene)

    def handle_events(self, events):
        super().handle_events(events)

        for e in events:
            self.active_button.handle_event(e)

    def update(self):
        super().update()

        for btn in self.buttons:
            btn.draw(self.screen.surface)

    def render(self):
        super().render()

    def next_scene(self):
        return super().next_scene()
