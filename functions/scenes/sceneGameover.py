import pygame as py

from functions.scenes.sceneBase import Scene
from functions.screen import Screen
from components.counter import Counter
from components.button import Button
from constants.index import white


class GameOverScene(Scene):
    def __init__(self, manager):
        # Initialize screen
        self.screen = Screen()
        py.display.set_caption("Game Over Scene")

        # Running
        self.running = True
        self._next_scene = self

        # Manager
        self.manager = manager

        self.counter = Counter(10000)

        self.buttons = [
            Button(
                (150, self.screen.screen.get_height() / 2 - 25, 150, 50),
                "Play Again",
                lambda: self.play_again(),
                lambda: self.move(-1),
                lambda: self.move(1),
            ),
            Button(
                (550, self.screen.screen.get_height() / 2 - 25, 150, 50),
                "Quit",
                lambda: self.quit(),
                lambda: self.move(-1),
                lambda: self.move(1),
            ),
        ]
        self.activate_button = self.buttons[0]
        for btn in self.buttons:
            btn.deactivate()
        self.activate_button.activate()

    def play_again(self):
        from functions.scenes.scenePickMode import PickModeScene

        self._next_scene = PickModeScene(self.manager)

    def quit(self):
        from functions.scenes.sceneStart import StartScene

        self._next_scene = StartScene(self.manager)

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
        left = self.counter.draw(self.screen.screen)
        if left == 0:
            self.quit()
        for button in self.buttons:
            button.draw(self.screen.screen)

    def render(self):
        self.screen.flip()

    def next_scene(self):
        return self._next_scene
