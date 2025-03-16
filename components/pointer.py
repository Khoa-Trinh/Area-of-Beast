import pygame as py


class Pointer:
    def __init__(
        self,
        position: tuple[int, int],
        size: tuple[int, int],
        color: tuple[int, int, int],
    ):
        self.position = position
        self.size = size
        self.color = color

        self.container = (self.size[0] * 3, self.size[1] * 3)
        self.surface = py.Surface(self.container, py.SRCALPHA)

        pointer = py.Rect(0, 0, 4, 4)
        pointer.right = self.container[0]
        pointer.centery = self.container[1] / 2
        py.draw.rect(self.surface, self.color, pointer)

    def draw(self, screen: py.Surface, x: int, y: int, degree: int):
        rotate_surface = py.transform.rotate(self.surface, degree)
        rotate_rect = rotate_surface.get_rect(
            center=(x + self.size[0] / 2, y + self.size[1] / 2)
        )
        screen.blit(rotate_surface, rotate_rect)
