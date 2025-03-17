import pygame

pygame.init()
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Character settings
WALK_SPEED = 5
SIT_SPEED = 1
PARRY_FRAMES = 30
JUMP_HEIGHT = 15
GRAVITY = 1


# Hitbox and Hurtbox settings
HITBOX_WIDTH = 50
HITBOX_HEIGHT = 50
HURTBOX_WIDTH = 50
HURTBOX_HEIGHT = 50

# Game settings
MAX_HEALTH = 100
DAMAGE = 10