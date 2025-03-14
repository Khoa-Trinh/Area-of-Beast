import pygame as py

from constants.index import black, white
from functions.font import Font


class Button:
    def __init__(
        self,
        rect,
        text,
        select,
        prev=None,
        next=None,
        boxtext=None,
        pos=None,
    ):
        # Define callbacks
        self.prev = prev
        self.next = next
        self.select = select
        self.pos = pos
        self.boxtext = boxtext

        # Define button properties
        self.rect = py.Rect(rect)
        self.text = text
        self.font = Font(12)
        self.base_bg_color = black
        self.base_text_color = white

        # Colors for active state
        self.active_bg_color = white
        self.active_text_color = black

        self.is_active = False

    def draw(self, screen: py.Surface):
        if self.is_active:
            bg_color = self.active_bg_color
            text_color = self.active_text_color
        else:
            bg_color = self.base_bg_color
            text_color = self.base_text_color

        py.draw.rect(screen, bg_color, self.rect)
        text = self.font.render(self.text, text_color)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def handle_event(self, e):
        if e.type == py.KEYDOWN:
            if self.pos == "left":
                if e.key == py.K_x:
                    self.select()
                elif e.key == py.K_a and self.prev:
                    self.prev()
                elif e.key == py.K_d and self.next:
                    self.next()
            elif self.pos == "right":
                if e.key == py.K_SLASH:
                    self.select()
                elif e.key == py.K_LEFT and self.prev:
                    self.prev()
                elif e.key == py.K_RIGHT and self.next:
                    self.next()
            else:
                if e.key == py.K_RETURN:
                    self.select()
                elif e.key in (py.K_LEFT, py.K_a) and self.prev:
                    self.prev()
                elif e.key in (py.K_RIGHT, py.K_d) and self.next:
                    self.next()

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False
