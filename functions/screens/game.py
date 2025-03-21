import pygame as py

from functions.screens.base import Base
from components.ground import Ground
from functions.players.main import Player
from functions.players.ai_controller import AIController
from components.health import Health
P_WIDTH = 27.5
P_HEIGHT = 43.5
class GameScene(Base):
    def __init__(self, manager):
        super().__init__(manager)
        py.display.set_caption("Game Scene")

        # Manager data
        self.mode = self.manager.data.get("mode", "h_h")
        #self.character = self.manager.data.get("characters", ("something", "something"))
        self.character = [0,0]
        self.map = self.manager.data.get("map", "city")
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
                    self.save_data[i][2]
                    if self.save_data is not None
                    else 100
                )
            )
            for i, char in enumerate(self.character)
        ]
   #     self.players[0].debug_attack_frame()
        if self.mode == "h_ai":
            self.ai_controller = AIController(self.players[1], self.players[0])
        else:
            self.ai_controller = None

        self.health_bar = [
          Health((10, 30)),
          Health((self.width - 270, 30))
        ]

    def start(self, scene):
        if scene == 'pause':
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
        elif scene == 'game_over':
          from functions.screens.game_over import GameOverScene

          self.manager.data['winner'] = 0 if self.players[0].health > 0 else 1
          super().start(GameOverScene)

    def handle_events(self, events):
        super().handle_events(events)

        for e in events:
            if e.type == py.KEYDOWN:
                if e.key == py.K_ESCAPE:
                    self.start('pause')

    def update(self):
        super().update()
        for player in self.players:
            if player.health <= 0:
                self.start('game_over')
        if self.players[0].x < self.players[1].x:
            self.players[0].direction = 1
            self.players[1].direction = -1
        else:
            self.players[0].direction = -1
            self.players[1].direction = 1

        self.players[0].handle_input(self.screen.surface, self.players[1])

    # Player 2 là AI nếu chế độ "h_ai", ngược lại dùng input người chơi
        if self.mode == "h_ai" and self.ai_controller:
            self.ai_controller.update(self.screen.surface)
        else:
            self.players[1].handle_input(self.screen.surface, self.players[0])

        self.players[0]._update_hurtbox()
        self.players[1]._update_hurtbox()

        # Collision check with predicted movement
        p0_next_x = self.players[0].x + self.players[0].v_x
        p1_next_x = self.players[1].x + self.players[1].v_x
        p0_next_hurtbox = py.Rect(
            p0_next_x, self.players[0].hurtbox.y,
            self.players[0].hurtbox.width, self.players[0].hurtbox.height
        )
        p1_next_hurtbox = py.Rect(
            p1_next_x, self.players[1].hurtbox.y,
            self.players[1].hurtbox.width, self.players[1].hurtbox.height
        )

        if (p0_next_hurtbox.colliderect(p1_next_hurtbox) and
            self.players[0].on_ground and self.players[1].on_ground):
            if self.players[0].v_x > 0 and self.players[0].x < self.players[1].x:
                self.players[0].v_x = 0
            if self.players[0].v_x < 0 and self.players[0].x > self.players[1].x:
                self.players[0].v_x = 0
            if self.players[1].v_x > 0 and self.players[1].x < self.players[0].x:
                self.players[1].v_x = 0
            if self.players[1].v_x < 0 and self.players[1].x > self.players[0].x:
                self.players[1].v_x = 0


        width_limit = (0, self.screen.surface.get_width() - P_WIDTH * self.players[0].image_scale)
        height_limit = (0, self.screen.surface.get_height() - P_HEIGHT * self.players[0].image_scale)
        self.players[0]._apply_physics(width_limit, height_limit)
        self.players[1]._apply_physics(width_limit, height_limit)


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
        self.players[0].update(self.screen.surface, self.players[1])
        self.players[1].update(self.screen.surface, self.players[0])
        for player, health in zip(self.players, self.health_bar):
            player.draw(self.screen.surface)
            health.draw(self.screen.surface, player.health)
        self.screen.get_AfterBurner()

    def render(self):
        super().render()

    def next_scene(self):
        return super().next_scene()
