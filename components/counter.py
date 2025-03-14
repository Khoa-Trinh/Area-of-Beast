import pygame as py

from constants.index import black
from functions.font import Font


class Counter:
    def __init__(self, time):
        self.total_time = time
        self.current = 0
        self.font = Font(32)

    def update(self, screen: py.Surface):
      if self.current == 0:
        self.current = py.time.get_ticks()
      elapsed = py.time.get_ticks() - self.current
      left = max(0, self.total_time - elapsed)
      text = self.font.render(f"{left // 1000}", black)
      text_rect = text.get_rect(center=(screen.get_width() // 2, 35))
      screen.blit(text, text_rect)
      return left
