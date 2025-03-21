import pygame as py

from functions.screens.base import Base
from functions.helpers.move import move
from functions.helpers.create_button import create_buttons
from components.button import Button
from components.text import Text
from components.box import Box
from components.counter import Counter
from constants.characters import position
from constants.index import text_size


class CharacterScene(Base):
    def __init__(self, manager):
        super().__init__(manager)
        py.display.set_caption("Character Scene")

        self.mode = self.manager.data["mode"]

        self.can_change_character = (True, True)

        # UI
        # Buttons
        self.button_left = create_buttons(self, position[0:10], "left")
        self.button_right = create_buttons(self, position[10:20], "right")

        self.active_button_left = self.button_left[0]
        self.active_button_right = self.button_right[0]
        self.active_button_left.activate()
        self.active_button_right.activate()

        # Texts
        positions = [
            ((self.width - text_size[0]) / 2, (self.height / 4 - text_size[1]) / 2),
            (
                (self.width / 1.75 - text_size[0]) / 2,
                (self.height / 1.75 - text_size[1]) / 2,
            ),
            (
                (self.width / 1.75 * 2.5 - text_size[0]) / 2,
                (self.height / 1.75 - text_size[1]) / 2,
            ),
            (
                (self.width / 1.75 - text_size[0]) / 2,
                (self.height / 1.45 - text_size[1]) / 2,
            ),
            (
                (self.width / 1.75 * 2.5 - text_size[0]) / 2,
                (self.height / 1.45 - text_size[1]) / 2,
            ),
        ]
        sizes = [24, 18, 18, 15, 15]

        self.texts = [
            Text((pos, text_size), size) for pos, size in zip(positions, sizes)
        ]

        # Boxes
        self.boxes = [Box((180, 260, 330, 260)), Box((690, 260, 330, 260))]

        # Counter
        self.counter = Counter(30000)

    def start(self):
        from functions.screens.map import MapScene

        self.manager.data["characters"] = (
            self.active_button_left.boxtext[0],
            self.active_button_right.boxtext[0],
        )
        super().start(MapScene)

    def handle_events(self, events):
        super().handle_events(events)
        for e in events:
            if self.can_change_character[0]:
                self.active_button_left.handle_event(e)
            if self.mode == "h_h" and self.can_change_character[1]:
                self.active_button_right.handle_event(e)
            if e.type == py.KEYDOWN:
                if e.key in (py.K_RETURN, py.K_SPACE) and self.can_change_character == (
                    False,
                    False,
                ):
                    self.start()

    def update(self):
        super().update()
        left = self.counter.draw(self.screen.surface)
        if left == 0:
            self.start()

        # Auto lock in for AI
        if self.mode != "h_h" and self.can_change_character[1]:
            self.can_change_character = (self.can_change_character[0], False)

        labels = [
            "Pick Character",
            "Player 1" if self.mode == "h_h" else "Player",
            "Player 2" if self.mode == "h_h" else "AI",
            "Press X to lock in" if self.can_change_character[0] else "Lock In",
            (
                'Press "/" to lock in'
                if self.mode == "h_h" and self.can_change_character[1]
                else "Lock In" if self.mode == "h_h" else ""
            ),
        ]

        for text, label in zip(self.texts, labels):
            text.change_text(self.screen.surface, label)

        for item in self.texts + self.button_left + self.button_right + self.boxes:
            item.draw(self.screen.surface)

            for text, label in zip(self.texts, labels):
                text.change_text(self.screen.surface, label)

            for item in self.texts + self.button_left + self.button_right + self.boxes:
                item.draw(self.screen.surface)

    def render(self):
        super().render()

    def next_scene(self):
        return super().next_scene()
