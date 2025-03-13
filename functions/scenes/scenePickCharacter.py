import pygame as py

from functions.scenes.sceneBase import Scene
from functions.screen import Screen
from functions.scenes.sceneGame import GameScene
from constants.index import white
from components.text import Text


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

        # # Text
        self.text_title = Text(
            (
                self.screen.screen.get_width() / 2 - 50,
                self.screen.screen.get_height() / 8 - 25,
                100,
                50,
            ),
            "Pick Character",
            36,
        )
        self.text_plr_1 = Text(
            (
                self.screen.screen.get_width() / 4 - 50,
                self.screen.screen.get_height() / 4 - 25,
                100,
                50,
            ),
            "Player 1" if self.mode == 'h_h' else 'Player',
            24,
        )
        self.text_plr_2 = Text(
            (
                self.screen.screen.get_width() / 4 * 3 - 50,
                self.screen.screen.get_height() / 4 - 25,
                100,
                50,
            ),
            "Player 2" if self.mode == 'h_h' else 'AI',
            24,
        )

        # Screen
        self.screen.fill(white)

        # Draw
        self.screen.flip()

    def start(self):
        self._next_scene = GameScene(self.manager)

    def handle_events(self, events):
        for e in events:
            if e.type == py.QUIT:
                self.running = False

    def update(self):
        self.screen.fill(white)
        
        self.text_title.draw(self.screen.screen)
        self.text_plr_1.draw(self.screen.screen)
        self.text_plr_2.draw(self.screen.screen)

    def render(self):
        self.screen.flip()

    def next_scene(self):
        return self._next_scene
