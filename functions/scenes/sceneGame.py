import pygame as py

from functions.scenes.sceneBase import Scene
from functions.screen import Screen
from functions.player import Player
from constants.index import white, plr_y, plr_width, plr_height, plr_color


class GameScene(Scene):
    def __init__(self, manager):
        # Initialize clock and screen
        self.clock = py.time.Clock()
        self.screen = Screen(self.clock)
        py.display.set_caption("Game Scene")

        # Running
        self.running = True
        self._next_scene = self

        # Manager
        self.manager = manager

        # Screen
        self.screen.fill(white)

        # Create Players
        self.player_1 = Player(
            (100, plr_y), (plr_width, plr_height), plr_color, self.clock, "wasd"
        )
        self.player_2 = Player(
            (700, plr_y), (plr_width, plr_height), plr_color, self.clock, "arrow"
        )

        # Draw
        self.screen.flip()

    def handle_events(self, events):
        for e in events:
            if e.type == py.QUIT:
                self.running = False

    def update(self):
        dt = self.clock.tick(120) / 1000

        # Update screen
        self.screen.fill(white)
        self.screen.get_FPS()

        # Update players
        self.player_1.action(self.screen.screen, dt)
        self.player_2.action(self.screen.screen, dt)

    def render(self):
        self.screen.flip()

    def next_scene(self):
        return self._next_scene
