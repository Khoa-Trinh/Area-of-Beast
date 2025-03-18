import pygame as py

from functions.screens.base import Base
from components.ground import Ground
from functions.players.main import Player

class GameScene(Base):
    def __init__(self, manager):
        super().__init__(manager)
        py.display.set_caption("Game Scene")
        
        # Manager data
        self.mode = self.manager.data.get("mode", "h_h")
        #self.character = self.manager.data.get("characters", ("something", "something"))
        self.character = [0,0]
        self.map = self.manager.data.get("map", "city")
        print(self.character)
        self.default_pos=[(50,50),(300,300)]
        # Ground
        self.ground = Ground(self.map, self.width, self.height)
        self.save_data = self.manager.data.get("save", None)
        # Create players
        self.players = [
            Player(
                (
                    self.save_data[i][0]
                    if self.save_data is not None
                    else self.default_pos[i]
                ),
                (
                    self.save_data[i][1]
                    if self.save_data is not None
                    else 1 if i==0 else -1
                ),
                self.clock,
                i,
                char,
                (
                    self.save_data[i][3]
                    if self.save_data is not None
                    else 100
                )
            )
            for i, char in enumerate(self.character)
        ]

    def start(self):
        from functions.screens.pause import PauseScene

        self.manager.data['save'] = [
            (
                (player.x, player.y),
                player.direction,
                player.health
            )
            for player in self.player
        ]
        super().start(PauseScene)

    def handle_events(self, events):
        super().handle_events(events)

        for e in events:
            if e.type == py.KEYDOWN:
                if e.key == py.K_ESCAPE:
                    self.start()

    def update(self):
        super().update()
        self.clock.tick(60)
        fps = self.clock.get_fps()
        self.screen.fill((255,255,255))
        for player in self.players:
            player.handle_input(self.screen.surface)
            player.update(self.screen.surface)
            player.draw(self.screen.surface)
        # AfterBurner
        self.screen.get_AfterBurner()

        # Update ground
        

    def render(self):
        super().render()

    def next_scene(self):
        return super().next_scene()
