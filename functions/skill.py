import pygame as py
import math as m

from functions.helper import minmax
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

    def reset(self):
        raise NotImplementedError


class Skill1(Skill):
    def __init__(self, width, height):
        # Skill settings(inner)
        self.width = width
        self.height = height
        self.direction = None
        self.distance = None
        self.remaining_distance = None

        # Skill settings(outer)
        self.skill_activate = False
        self.skill_last = -skill_properties[0][0]
        self.skill_cooldown = skill_properties[0][0]
        self.skill_distance = skill_properties[0][1]
        self.skill_speed = skill_properties[0][2]
        self.skill_repeat_times = 0

    def action(
        self,
        screen: py.Surface,
        x: float | int,
        y: float | int,
        cur_x: int,
        cur_y: int,
        distance: int,
        fps: float,
        _: int,
    ):
        dx, dy = cur_x - x, cur_y - y
        step = distance / fps
        width_limit = (0, screen.get_width() - self.width)
        height_limit = (0, screen.get_height() - self.height)

        if self.direction is None or self.distance is None:
            self.direction = m.degrees(m.atan2(dy, dx))
            self.distance = m.hypot(dx, dy)
            self.remaining_distance = self.distance

        move_x = step * m.cos(m.radians(self.direction))
        move_y = step * m.sin(m.radians(self.direction))

        x = minmax(x + move_x, width_limit)
        y = minmax(y + move_y, height_limit)

        self.remaining_distance -= step
        if self.remaining_distance <= 0:
            return (
                minmax(cur_x - self.width / 2, width_limit),
                minmax(cur_y - self.height / 2, height_limit),
                True,
            )

        return x, y, False

    def hit_box(self, x: int, y: int):
        return py.Rect(x, y, self.width * 2, self.height * 2)

    def reset(self):
        self.direction = None
        self.distance = None
        self.remaining_distance = None


class Skill2(Skill):
    def __init__(self, width, height):
        # Skill settings(inner)
        self.width = width
        self.height = height
        self.direction = None
        self.distance = None
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
        screen: py.Surface,
        x: float | int,
        y: float | int,
        cur_x: int,
        cur_y: int,
        distance: int,
        fps: float,
        i: int,
    ):
        fr = fps / len(self.deviation_values)
        index = min(int(i // fr), len(self.deviation_values) - 1)

        dx, dy = cur_x - x, cur_y - y
        if self.direction is None or self.distance is None:
            self.direction = m.degrees(m.atan2(dy, dx))
            self.distance = m.hypot(dx, dy)

        if distance > self.distance:
            distance = self.distance

        return self.step(screen, x, y, distance, fr, self.deviation_values[index])

    def step(
        self,
        screen: py.Surface,
        x: float | int,
        y: float | int,
        distance: int,
        fr: float,
        deviated_value: float,
    ):
        step = distance / (fr * len(self.deviation_values))
        deviated = deviated_value / fr
        width_limit = (0, screen.get_width() - self.width)
        height_limit = (0, screen.get_height() - self.height)

        deviated_move_x = step * m.cos(m.radians(self.direction)) + deviated * m.cos(
            m.radians(self.direction + 90)
        )
        deviated_move_y = step * m.sin(m.radians(self.direction)) + deviated * m.sin(
            m.radians(self.direction + 90)
        )

        x = minmax(x + deviated_move_x, width_limit)
        y = minmax(y + deviated_move_y, height_limit)
        return x, y, False

    def hit_box(self, x, y):
        return py.Rect(x, y, self.width * 2, self.height * 2)

    def reset(self):
        self.direction = None
        self.distance = None


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
