import pygame as py

from functions.screens.base import Base
from functions.helpers.move import move
from components.box import Box
from components.button import Button
from components.text import Text
from components.counter import Counter
from constants.index import box_size, text_size
from constants.setting import map


class MapScene(Base):
    def __init__(self, manager):
        super().__init__(manager)
        py.display.set_caption("Map Scene")

        # UI
        positions = [
            ((self.width / 2 - box_size[0]) / 2, (self.height / 1.5 - box_size[1]) / 2),
            ((self.width - box_size[0]) / 2, (self.height / 1.5 - box_size[1]) / 2),
            (
                (self.width / 2 * 3 - box_size[0]) / 2,
                (self.height / 1.5 - box_size[1]) / 2,
            ),
            (
                (self.width / 2 - box_size[0]) / 2,
                (self.height / 2.5 * 4 - box_size[1]) / 2,
            ),
            ((self.width - box_size[0]) / 2, (self.height / 2.5 * 4 - box_size[1]) / 2),
            (
                (self.width / 2 * 3 - box_size[0]) / 2,
                (self.height / 2.5 * 4 - box_size[1]) / 2,
            ),
        ]

        # Boxes
        self.boxes = [Box((pos, box_size)) for pos in positions]

        # Buttons
        self.buttons = [
            Button(
                (pos, box_size),
                "",
                lambda: self.start(),
                lambda: move(self, -1),
                lambda: move(self, 1),
                text,
            )
            for pos, text in zip(positions, map)
        ]
        self.active_button = self.buttons[0]
        for btn in self.buttons:
            btn.deactivate()
        self.active_button.activate()

        # Texts
        self.texts = [
            Text(
                (
                    (
                        (self.width - text_size[0]) / 2,
                        (self.height / 4 - text_size[1]) / 2,
                    ),
                    text_size,
                ),
                24,
            )
        ] + [
            Text(
                (
                    pos[0] + 2,
                    pos[1] + 2,
                    box_size[0] - 4,
                    box_size[1] - 4,
                ),
                24,
            )
            for pos in positions
        ]

        # Counter
        self.counter = Counter(30000)

    def start(self):
        from functions.screens.game import GameScene

        self.manager.data["map"] = self.active_button.boxtext
        super().start(GameScene)

    def handle_events(self, events):
        super().handle_events(events)

        for e in events:
            self.active_button.handle_event(e)

    def update(self):
        super().update()

        left = self.counter.draw(self.screen.surface)
        if left == 0:
            self.start()

        for item in self.buttons + self.boxes:
            item.draw(self.screen.surface)

        labels = ["Choose a map"] + map

        for label, text in zip(labels, self.texts):
            text.change_text(self.screen.surface, label)

    def render(self):
        super().render()

    def next_scene(self):
        return super().next_scene()
