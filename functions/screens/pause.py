import pygame as py

from functions.screens.base import Base
from components.button import Button
from functions.helpers.move import move
from constants.index import button_size, button_margin


class PauseScene(Base):
    def __init__(self, manager):
        super().__init__(manager)
        py.display.set_caption("Pause Scene")

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
                "Resume Game",
                lambda: self.start("resume"),
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
                lambda: self.start("quit"),
                lambda: move(self, -1),
                lambda: move(self, 1),
            ),
        ]
        self.active_button = self.buttons[0]
        for btn in self.buttons:
            btn.deactivate()
        self.active_button.activate()

    def start(self, mode):
        scenes = {
            "resume": "functions.screens.game.GameScene",
            "quit": "functions.screens.start.StartScene",
        }
        if mode in scenes:
            module_name, class_name = scenes[mode].rsplit(".", 1)
            module = __import__(module_name, fromlist=[class_name])
            scene_class = getattr(module, class_name)
            super().start(scene_class)

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
