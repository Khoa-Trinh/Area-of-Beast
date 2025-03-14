import pygame as py

from functions.scenes.sceneBase import Scene
from functions.screen import Screen
from functions.scenes.sceneGame import GameScene
from constants.index import white, position, text, text_character
from components.text import Text
from components.button import Button
from components.box import Box
from components.counter import Counter


class PickCharacterScene(Scene):
    def __init__(self, manager):
        self.clock = py.time.Clock()
        self.screen = Screen(self.clock)
        py.display.set_caption("Pick Character Scene")

        # Manager
        self.manager = manager
        self.mode = self.manager.data["mode"]

        # Running
        self.running = True
        self._next_scene = self

        self.can_change_character = (True, True)

        # # Text
        screen_width = self.screen.screen.get_width()
        screen_height = self.screen.screen.get_height()

        self.text = [
            Text((screen_width / 2 - 50, screen_height / 8 - 25, 100, 50), 18),
            Text((screen_width / 4 - 50, screen_height / 4 - 25, 100, 50), 12),
            Text((screen_width / 4 * 3 - 50, screen_height / 4 - 25, 100, 50), 12),
            Text((100 + ((195 - 100) / 2), 540, 100, 50), 12),
            Text((505 + ((195 - 100) / 2), 540, 100, 50), 12),
            Text((screen_width / 2 - 50, screen_height / 4 - 25, 100, 50), 18),
        ]

        self.button_left = [
            Button(
                pos,
                text,
                lambda: self.lock_in("left"),
                lambda: self.move(-1, "left"),
                lambda: self.move(1, "left"),
                boxtext,
                "left",
            )
            for pos, text, boxtext in zip(position[0:10], text, text_character)
        ]
        self.button_right = [
            Button(
                pos,
                text,
                lambda: self.lock_in("right"),
                lambda: self.move(-1, "right"),
                lambda: self.move(1, "right"),
                boxtext,
                "right",
            )
            for pos, text, boxtext in zip(position[10:20], text, text_character)
        ]
        self.active_button_left = self.button_left[0]
        self.active_button_right = self.button_right[0]

        self.showcase = [
            Box((30, 365, 335, 175), "", "left"),
            Box((435, 365, 335, 175), "", "right"),
        ]

        self.counter = Counter(30000)

    def lock_in(self, pos):
        if pos == "left":
            self.can_change_character = (False, self.can_change_character[1])
        else:
            self.can_change_character = (self.can_change_character[0], False)

    def start(self):
        self.manager.data["player1"] = self.active_button_left.boxtext[0]
        self.manager.data["player2"] = self.active_button_right.boxtext[0]
        print(self.manager.data)
        self._next_scene = GameScene(self.manager)

    def move(self, direction, pos):
        buttons = self.button_left if pos == "left" else self.button_right
        active_button = (
            self.active_button_left if pos == "left" else self.active_button_right
        )
        new_index = (buttons.index(active_button) + direction) % len(buttons)

        if pos == "left":
            if self.can_change_character[0]:
                self.active_button_left = buttons[new_index]
        else:
            if self.can_change_character[1]:
                self.active_button_right = buttons[new_index]

    def handle_events(self, events):
        for e in events:
            if e.type == py.QUIT:
                self.running = False
            if self.can_change_character[0]:
                self.active_button_left.handle_event(e)
            if self.mode == "h_h" and self.can_change_character[1]:
                self.active_button_right.handle_event(e)
            if e.type == py.KEYDOWN:
                if e.key == py.K_RETURN and self.can_change_character == (False, False):
                    self.start()

    def update(self):
        self.screen.fill(white)

        left = self.counter.update(self.screen.screen)
        if left == 0:
            self.start()

        labels = [
            "Pick Character",
            "Player 1" if self.mode == "h_h" else "Player",
            "Player 2" if self.mode == "h_h" else "AI",
            'Press "X" to lock in' if self.can_change_character[0] else "Lock In",
            (
                'Press "/" to lock in'
                if self.mode == "h_h" and self.can_change_character[1]
                else "Lock In" if self.mode == "h_h" else ""
            ),
            (
                "Press Enter to start"
                if self.can_change_character == (False, False)
                else ""
            ),
        ]

        for text_obj, label in zip(self.text, labels):
            text_obj.change_text(self.screen.screen, label)

        for item in self.text + self.button_left + self.button_right:
            item.draw(self.screen.screen)

        for box, button in zip(
            self.showcase, [self.active_button_left, self.active_button_right]
        ):
            box.change_text(self.screen.screen, button.boxtext)

    def render(self):
        self.screen.flip()

    def next_scene(self):
        return self._next_scene
