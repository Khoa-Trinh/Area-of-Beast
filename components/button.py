import pygame as py

from constants.index import black, white


class Button:
    def __init__(self, rect, text, select, prev=None, next=None):
        # Define callbacks
        self.prev = prev
        self.next = next
        self.select = select

        # Define button properties
        self.rect = py.Rect(rect)
        self.text = text
        self.font = py.font.Font(py.font.match_font("roboto"), 24)
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
        text = self.font.render(self.text, True, text_color)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == py.KEYDOWN:
            if event.key == py.K_RETURN:
                self.select()
            elif event.key in (py.K_a, py.K_LEFT) and self.prev:
                self.prev()
            elif event.key in (py.K_d, py.K_RIGHT) and self.next:
                self.next()

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False
