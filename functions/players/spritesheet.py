import pygame as py

class SpriteSheet(py.sprite.Sprite):
    def __init__(self, filename):
        self.spritesheet = py.image.load(filename).convert_alpha()
    
    def get_image(self, x:int, y:int, width:int, height:int, scale=1):
        image = py.Surface((width, height), py.SCRALPHA)
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))

        return image
    
    def get_images(self, positions, width, height, scale=1):
        return [self.get_image(self, x, y, width, height, scale) for x, y in positions]