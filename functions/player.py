import pygame as py

from constants.index import plr_x, plr_y, plr_height, plr_width, plr_color


class Player:
    def __init__(self):
        self.x = plr_x
        self.y = plr_y
        self.height = plr_height
        self.width = plr_width
        self.color = plr_color
        self.can_move = True
        self.coolDown = 0
        self.waiting = False
        self.wait_phase = 0
        self.wait_start = 0

    def draw(self, screen):
        py.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self, screen, x=0, y=0, velo=0.1):
        current_time = py.time.get_ticks()
        coolDown = 1000
        key = py.key.get_pressed()

        if self.can_move:
            if key[py.K_LEFT] and self.x > 0:
                self.x -= velo
            if key[py.K_RIGHT] and self.x < screen.get_width() - self.width:
                self.x += velo
            if key[py.K_UP] and self.y > 0:
                self.y -= velo
            if key[py.K_DOWN] and self.y < screen.get_height() - self.height:
                self.y += velo

            if (
                key[py.K_k]
                and self.wait_phase == 0
                and (current_time - self.coolDown >= coolDown)
            ):
                self.can_move = False
                self.x = min(max(self.x + 50, 0), screen.get_width() - self.width)
                self.y = min(max(self.y + 50, 0), screen.get_height() - self.height)
                self.wait_phase = 1
                self.wait_start = current_time

            if self.wait_phase == 1 and (current_time - self.wait_start >= 50):
                self.x = min(max(self.x + 50, 0), screen.get_width() - self.width)
                self.y = min(max(self.y - 50, 0), screen.get_height() - self.height)
                self.wait_phase = 2
                self.wait_start = current_time

            if self.wait_phase == 2 and (current_time - self.wait_start >= 50):
                self.x = min(max(self.x + 50, 0), screen.get_width() - self.width)
                self.y = min(max(self.y + 50, 0), screen.get_height() - self.height)
                self.coolDown = current_time
                self.can_move = True
                self.wait_phase = 0

        self.draw(screen)

        self.draw(screen)
