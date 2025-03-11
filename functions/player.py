import pygame as py

from constants.index import (
    skill_1_cooldown_duration,
    skill_1_distance,
    skill_1_speed,
    skill_2_cooldown_duration,
    skill_2_distance,
    skill_2_speed,
)
from functions.skill import Skill1, Skill2
from functions.helper import minmax


class Player:
    def __init__(
        self,
        position: tuple[int, int],
        size: tuple[int, int],
        color: tuple[int, int, int],
        clock: py.time.Clock,
        movement: str,
    ):
        # Player settings
        self.x = position[0]
        self.y = position[1]
        self.height = size[0]
        self.width = size[1]
        self.color = color
        self.clock = clock
        self.move = movement

        # Player movement
        self.can_move = True
        self.can_use_skill = True

        # Player skill
        self.skill1 = Skill1(self.width, self.height)
        self.skill_1_last = -skill_1_cooldown_duration
        self.skill_1_cooldown = skill_1_cooldown_duration
        self.skill_1_repeat_times = 0
        self.skill_1_speed = skill_1_speed

        self.skill2 = Skill2(self.width, self.height)
        self.skill_2_last = -skill_2_cooldown_duration
        self.skill_2_cooldown = skill_2_cooldown_duration
        self.skill_2_repeat_times = 0
        self.skill_2_speed = skill_2_speed

    def draw(self, screen: py.Surface):
        py.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def movement(self, screen: py.Surface, dt: float, velo=200):
        key = py.key.get_pressed()
        width_limit = (0, screen.get_width() - self.width)
        height_limit = (0, screen.get_height() - self.height)

        if self.can_move:
            directions = {
                "wasd": {
                    py.K_a: (-velo * dt, 0),
                    py.K_d: (velo * dt, 0),
                    py.K_w: (0, -velo * dt),
                    py.K_s: (0, velo * dt),
                },
                "arrow": {
                    py.K_LEFT: (-velo * dt, 0),
                    py.K_RIGHT: (velo * dt, 0),
                    py.K_UP: (0, -velo * dt),
                    py.K_DOWN: (0, velo * dt),
                },
            }
            for key_code, (dx, dy) in directions.get(self.move, {}).items():
                if key[key_code]:
                    self.x = minmax(self.x + dx, width_limit)
                    self.y = minmax(self.y + dy, height_limit)

        self.draw(screen)

    def skill(self, screen: py.Surface):
        # Variables
        key = py.key.get_pressed()
        current_time = py.time.get_ticks()
        cur_x, cur_y = py.mouse.get_pos()
        fps = int(self.clock.get_fps())

        skill_keys = {
            "wasd": {"skill1": py.K_c, "skill2": py.K_v},
            "arrow": {"skill1": py.K_COMMA, "skill2": py.K_PERIOD},
        }

        if self.move in skill_keys:
            keys = skill_keys[self.move]

            # Skill 1
            if (
                key[keys["skill1"]]
                and current_time - self.skill_1_last >= self.skill_1_cooldown
                and self.can_use_skill
                and self.skill_1_repeat_times == 0
            ):
                # Setting
                self.skill_1_repeat_times = fps / self.skill_1_speed
                self.skill1.direction = None
                self.skill1.distance = None
                self.skill1.remaining_distance = None

            if self.skill_1_repeat_times > 0:
                # Action
                self.x, self.y, stop = self.skill1.action(
                    screen,
                    self.x,
                    self.y,
                    cur_x,
                    cur_y,
                    skill_1_distance,
                    fps / self.skill_1_speed,
                )
                self.draw(screen)
                self.skill_1_last = current_time
                self.skill_1_repeat_times = max(
                    0, self.skill_1_repeat_times - 1 if not stop else 0
                )

            # Skill 2
            if (
                key[keys["skill2"]]
                and current_time - self.skill_2_last >= self.skill_2_cooldown
                and self.can_use_skill
                and self.skill_2_repeat_times == 0
            ):
                # Setting
                self.skill_2_repeat_times = fps
                self.skill2.direction = None
                self.skill2.distance = None

            if self.skill_2_repeat_times > 0:
                # Action
                self.x, self.y = self.skill2.action(
                    screen,
                    self.x,
                    self.y,
                    cur_x,
                    cur_y,
                    skill_2_distance,
                    fps,
                    fps - self.skill_2_repeat_times,
                )
                self.draw(screen)
                self.skill_2_last = current_time
                self.skill_2_repeat_times -= 1

            self.can_move = (
                self.skill_1_repeat_times == 0 and self.skill_2_repeat_times == 0
            )
            self.can_use_skill = self.can_move

    def action(self, screen: py.Surface, dt: float):
        self.movement(screen, dt)
        self.skill(screen)
