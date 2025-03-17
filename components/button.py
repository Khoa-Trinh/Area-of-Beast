import pygame as py

from functions.helpers.font import Font
from constants.colors import black, white


class Button:
    def __init__(
        self, rect, text, select, prev=None, next=None, boxtext=None, pos=None
    ):
        # Define callbacks
        self.select = select
        self.prev = prev
        self.next = next

        # Define button properties
        self.rect = py.Rect(rect)
        self.text = text
        self.boxtext = boxtext
        self.pos = pos
        self.font = Font(16)

        # Define button state
        self.is_active = False

        self.base_bg = black
        self.base_text = white
        self.active_bg = white
        self.active_text = black

    def draw(self, screen: py.Surface):
        if self.is_active:
            b_padding = 4
            b_rect = self.rect.inflate(b_padding * 2, b_padding * 2)
            py.draw.rect(screen, black, b_rect)
            py.draw.rect(screen, self.active_bg, self.rect)
            text_color = self.active_text
        else:
            py.draw.rect(screen, self.base_bg, self.rect)
            text_color = self.base_text

        text_surface = self.font.draw(self.text, text_color)
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
                if e.key in (py.K_SPACE, py.K_RETURN):
                    self.select()
                elif e.key in (py.K_LEFT, py.K_a) and self.prev:
                    self.prev()
                elif e.key in (py.K_RIGHT, py.K_d) and self.next:
                    self.next()

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False
