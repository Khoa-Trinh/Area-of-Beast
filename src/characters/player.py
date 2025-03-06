import pygame
from utils.constants import MAX_HEALTH, WALK_SPEED, SIT_SPEED

class Player:
    def __init__(self, x, y):
        # Load sprites
        self.sprites = {
            'idle': pygame.image.load('assets/images/character1/idle.png'),
            'attack': pygame.image.load('assets/images/character1/attack.png'),  # Sprite với lưỡi
        }
        # Dùng mask để lấy kích thước thân chính từ idle sprite
        mask = pygame.mask.from_surface(self.sprites['idle'])
        mask_rect = mask.get_bounding_rect()
        self.rect = pygame.Rect(x, y, mask_rect.width, mask_rect.height)  # Rect ôm sát thân
        
        # Thuộc tính
        self.health = MAX_HEALTH
        self.is_jumping = False
        self.is_sitting = False
        self.is_attacking = False
        self.velocity_y = 0
        self.gravity = 0.5
        self.hitbox = self.rect.copy()  # Ban đầu hitbox bằng rect
        self.hurtbox = self.rect.copy()  # Ban đầu hurtbox bằng rect
        self.current_sprite = self.sprites['idle']
        self.original_sprites = self.sprites.copy()  # Lưu sprite gốc để flip
        self.attack_frame = 0
        self.attack_power = 10
        self.cooldown = 0
        self.direction = 1  # 1: phải, -1: trái

    def walk(self, dx):
        speed = SIT_SPEED if self.is_sitting else WALK_SPEED
        self.rect.x += dx * speed

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = -10
            self.is_jumping = True

    def attack(self):
        if self.cooldown > 0:
            return
        self.is_attacking = True
        self.cooldown = 50
        self.attack_frame = 0
        self.current_sprite = self.sprites['attack']

    def sit(self):
        self.is_sitting = True

    def stand(self):
        self.is_sitting = False

    def take_damage(self, damage):
        if not self.is_sitting:  # Chỉ ngồi mới block
            self.health -= damage

    def update(self):
        # Cooldown
        if self.cooldown > 0:
            self.cooldown -= 1

        # Nhảy
        if self.is_jumping:
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y
            if self.rect.y >= 300:  # Mặt đất
                self.rect.y = 300
                self.is_jumping = False

        # Tấn công
        if self.is_attacking:
            self.attack_frame += 1
            if self.attack_frame > 10:  # Thời gian tấn công
                self.is_attacking = False
                self.current_sprite = self.sprites['idle']

        # Trạng thái đứng im
        if not self.is_jumping and not self.is_attacking:
            self.current_sprite = self.sprites['idle']

        self.update_hitbox()
        self.update_hurtbox()
        self.flip_sprite()

    def face_direction(self, other_player):
        self.direction = -1 if self.rect.x > other_player.rect.x else 1

    def flip_sprite(self):
        # Lật sprite theo hướng
        if self.direction == -1:
            self.current_sprite = pygame.transform.flip(self.original_sprites['idle' if not self.is_attacking else 'attack'], True, False)
        else:
            self.current_sprite = self.original_sprites['idle' if not self.is_attacking else 'attack']

    def update_hurtbox(self):
        # Hurtbox ôm sát thân dựa trên rect (đã được tính bằng mask từ idle)
        self.hurtbox = self.rect.copy()

    def update_hitbox(self):
        if self.is_attacking:
            # Giả sử lưỡi dài thêm 30px so với thân
            tongue_length = 30
            hitbox_height = 20
            if self.direction == 1:  # Lưỡi thè sang phải
                self.hitbox = pygame.Rect(
                    self.rect.right,  # Bắt đầu từ cạnh phải thân
                    self.rect.centery - hitbox_height // 2,
                    tongue_length,    # Độ dài lưỡi
                    hitbox_height
                )
            else:  # Lưỡi thè sang trái
                self.hitbox = pygame.Rect(
                    self.rect.left - tongue_length,  # Kéo dài sang trái
                    self.rect.centery - hitbox_height // 2,
                    tongue_length,
                    hitbox_height
                )
        else:
            self.hitbox = self.rect.copy()  # Khi không tấn công, hitbox bằng thân

    def draw(self, surface):
        # Căn chỉnh sprite với rect
        sprite_size = self.current_sprite.get_size()
        if self.direction == 1:  # Nhìn phải, lưỡi thè ra bên phải
            offset_x = 0
        else:  # Nhìn trái, lưỡi thè ra bên trái
            offset_x = sprite_size[0] - self.rect.width
        offset_y = sprite_size[1] - self.rect.height  # Căn đáy sprite với rect
        surface.blit(self.current_sprite, (self.rect.x - offset_x, self.rect.y - offset_y))
        pygame.draw.rect(surface, (0, 255, 0), self.rect, 2)    # Debug rect
        pygame.draw.rect(surface, (255, 0, 0), self.hurtbox, 2) # Debug hurtbox
        pygame.draw.rect(surface, (0, 0, 255), self.hitbox, 2)  # Debug hitbox