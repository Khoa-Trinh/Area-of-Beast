import pygame as py
import random as ra

from functions.font import Font
from constants.index import red


class DamageCounter:
    def __init__(self, position: tuple[int, int], size: tuple[int, int]):
        self.position = position
        self.size = size
        self.font = Font(12)
        self.show_last = -2000
        self.show_time = 2000
        self.damage = None
        self.prev_damage = None
        self.degree = None

        self.container = (50, 50)
        self.surface = py.Surface(self.container, py.SRCALPHA)

    def trigger(self, damage: int):
      if damage > 0:
        self.damage = (self.damage or 0) + damage
        self.show_last = py.time.get_ticks()

    def draw(self, screen: py.Surface, x: int, y: int):
      current_time = py.time.get_ticks()

      if current_time - self.show_last > self.show_time:
        self.damage = None
        return

      if self.degree is None or self.damage != self.prev_damage:
        self.degree = ra.randint(0, 5) if ra.random() < 0.5 else ra.randint(355, 360)
        self.prev_damage = self.damage

      text = self.font.render(str(self.damage), red)
      text_rect = text.get_rect(centerx=self.container[0] / 2, top=0)

      temp_surface = self.surface.copy()
      temp_surface.blit(text, text_rect)

      rotate_surface = py.transform.rotate(temp_surface, self.degree)
      rotate_rect = rotate_surface.get_rect(
        center=(x + self.size[0] / 2, y + self.size[1] / 2)
      )

      screen.blit(rotate_surface, rotate_rect)
