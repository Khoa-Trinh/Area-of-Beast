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
        self.active_bg_color = white
        self.active_text_color = black

        self.is_active = False

    def draw(self, screen: py.Surface):
        if self.is_active:
            border_padding = 4
            border_rect = self.rect.inflate(border_padding * 2, border_padding * 2)
            py.draw.rect(screen, black, border_rect)
            py.draw.rect(screen, self.active_bg_color, self.rect)
            text_color = self.active_text_color
        else:
            py.draw.rect(screen, self.base_bg_color, self.rect)
            text_color = self.base_text_color

        text_surface = self.font.render(self.text, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

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
