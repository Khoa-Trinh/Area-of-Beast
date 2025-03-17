import pygame as py

from functions.screens.base import Base
from functions.helpers.move import move
from components.button import Button


class ModeScene(Base):
    def __init__(self, manager):
        super().__init__(manager)
        py.display.set_caption("Mode Scene")

        # UI
        # Buttons
        button = (150, 50)
        self.buttons = [
            Button(
                (button[0], (self.height - button[1]) / 2, button[0], button[1]),
                "Human vs Human",
                lambda: self.pick_mode("h_h"),
                lambda: move(self, -1),
                lambda: move(self, 1),
            ),
            Button(
                (
                    self.width - button[0] * 2,
                    (self.height - button[1]) / 2,
                    button[0],
                    button[1],
                ),
                "Human vs AI",
                lambda: self.pick_mode("h_ai"),
                lambda: move(self, -1),
                lambda: move(self, 1),
            ),
        ]
        self.active_button = self.buttons[0]
        for btn in self.buttons:
            btn.deactivate()
        self.active_button.activate()

    def pick_mode(self, mode):
        from functions.screens.character import CharacterScene

        self.manager.data["mode"] = mode
        self._next_scene = CharacterScene(self.manager)

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
