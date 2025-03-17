import pygame as py

from functions.screens.base import Base
from functions.screens.screen import Screen
from functions.helpers.move import move
from components.button import Button
from components.text import Text
from constants.button import button_size, button_margin


class StartScene(Base):
    def __init__(self, manager):
        super().__init__(manager)
        py.display.set_caption("Start Scene")

        # UI
        # Buttons
        self.buttons = [
            Button(
                (
                    button_margin[0],
                    (self.height - button_size[1]) / 2,
                    button_size[0],
                    button_size[1],
                ),
                "Start Game",
                lambda: self.start(),
                lambda: move(self, -1),
                lambda: move(self, 1),
            ),
            Button(
                (
                    (self.width - button_size[0]) / 2,
                    (self.height - button_size[1]) / 2,
                    button_size[0],
                    button_size[1],
                ),
                "Settings",
                lambda: self.setting(),
                lambda: move(self, -1),
                lambda: move(self, 1),
            ),
            Button(
                (
                    self.width - button_size[0] - button_margin[0],
                    (self.height - button_size[1]) / 2,
                    button_size[0],
                    button_size[1],
                ),
                "Quit Game",
                lambda: self.quit(),
                lambda: move(self, -1),
                lambda: move(self, 1),
            ),
        ]
        self.active_button = self.buttons[0]
        for btn in self.buttons:
            btn.deactivate()
        self.active_button.activate()

    def start(self):
        from functions.screens.mode import ModeScene

        self._next_scene = ModeScene(self.manager)

    def setting(self):
        pass

    def quit(self):
        self.running = False

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
