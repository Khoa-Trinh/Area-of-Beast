import pygame as py

from functions.screens.base import Base
from components.ground import Ground


class GameScene(Base):
    def __init__(self, manager):
        super().__init__(manager)
        py.display.set_caption("Game Scene")

        # Manager data
        self.mode = self.manager.data.get("mode", "h_h")
        self.character = self.manager.data.get("characters", ("something", "something"))
        self.map = self.manager.data.get("map", "city")
        print(self.character)

        # Ground
        self.ground = Ground(self.map, self.width, self.height)

        # Create players

    def start(self):
        from functions.screens.pause import PauseScene

        self.manager.data['save'] = 'nothing'
        super().start(PauseScene)

    def handle_events(self, events):
        super().handle_events(events)

        for e in events:
            if e.type == py.KEYDOWN:
                if e.key == py.K_ESCAPE:
                    self.start()

    def update(self):
        super().update()

        fps = self.clock.get_fps()

        # AfterBurner
        self.screen.get_AfterBurner()

        # Update ground
        self.ground.draw(self.screen.surface, fps)

    def render(self):
        super().render()

    def next_scene(self):
        return super().next_scene()
