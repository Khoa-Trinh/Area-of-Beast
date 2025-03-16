import pygame as py
import math as m

from functions.helper import minmax, get_box
from constants.index import skill_properties


class Skill:
    def __init__(self):
        self.skill_activate = False
        self.skill_last = 0
        self.skill_cooldown = 0
        self.skill_repeat_times = 0
        self.skill_speed = 0
        self.skill_distance = 0

        raise NotImplementedError

    def action(self, *args, **kwargs):
        raise NotImplementedError

    def hit_box(self):
        raise NotImplementedError

    def hit_damage(self):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError


class Skill1(Skill):
    def __init__(self, width: int, height: int):
        # Skill settings(inner)
        self.width = width
        self.height = height
        self.direction = None
        self.can_damage = True

        # Skill settings(outer)
        self.skill_activate = False
        self.skill_last = -skill_properties[0][0]
        self.skill_cooldown = skill_properties[0][0]
        self.skill_distance = skill_properties[0][1]
        self.skill_speed = skill_properties[0][2]
        self.skill_repeat_times = 0

    def action(
        self,
        x: float | int,
        y: float | int,
        degree: int,
        distance: int,
        fps: float,
        _: int,
        limit: tuple[int, int],
    ):
        step = distance / fps

        if self.direction is None:
            self.direction = degree

        move_x = step * m.cos(m.radians(self.direction))
        move_y = -step * m.sin(m.radians(self.direction))

        x = minmax(x + move_x, limit[0])
        y = minmax(y + move_y, limit[1])

        return x, y, False

    def hit_box(self, x: int, y: int):
        return get_box((x, y), (self.width, self.height), 3)

    def hit_damage(self):
        if self.can_damage:
            self.can_damage = False
            return 10
        return 0

    def reset(self):
        self.direction = None
        self.can_damage = True


class Skill2(Skill):
    def __init__(self, width: int, height: int):
        # Skill settings(inner)
        self.width = width
        self.height = height
        self.direction = None
        self.damage = 0
        self.deviation_values = [-100, 200, -200, 200, -100]

        # Skill settings(outer)
        self.skill_activate = False
        self.skill_last = -skill_properties[1][0]
        self.skill_cooldown = skill_properties[1][0]
        self.skill_distance = skill_properties[1][1]
        self.skill_speed = skill_properties[1][2]
        self.skill_repeat_times = 0

    def action(
        self,
        x: float | int,
        y: float | int,
        degree: int,
        distance: int,
        fps: float,
        i: int,
        limit: tuple[int, int],
    ):
        fr = fps / len(self.deviation_values)
        index = min(int(i // fr), len(self.deviation_values) - 1)

        if self.direction is None:
            self.direction = degree

        return self.step(x, y, distance, fr, self.deviation_values[index], limit)

    def step(
        self,
        x: float | int,
        y: float | int,
        distance: int,
        fr: float,
        deviated_value: float,
        limit: tuple[int, int],
    ):
        step = distance / (fr * len(self.deviation_values))
        deviated = deviated_value / fr

        deviated_move_x = step * m.cos(m.radians(self.direction)) + deviated * m.cos(
            m.radians(self.direction + 90)
        )
        deviated_move_y = -step * m.sin(m.radians(self.direction)) + -deviated * m.sin(
            m.radians(self.direction + 90)
        )

        x = minmax(x + deviated_move_x, limit[0])
        y = minmax(y + deviated_move_y, limit[1])
        return x, y, False

    def hit_box(self, x, y):
        return get_box((x, y), (self.width, self.height), 10)

    def hit_damage(self):
        self.damage += 1
        if self.damage > 20:
            return 0
        return 1

    def reset(self):
        self.direction = None
        self.damage = 0


class Skill3(Skill):
    def __init__(self):
        pass


class Skill4(Skill):
    def __init__(self):
        pass


class Skill5(Skill):
    def __init__(self):
        pass


class Skill6(Skill):
    def __init__(self):
        pass


class Skill7(Skill):
    def __init__(self):
        pass


class Skill8(Skill):
    def __init__(self):
        pass


class Skill9(Skill):
    def __init__(self):
        pass


class Skill10(Skill):
    def __init__(self):
        pass


class Skill11(Skill):
    def __init__(self):
        pass


class Skill12(Skill):
    def __init__(self):
        pass


class Skill13(Skill):
    def __init__(self):
        pass


class Skill14(Skill):
    def __init__(self):
        pass


class Skill15(Skill):
    def __init__(self):
        pass


class Skill16(Skill):
    def __init__(self):
        pass


class Skill17(Skill):
    def __init__(self):
        pass


class Skill18(Skill):
    def __init__(self):
        pass


class Skill19(Skill):
    def __init__(self):
        pass


class Skill20(Skill):
    def __init__(self):
        pass
