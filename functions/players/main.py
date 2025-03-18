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
        
        # Animation settings
        self.size = 64
        self.image_scale = 2
        self.offset = (19.2, 20)
        self.sprite_sheet = py.image.load("assets/images/character.png").convert_alpha()
        self.animation_steps = [4, 4, 4, 4, 4, 4, 1]
        self.animation_list = self.load_images()
        
        # Action states
        self.action = 0  # 0: idle, 1: crouch, 2: walk, 3: walkback, 4: jump, 5: jumpsquat, 6: blockstun
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = py.time.get_ticks()
        
        # Physics and state
        self.is_sitting = False
        self.hurtbox = py.Rect(self.x, self.y, 27.5*2, 43.5*2)
        self.framespeed = [12, 9]
        self.jumppower = -60
        self.jumpsquatting = False
        self.jumpsquatframes = 0
        self.on_ground = False
        self.v_x = 0
        self.v_y = 0

    def load_images(self):
        animation_list = []
        frame_height = self.sprite_sheet.get_height() // len(self.animation_steps)
        
        for y, steps in enumerate(self.animation_steps):
            temp_img_list = []
            frame_width = self.sprite_sheet.get_width() // steps
            
            for x in range(steps):
                temp_img = self.sprite_sheet.subsurface(
                    x * frame_width, 
                    y * frame_height, 
                    frame_width, 
                    frame_height
                )
                temp_img = py.transform.scale(
                    temp_img,
                    (frame_width * self.image_scale, frame_height * self.image_scale)
                )
                temp_img_list.append(temp_img)
                
            animation_list.append(temp_img_list)
        return animation_list

    def handle_input(self, screen):
        width_limit = (0, screen.get_width() - 27.5*2)
        height_limit = (0, screen.get_height() - 43.5*2)
        
        # Get key input based on player number
        key = py.key.get_pressed()
        if self.player == 1:
            lpress, rpress = key[py.K_LEFT], key[py.K_RIGHT]
            upress, dpress = key[py.K_UP], key[py.K_DOWN]
        else:
            lpress, rpress = key[py.K_a], key[py.K_d]
            upress, dpress = key[py.K_w], key[py.K_s]
        
        # Handle horizontal movement
        self.v_x = 0
        if lpress and not rpress and not self.is_sitting and not self.jumpsquatting:
            self.v_x = -SPEED
            if self.on_ground:
                self.update_action(3 if self.direction == 1 else 2)
        elif rpress and not lpress and not self.is_sitting and not self.jumpsquatting:
            self.v_x = SPEED
            if self.on_ground:
                self.update_action(2 if self.direction == 1 else 3)
        elif self.on_ground and not self.is_sitting and not self.jumpsquatting:
            self.update_action(0)  # idle

        # Handle crouching
        self.is_sitting = dpress and not upress and self.on_ground and not self.jumpsquatting
        if self.is_sitting:
            self.v_x = 0
            self.update_action(1)

        # Handle jumping
        if upress and not dpress and self.on_ground and not self.jumpsquatting and not self.is_sitting:
            self.jumpsquatting = True
            self.jumpsquatframes = 0
            self.update_action(5)

        # Process jumpsquat
        if self.jumpsquatting:
            self.jumpsquatframes += 1
            if self.jumpsquatframes >= 6:  # frame count for jumpsquat
                self.jump()
                
        # Apply physics
        self.v_y += GRAVITY
        self.y += self.v_y
        self.x += self.v_x

        # Apply position constraints
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
            self.frame_index = (self.frame_index + 1) % len(self.animation_list[self.action])
            self.update_time = py.time.get_ticks()

        self.image = self.animation_list[self.action][self.frame_index]

    def update_hurtbox(self):
        self.hurtbox.x, self.hurtbox.y = self.x, self.y

    def draw(self, screen: py.Surface):
        screen.blit(
            self.image,
            (self.x - self.offset[0] * self.image_scale, 
             self.y - self.offset[1] * self.image_scale)
        )
        py.draw.rect(screen, (255, 0, 0), self.hurtbox, 2)

    def update(self, screen: py.Surface):
        self.update_hurtbox()
        self.update_animation()