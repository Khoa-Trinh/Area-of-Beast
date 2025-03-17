import pygame as py

from constants.colors import black, white

class Box:
  def __init__(self, rect):
    self.rect = py.Rect(rect)
    self.border = black
    self.bg_color = white
    self.text_color = black

  def draw(self, screen: py.Surface):
    py.draw.rect(screen, self.border, self.rect)
    py.draw.rect(screen, self.bg_color, self.rect.inflate(-4, -4))
