import pygame
class SpriteSheet:
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert_alpha()

    def get_image(self, x, y, width, height):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        return image

    def get_images(self, x, y, width, height, count):
        images = []
        for i in range(count):
            images.append(self.get_image(x + (i * width), y, width, height))
        return images