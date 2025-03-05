import pygame
from utils.constants import MAX_HEALTH, WALK_SPEED, SIT_SPEED

class Player:
    def __init__(self, x, y):
        self.sprites = {
            'idle': pygame.image.load('assets/images/character1/idle.png'),
            # 'walk': pygame.image.load('assets/images/character1/move_right.png'),
            # 'attack': pygame.image.load('assets/images/character1/attack.png'),
            # 'jump': pygame.image.load('assets/images/character1/jump.png'),
            # 'sit': pygame.image.load('assets/images/character1/sit.png'),
        }
        size = self.sprites['idle'].get_size()
        self.rect = pygame.Rect(x, y, size[0], size[1])
        self.health = MAX_HEALTH
        self.is_jumping = False
        self.is_sitting = False
        self.is_attacking = False
        self.is_dashing = False
        self.is_blocking = False
        self.velocity_y = 0
        self.gravity = 0.5
        self.hitbox = pygame.Rect(x, y, 50, 50)  # Placeholder for hitbox
        self.hurtbox = pygame.Rect(x, y, size[0], size[1])  # Placeholder for hurtbox
        self.current_sprite = self.sprites['idle']
        self.original_sprite = self.current_sprite  # Store the original sprite
        self.attack_frame = 0
        self.attack_power = 10  # Damage value
        self.attack_range = 20  # Attack range
        self.cooldown = 0
        self.direction = 1  # 1 for right, -1 for left

    def walk(self, dx):
        if self.is_sitting:
            self.rect.x += dx * SIT_SPEED
        else:
            self.rect.x += dx * WALK_SPEED
        self.current_sprite = self.sprites['idle']

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = -10  # Jump strength
            self.is_jumping = True
        self.current_sprite = self.sprites['idle']

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1

        if self.is_jumping:
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y
            if self.rect.y >= 300:  # Ground level
                self.rect.y = 300
                self.is_jumping = False

        if self.is_attacking:
            self.attack_frame += 1
            if self.attack_frame > 10:  # Attack duration
                self.is_attacking = False

        if not self.is_jumping and not self.is_attacking:
            self.current_sprite = self.sprites['idle']

        self.update_hitbox()
        self.update_hurtbox()
        self.flip_sprite()

    def attack(self):
        if self.cooldown > 0:
            return  # Exit the method if cooldown is active

        self.is_attacking = True
        self.cooldown = 50  # Set cooldown duration
        self.attack_frame = 0
        self.current_sprite = self.sprites['idle']
        # Implement attack logic

    def sit(self):
        self.is_sitting = True
        self.is_blocking = True  # Block when sitting
        self.current_sprite = self.sprites['idle']

    def stand(self):
        self.is_sitting = False
        self.is_blocking = False  # Stop blocking when standing

    def take_damage(self, damage):
        if not self.is_blocking:
            self.health -= damage

    def draw(self, surface):
        surface.blit(self.current_sprite, (self.rect.x, self.rect.y))
        pygame.draw.rect(surface, (255, 0, 0), self.hurtbox, 2)
   # def render(self, surface, rect):
   #     surface.blit(surface, (rect.x - camera.x, rect.y - camera.y))

    def face_direction(self, other_player):
        if self.rect.x > other_player.rect.x:
            self.direction = -1
        else:
            self.direction = 1

    def flip_sprite(self):
        if self.direction == -1:
            self.current_sprite = pygame.transform.flip(self.original_sprite, True, False)
        else:
            self.current_sprite = self.original_sprite

    def update_hitbox(self):
        # Update hitbox based on character's position and state
        self.hitbox = self.rect.inflate(20, 20)
       # self.hitbox.topleft = self.rect.topleft  # Example hitbox size

    def update_hurtbox(self):
          # Example hurtbox size
        self.hurtbox.topleft=self.rect.topleft