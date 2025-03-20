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
   #     self.players[0].debug_attack_frame()

    def start(self):
        from functions.screens.pause import PauseScene

        self.manager.data['save'] = [
            (
                (player.x, player.y),
                player.direction,
                player.health
            )
            for player in self.players
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
        self.screen.fill((255, 255, 255))
        if self.players[0].x < self.players[1].x:
            self.players[0].direction = 1
            self.players[1].direction = -1
        else:
            self.players[0].direction = -1
            self.players[1].direction = 1
        
        self.players[0].handle_input(self.screen.surface, self.players[1])
        self.players[1].handle_input(self.screen.surface, self.players[0])
        self.players[0].update(self.screen.surface, self.players[1])
        self.players[1].update(self.screen.surface, self.players[0])
        p1_attacking = self.players[0].is_attacking and self.players[0].hitbox
        p2_attacking = self.players[1].is_attacking and self.players[1].hitbox
        if p1_attacking and p2_attacking:
            # Nếu cả hai cùng tấn công và hitbox giao nhau
            if self.players[0].hitbox.colliderect(self.players[1].hurtbox) and self.players[1].hitbox.colliderect(self.players[0].hurtbox):
                self.players[0].handle_collision(self.players[1])
                self.players[1].handle_collision(self.players[0])
            elif self.players[0].hitbox.colliderect(self.players[1].hurtbox):
                self.players[0].handle_collision(self.players[1])
            elif self.players[1].hitbox.colliderect(self.players[0].hurtbox):
                self.players[1].handle_collision(self.players[0])
        elif p1_attacking and self.players[0].hitbox.colliderect(self.players[1].hurtbox):
                self.players[0].handle_collision(self.players[1])
        elif p2_attacking and self.players[1].hitbox.colliderect(self.players[0].hurtbox):
                self.players[1].handle_collision(self.players[0])
        for player in self.players:
            player.draw(self.screen.surface)
        self.screen.get_AfterBurner()

    def render(self):
        super().render()

    def next_scene(self):
        return super().next_scene()