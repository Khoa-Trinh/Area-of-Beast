import pygame as py

from functions.scenes.sceneBase import Scene
from functions.screen import Screen
from constants.index import white
from components.button import Button


class PickModeScene(Scene):
    def __init__(self, manager):
        # Initialize clock and screen
        self.screen = Screen()
        py.display.set_caption("Pick Mode Scene")

        # Manager
        self.manager = manager

        # Running
        self.running = True
        self._next_scene = self

        # Buttons
        self.buttons = [
            Button(
                (150, self.screen.screen.get_height() / 2 - 25, 150, 50),
                "Human vs Human",
                lambda: self.pick_mode("h_h"),
                lambda: self.move(-1),
                lambda: self.move(1),
            ),
            Button(
                (550, self.screen.screen.get_height() / 2 - 25, 150, 50),
                "Human vs AI",
                lambda: self.pick_mode("h_ai"),
                lambda: self.move(-1),
                lambda: self.move(1),
            ),
        ]
        self.activate_button = self.buttons[0]
        for btn in self.buttons:
            btn.deactivate()
        self.activate_button.activate()

    def pick_mode(self, mode):
        from functions.scenes.scenePickCharacter import PickCharacterScene

        self.manager.data["mode"] = mode
        self._next_scene = PickCharacterScene(self.manager)

    def move(self, direction):
        current_i = self.buttons.index(self.activate_button)
        for btn in self.buttons:
            btn.deactivate()
        new_index = (current_i + direction) % len(self.buttons)
        self.activate_button = self.buttons[new_index]
        self.activate_button.activate()

    def handle_events(self, events):
        for e in events:
            if e.type == py.QUIT:
                self.running = False
            self.activate_button.handle_event(e)

    def update(self):
        self.screen.fill(white)
        for button in self.buttons:
            button.draw(self.screen.screen)

    def render(self):
        self.screen.flip()

    def next_scene(self):
        return self._next_scene
