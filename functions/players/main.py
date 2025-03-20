import pygame as py
from constants.characters import GRAVITY

SPEED = 11

class Player:
    def __init__(
        self,
        position: tuple[int, int],
        direction: int,
        clock: py.time.Clock,
        player: int,
        character: int,
        health: int
    ):
        # Player settings
        self.x, self.y = position
        self.clock = clock
        self.player = player
        self.health = health
        self.direction = direction
        self.attackdamage = 10  # Damage for normal attack (single hit)
        self.crouch_attackdamage = 2  # Damage per frame for crouch attack (continuous)

        # Animation settings
        self.size = 64
        self.image_scale = 2
        self.offset = (19.2, 20)
        sprite_sheet = py.image.load("assets/images/character.png").convert_alpha()
        sprite_sheet_wide = py.image.load("assets/images/character_wide.png").convert_alpha()
        animation_steps = [4, 4, 4, 4, 4, 4, 1, 2]  # 0: idle, 1: crouch, 2: walk, 3: walkback, 4: jump, 5: jumpsquat, 6: blockstun, 7: hit_stun
        animation_steps_wide = [9, 9, 9]  # 8: attack, 9: crouch_attack, 10: air_attack
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.animation_list.extend(self.load_images(sprite_sheet_wide, animation_steps_wide))
        self.action = 0  # 0: idle, 1: crouch, 2: walk, 3: walkback, 4: jump, 5: jumpsquat, 6: blockstun, 7: hit_stun, 8: attack, 9: crouch_attack, 10: air_attack
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = py.time.get_ticks()

        # Physics and state
        self.is_sitting = False
        self.hurtbox = py.Rect(self.x, self.y, 27.5 * 2, 43.5 * 2)
        self.hitbox = None
        self.framespeed = [12, 9]
        self.jumppower = -60
        self.jumpsquatting = False
        self.jumpsquatframes = 0
        self.on_ground = False
        self.v_x = 0
        self.v_y = 0
        self.is_attacking = False
        self.forward_crouch = False
        self.hit_stunned = False
        self.block_stunned = False
        self.block_count = 0
        self.block_meter = 0
        self.guard_broken = False

    def load_images(self, sprite_sheet, animation_steps):
        animation_list = []
        frame_height = sprite_sheet.get_height() // len(animation_steps)
        for y, steps in enumerate(animation_steps):
            temp_img_list = []
            frame_width = sprite_sheet.get_width() // steps
            for x in range(steps):
                temp_img = sprite_sheet.subsurface(x * frame_width, y * frame_height, frame_width, frame_height)
                temp_img = py.transform.scale(temp_img, (frame_width * self.image_scale, frame_height * self.image_scale))
                temp_img_list.append(temp_img)
            animation_list.append(temp_img_list)
        return animation_list

    def handle_input(self, screen, opponent=None):
        width_limit = (0, screen.get_width() - 27.5 * 2)
        height_limit = (0, screen.get_height() - 43.5 * 2)
        
        key = py.key.get_pressed()
        if self.player == 1:
            lpress, rpress = key[py.K_LEFT], key[py.K_RIGHT]
            upress, dpress = key[py.K_UP], key[py.K_DOWN]
            attack_press = key[py.K_RETURN]
        else:
            lpress, rpress = key[py.K_a], key[py.K_d]
            upress, dpress = key[py.K_w], key[py.K_s]
            attack_press = key[py.K_SPACE]

        # Handle attacks
        if (attack_press and not self.is_attacking and not self.hit_stunned and not self.block_stunned):
            if self.is_sitting:
                self.is_attacking = True
                self.forward_crouch = rpress if self.direction == 1 else lpress
                self.update_action(9)
            elif self.on_ground:
                self.is_attacking = True
                self.update_action(8)

        # Handle movement
        
       # if self.hit_stunned==False: self.v_x = 0

        if not self.is_attacking and not self.hit_stunned and not self.block_stunned:
            self.v_x=0
            if lpress and not rpress and not self.is_sitting and not self.jumpsquatting:
                self.v_x = -SPEED
                if self.on_ground:
                    self.update_action(3 if self.direction == 1 else 2)
            elif rpress and not lpress and not self.is_sitting and not self.jumpsquatting:
                self.v_x = SPEED
                if self.on_ground:
                    self.update_action(2 if self.direction == 1 else 3)
            elif self.on_ground and not self.is_sitting and not self.jumpsquatting:
                self.update_action(0)

            if not self.guard_broken:
                self.is_sitting = dpress and not upress and self.on_ground and not self.jumpsquatting
                if self.is_sitting:
                    self.v_x = 0
                    self.update_action(1)
            else:
                self.is_sitting = False

            if upress and not dpress and self.on_ground and not self.jumpsquatting and not self.is_sitting:
                self.jumpsquatting = True
                self.jumpsquatframes = 0
                self.update_action(5)

        if self.jumpsquatting:
            self.jumpsquatframes += 1
            if self.jumpsquatframes >= 6:
                self.jump()

        self.v_y += GRAVITY
        self.y += self.v_y
        self.x += self.v_x

        self.x = max(width_limit[0], min(self.x, width_limit[1]))
        if self.x == width_limit[0] or self.x == width_limit[1]:
            self.v_x = 0
        if self.y >= height_limit[1]:
            self.y = height_limit[1]
            self.v_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

    def jump(self):
        self.v_y = self.jumppower
        self.jumpsquatting = False
        self.jumpsquatframes = 0
        self.on_ground = False
        self.update_action(4)

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = py.time.get_ticks()

    def update_animation(self):
        animation_cooldown = 1000 // self.framespeed[0]
        if py.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0
                if self.action in (8, 9):
                    self.is_attacking = False
                    self.hitbox = None
                    self.forward_crouch = False
                    self.update_action(1 if self.is_sitting else 0)
                elif self.action == 7:
                    self.hit_stunned = False
                    self.update_action(0)
                elif self.action == 6:
                    self.block_stunned = False
                    self.update_action(0)
            self.update_time = py.time.get_ticks()

            hitbox_width, hitbox_height = 40, 20
            if self.action == 8 and self.frame_index == 5:
                if self.direction == 1:
                    self.hitbox = py.Rect(self.hurtbox.right, self.hurtbox.centery - hitbox_height // 2, hitbox_width, hitbox_height)
                else:
                    self.hitbox = py.Rect(self.hurtbox.left - hitbox_width, self.hurtbox.centery - hitbox_height // 2, hitbox_width, hitbox_height)
            elif self.action == 9:
                if self.direction == 1:
                    self.hitbox = py.Rect(self.hurtbox.right, self.hurtbox.bottom - hitbox_height, hitbox_width, hitbox_height)
                else:
                    self.hitbox = py.Rect(self.hurtbox.left - hitbox_width, self.hurtbox.bottom - hitbox_height, hitbox_width, hitbox_height)
                if self.forward_crouch:
                    self.v_x = 5 * self.direction

        self.image = self.animation_list[self.action][self.frame_index]

    def update_hurtbox(self):
        self.hurtbox.x, self.hurtbox.y = self.x, self.y

    def draw(self, screen: py.Surface):
        flipped_image = py.transform.flip(self.image, True, False) if self.direction == -1 else self.image
        screen.blit(
            flipped_image,
            (self.x - self.offset[0] * self.image_scale, 
             self.y - self.offset[1] * self.image_scale)
        )
        py.draw.rect(screen, (255, 0, 0), self.hurtbox, 2)
        if self.hitbox:
            py.draw.rect(screen, (0, 255, 0), self.hitbox, 2)

    def update(self, screen: py.Surface, opponent=None):
        self.update_hurtbox()
        self.update_animation()
        if self.is_attacking and self.hitbox and opponent and self.hitbox.colliderect(opponent.hurtbox):
            if self.action == 8 and self.frame_index == 5:
                self.handle_collision(opponent)
            elif self.action == 9:
                self.handle_collision(opponent)

    def handle_collision(self, opponent):
        if opponent.is_sitting and opponent.action != 9:
            opponent.block_stun(self.direction)
        else:
            opponent.hit_stun(self.direction)
            opponent.health -= (self.crouch_attackdamage if self.action == 9 else self.attackdamage)

    def hit_stun(self, attack_direction):
        self.hit_stunned = True
        self.v_x = 20 * attack_direction
        self.update_action(7)
        self.block_count = 0
        self.block_meter = max(0, self.block_meter - 10)

    def block_stun(self, attack_direction):
        self.block_stunned = True
        self.v_x = 10 * attack_direction
        self.update_action(6)
        self.block_count += 1
        self.block_meter = min(100, self.block_meter + 20)
        if self.block_meter >= 100:
            self.guard_broken = True
            self.is_sitting = False
            self.update_action(0)