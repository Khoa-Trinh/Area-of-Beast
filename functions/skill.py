import pygame as py
import math as m

from functions.helper import minmax


class Skill1:
    def __init__(self, width, height):
        # Skill settings
        self.width = width
        self.height = height
        self.direction = None
        self.distance = None
        self.remaining_distance = None

    def action(
        self,
        screen: py.Surface,
        x: float | int,
        y: float | int,
        cur_x: int,
        cur_y: int,
        distance: int,
        fps: float,
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
                True
            )

        return x, y, False


class Skill2:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.direction = None
        self.distance = None
        self.deviation_values = [-100, 200, -200, 200, -100]

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
        return x, y
