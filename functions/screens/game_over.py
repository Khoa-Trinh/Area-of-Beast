import pygame as py

from functions.screens.base import Base

from functions.helpers.move import move
from components.button import Button
from components.counter import Counter
from components.text import Text
from constants.index import button_size


class GameOverScene(Base):
    def __init__(self, manager):
        super().__init__(manager)
        py.display.set_caption("Game Over Scene")

        self.winner = self.manager.data["winner"]

        self.text = Text(
            (
                self.width / 2 - button_size[0] / 2,
                (self.height /2 - button_size[1]) / 2,
                button_size[0],
                button_size[1],
            ),
            24,
        )

        self.buttons = [
            Button(
                (
                    self.width / 2 - button_size[0] / 2,
                    (self.height - button_size[1]) / 2,
                    button_size[0],
                    button_size[1],
                ),
                "Play again",
                lambda: self.start(),
                lambda: move(self, -1),
                lambda: move(self, 1),
            ),
        ]
        self.active_button = self.buttons[0]
        for btn in self.buttons:
            btn.deactivate()
        self.active_button.activate()

        self.counter = Counter(30000)

    def start(self):
        from functions.screens.start import StartScene

        self.manager.data.clear()
        super().start(StartScene)

    def handle_events(self, events):
        super().handle_events(events)

        for e in events:
            self.active_button.handle_event(e)

    def update(self):
        super().update()

        left = self.counter.draw(self.screen.surface)
        if left == 0:
            self.start()

        label = "Player 1 wins!" if self.winner == 0 else "Player 2 wins!"
        self.text.change_text(self.screen.surface, label)

        for btn in self.buttons:
            btn.draw(self.screen.surface)

    def render(self):
        super().render()

    def next_scene(self):
        return super().next_scene()
