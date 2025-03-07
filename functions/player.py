import pygame as py

from constants.index import plr_x, plr_y, plr_height, plr_width, plr_color
from functions.skill import Skill1


class Player:
    def __init__(self, clock: py.time.Clock):
        # Player settings
        self.x = plr_x
        self.y = plr_y
        self.height = plr_height
        self.width = plr_width
        self.color = plr_color
        self.clock = clock

        # Player movement
        self.can_move = True

        # Player skill
        self.skill1 = Skill1(plr_width, plr_height)

    def draw(self, screen: py.Surface):
        py.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def movement(self, screen: py.Surface, dt: float, velo=200):
        key = py.key.get_pressed()
        if self.can_move:
            if key[py.K_LEFT]:
                self.x = max(self.x - velo * dt, 0)
            if key[py.K_RIGHT]:
                self.x = min(self.x + velo * dt, screen.get_width() - self.width)
            if key[py.K_UP]:
                self.y = max(self.y - velo * dt, 0)
            if key[py.K_DOWN]:
                self.y = min(self.y + velo * dt, screen.get_height() - self.height)

        self.draw(screen)

    def skill(self, screen: py.Surface):
        key = py.key.get_pressed()

        # Skill 1
        if key[py.K_k]:
          self.x, self.y = self.skill1.action(screen, self.x, self.y)
          self.draw(screen)


    def action(self, screen: py.Surface, dt: float):
        self.movement(screen, dt)
        self.skill(screen)
