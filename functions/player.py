import pygame as pygame
from components.damage_counter import DamageCounter
from functions.helper import minmax, approach_angle, get_box


class Player:
    def __init__(
        self,
        position: tuple[int, int],
        clock: py.time.Clock,
        movement: str,
        character: int,
        health: int

    ):
        # Player settings
        self.x = position[0]
        self.y = position[1]
        self.height = size[0]#constant
        self.width = size[1]#constant
        self.clock = clock
        self.move = movement
        self.health = 100
        self.direction = 1 if self.move == "wasd" else -1
        # Player movement
        self.can_move = True
        self.can_use_skill = True
        self.cooldown_percent = [1, 1]


        # Player damage counter
        self.damage_counter = DamageCounter(position, size)

    def hurt_box(self):
        return get_box((self.x, self.y), (self.width, self.height), 4)
    def attack_hitbox(self):
        if self.direction == 0:
            return py.Rect(
                self.rect.
            )
    def lose_health(self, damage: int):
        self.health = max(0, self.health - damage)
        self.damage_counter.trigger(damage)

    def draw(self, screen: py.Surface):
        self.damage_counter.draw(screen, self.x, self.y)
        py.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def action(self, screen: py.Surface):
        key = py.key.get_pressed()
        fps = max(1, int(self.clock.get_fps()))
        self.movement(screen, key, fps)
        self.skill(screen, key, fps)

    def movement(self, screen: py.Surface, key: py.key.ScancodeWrapper, fps: int):
        width_limit = (0, screen.get_width() - self.width)
        height_limit = (0, screen.get_height() - self.height)
        velo = 200

        if self.can_move:
            directions = {
                "wasd": {
                    (py.K_a, py.K_w): (135, -1, -1),
                    (py.K_a, py.K_s): (225, -1, 1),
                    (py.K_d, py.K_w): (45, 1, -1),
                    (py.K_d, py.K_s): (315, 1, 1),
                    py.K_a: (180, -1, 0),
                    py.K_d: (0, 1, 0),
                    py.K_w: (90, 0, -1),
                    py.K_s: (270, 0, 1),
                },
                "arrow": {
                    (py.K_LEFT, py.K_UP): (135, -1, -1),
                    (py.K_LEFT, py.K_DOWN): (225, -1, 1),
                    (py.K_RIGHT, py.K_UP): (45, 1, -1),
                    (py.K_RIGHT, py.K_DOWN): (315, 1, 1),
                    py.K_LEFT: (180, -1, 0),
                    py.K_RIGHT: (0, 1, 0),
                    py.K_UP: (90, 0, -1),
                    py.K_DOWN: (270, 0, 1),
                },
            }

            move_keys = directions[self.move]
            for keys, (angle, dx, dy) in move_keys.items():
                if isinstance(keys, tuple):
                    if all(key[k] for k in keys):
                        self.x = minmax(self.x + dx * velo / fps, width_limit)
                        self.y = minmax(self.y + dy * velo / fps, height_limit)
                        self.direction = approach_angle(self.direction, angle, 3)
                        break
                elif key[keys]:
                    self.x = minmax(self.x + dx * velo / fps, width_limit)
                    self.y = minmax(self.y + dy * velo / fps, height_limit)
                    self.direction = approach_angle(self.direction, angle, 3)
                    break
        self.draw(screen)

    # def skill(self, screen: py.Surface, key: py.key.ScancodeWrapper, fps: int):
    #     # Variables
    #     width_limit = (0, screen.get_width() - self.width)
    #     height_limit = (0, screen.get_height() - self.height)
    #     current_time = py.time.get_ticks()

    #     skill_keys = {
    #         "wasd": (py.K_c, py.K_v),
    #         "arrow": (py.K_COMMA, py.K_PERIOD),
    #     }

    #     if self.move in skill_keys:
    #         keys = skill_keys[self.move]
    #         skills = [self.skill1, self.skill2]
    #         speeds = [fps / skill.skill_speed for skill in skills]

    #     for i, skill in enumerate(skills):
    #         key_code = keys[i]
    #         speed = speeds[i]
    #         self.cooldown_percent[i] = min(
    #             1, (current_time - skill.skill_last) / skill.skill_cooldown
    #         )

    #         if (
    #             key[key_code]
    #             and current_time - skill.skill_last >= skill.skill_cooldown
    #             and self.can_use_skill
    #             and skill.skill_repeat_times == 0
    #         ):
    #             skill.skill_repeat_times = speed
    #             skill.reset()

    #         if skill.skill_repeat_times > 0:
    #             self.x, self.y, stop = skill.action(
    #                 self.x,
    #                 self.y,
    #                 self.direction,
    #                 skill.skill_distance,
    #                 speed,
    #                 speed - skill.skill_repeat_times if i == 1 else 0,
    #                 (width_limit, height_limit),
    #             )
    #             self.draw(screen)
    #             skill.skill_activate = True
    #             skill.skill_last = current_time
    #             skill.skill_repeat_times = max(
    #                 0, skill.skill_repeat_times - 1 if not stop else 0
    #             )
    #         if skill.skill_repeat_times == 0:
    #             skill.skill_activate = False

    #         self.can_move = all(skill.skill_repeat_times == 0 for skill in skills)
    #         self.can_use_skill = self.can_move
