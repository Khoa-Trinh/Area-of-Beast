import pygame as py

from functions.skill import (
    Skill,
    Skill1,
    Skill2,
    Skill3,
    Skill4,
    Skill5,
    Skill6,
    Skill7,
    Skill8,
    Skill9,
    Skill10,
    Skill11,
    Skill12,
    Skill13,
    Skill14,
    Skill15,
    Skill16,
    Skill17,
    Skill18,
    Skill19,
    Skill20,
)
from functions.helper import minmax


class Player:
    def __init__(
        self,
        position: tuple[int, int],
        size: tuple[int, int],
        color: tuple[int, int, int],
        clock: py.time.Clock,
        movement: str,
        character: int,
    ):
        # Player settings
        self.x = position[0]
        self.y = position[1]
        self.height = size[0]
        self.width = size[1]
        self.color = color
        self.clock = clock
        self.move = movement

        # Player character
        self.pick_skill(character)

        # Player movement
        self.can_move = True
        self.can_use_skill = True
        self.cooldown_percent = [1, 1]

        # Player skills
        self.skill1: Skill
        self.skill2: Skill

    def pick_skill(self, skills: int):
        skill_classes: list[tuple[type[Skill], type[Skill]]] = [
            (Skill1, Skill2),
            (Skill3, Skill4),
            (Skill5, Skill6),
            (Skill7, Skill8),
            (Skill9, Skill10),
            (Skill11, Skill12),
            (Skill13, Skill14),
            (Skill15, Skill16),
            (Skill17, Skill18),
            (Skill19, Skill20),
        ]
        if 0 <= skills < len(skill_classes):
            self.skill1, self.skill2 = (
                cls(self.width, self.height) for cls in skill_classes[skills]
            )

    def hurt_box(self):
        return py.Rect(self.x, self.y, self.width * 2, self.height * 2)

    def draw(self, screen: py.Surface):
        py.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def action(self, screen: py.Surface, dt: float):
        self.movement(screen, dt)
        self.skill(screen)

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
            "wasd": (py.K_c, py.K_v),
            "arrow": (py.K_COMMA, py.K_PERIOD),
        }

        if self.move in skill_keys:
            keys = skill_keys[self.move]
            skills = [self.skill1, self.skill2]
            speeds = [fps / skill.skill_speed for skill in skills]

        for i, skill in enumerate(skills):
            key_code = keys[i]
            speed = speeds[i]
            self.cooldown_percent[i] = min(
                1, (current_time - skill.skill_last) / skill.skill_cooldown
            )

            if (
                key[key_code]
                and current_time - skill.skill_last >= skill.skill_cooldown
                and self.can_use_skill
                and skill.skill_repeat_times == 0
            ):
                skill.skill_repeat_times = speed
                skill.reset()

            if skill.skill_repeat_times > 0:
                self.x, self.y, stop = skill.action(
                    screen,
                    self.x,
                    self.y,
                    cur_x,
                    cur_y,
                    skill.skill_distance,
                    speed,
                    speed - skill.skill_repeat_times if i == 1 else 0,
                )
                self.draw(screen)
                skill.skill_activate = True
                skill.skill_last = current_time
                skill.skill_repeat_times = max(
                    0, skill.skill_repeat_times - 1 if not stop else 0
                )
            if skill.skill_repeat_times == 0:
                skill.skill_activate = False

            self.can_move = all(skill.skill_repeat_times == 0 for skill in skills)
            self.can_use_skill = self.can_move
