import pygame as py
from constants.characters import GRAVITY

# Constants to replace magic numbers
SPEED = 11
NORMAL_ATTACK_DAMAGE = 10
CROUCH_ATTACK_DAMAGE = 1
P_WIDTH = 27.5
P_HEIGHT = 43.5
PCROUCH_HEIGHT = 31.5
HITBOX_WIDTH = 95
HITBOX_HEIGHT = 20
CROUCH_HITBOX_WIDTH=30
CROUCH_HITBOX_HEIGHT=25
JUMP_POWER = -60
JUMPSQUAT_FRAMES = 6
BLOCK_METER_MAX = 100
BLOCK_METER_INCREMENT = 20
BLOCK_METER_DECREMENT = 1
ACTIONS = {
    'IDLE': 0, 'CROUCH': 1, 'WALK': 2, 'WALKBACK': 3, 'JUMP': 4, 
    'JUMPSQUAT': 5, 'BLOCKSTUN': 6, 'HIT_STUN': 7, 'ATTACK': 8, 
    'CROUCH_ATTACK': 9, 'AIR_ATTACK': 10
}     
ANIMATION_STEPS = [4, 4, 4, 4, 4, 4, 1, 2]
ANIMATION_STEPS_WIDE = [9, 9, 9]
OFFSET_VALUES = [
    (19.2, 20),  # IDLE
    (19.2, 20),  # CROUCH
    (19.2, 20),  # WALK
    (19.2, 20),  # WALKBACK
    (19.2, 20),  # JUMP
    (19.2, 20),  # JUMPSQUAT
    (19.2, 20),  # BLOCKSTUN
    (19.2, 20),  # HIT_STUN
    (112.5, 32.5),  # ATTACK
    (112.5, 32.5), # CROUCH_ATTACK
    (20.0, 21),  # AIR_ATTACK
]
framespeed = [
    9,  # IDLE
    12, # CROUCH
    12, # WALK
    12, # WALKBACK
    12, # JUMP
    20, # JUMPSQUAT
    5,  # BLOCKSTUN
    6,  # HIT_STUN
    12, # ATTACK
    14, # CROUCH_ATTACK
    12  # AIR_ATTACK
]

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
        self.attackdamage = NORMAL_ATTACK_DAMAGE
        self.crouch_attackdamage = CROUCH_ATTACK_DAMAGE

        # Animation settings
        self.size = 64
        self.image_scale = 3
        self.offset = (19.2, 20)
        sprite_sheet = py.image.load("assets/images/character.png").convert_alpha()
        sprite_sheet_wide = py.image.load("assets/images/character_wide.png").convert_alpha()
        
        self.animation_list = self.load_images(sprite_sheet, ANIMATION_STEPS)
        self.animation_list.extend(self.load_images(sprite_sheet_wide, ANIMATION_STEPS_WIDE))
        
        self.action = ACTIONS['IDLE']
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = py.time.get_ticks()

        # Physics and state
        self.is_sitting = False
        self.hurtbox = py.Rect(self.x, self.y, P_WIDTH*self.image_scale, P_HEIGHT*self.image_scale)
        self.hitbox = None
        self.jumppower = JUMP_POWER
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
        self.has_hit = False  # Flag to prevent multiple hits in one normal attack  
        # Control mappings (cached)
        self._setup_controls()

    def _setup_controls(self):
        """Cache control mappings to avoid repeating them"""
        if self.player == 1:
            self.left_key = py.K_LEFT
            self.right_key = py.K_RIGHT
            self.up_key = py.K_UP
            self.down_key = py.K_DOWN
            self.attack_key = py.K_RETURN
        else:
            self.left_key = py.K_a
            self.right_key = py.K_d
            self.up_key = py.K_w
            self.down_key = py.K_s
            self.attack_key = py.K_SPACE

    def load_images(self, sprite_sheet, animation_steps):
        animation_list = []
        frame_height = sprite_sheet.get_height() // len(animation_steps)
        frame_width = sprite_sheet.get_width() // max(animation_steps)
        for y, steps in enumerate(animation_steps):
            temp_img_list = []
            scaled_height = frame_height * self.image_scale
            scaled_width = frame_width * self.image_scale
            
            for x in range(steps):
                temp_img = sprite_sheet.subsurface(x * frame_width, y * frame_height, frame_width, frame_height)
                temp_img = py.transform.scale(temp_img, (scaled_width, scaled_height))
                temp_img_list.append(temp_img)
                
            animation_list.append(temp_img_list)
        return animation_list
    
    def debug_attack_frame(self):
        self.action = ACTIONS['CROUCH_ATTACK']
        self.frame_index = 1
        self.offset = OFFSET_VALUES[self.action]  # Update offset for ATTACK
        self.image = self.animation_list[self.action][self.frame_index]

    def handle_input(self, screen, opponent=None):
        width_limit = (0, screen.get_width() - P_WIDTH*self.image_scale)
        height_limit = (0, screen.get_height() - P_HEIGHT*self.image_scale)
        
        key = py.key.get_pressed()
        lpress = key[self.left_key]
        rpress = key[self.right_key]
        upress = key[self.up_key]
        dpress = key[self.down_key]
        attack_press = key[self.attack_key]

        # Early return for states that block most inputs
        if self.hit_stunned or self.block_stunned:
            self._apply_physics(width_limit, height_limit)
            return

        # Handle attacks
        if attack_press and not self.is_attacking and not self.jumpsquatting:
            if self.is_sitting:
                self.is_attacking = True
                self.forward_crouch = rpress if self.direction == 1 else lpress
                if self.forward_crouch:
                    self.v_x = 5 * self.direction
                self.update_action(ACTIONS['CROUCH_ATTACK'])
            elif self.on_ground:
                self.is_attacking = True
                self.v_x = 0
                self.update_action(ACTIONS['ATTACK'])

        # Handle movement
        if not self.is_attacking:
            self.v_x = 0
            can_move = not self.is_sitting and not self.jumpsquatting
            
            if lpress and not rpress and can_move:
                self.v_x = -SPEED
                if self.on_ground:
                    self.update_action(ACTIONS['WALKBACK'] if self.direction == 1 
                                      else ACTIONS['WALK'])
            elif rpress and not lpress and can_move:
                self.v_x = SPEED
                if self.on_ground:
                    self.update_action(ACTIONS['WALK'] if self.direction == 1 
                                      else ACTIONS['WALKBACK'])
            elif self.on_ground and can_move:
                self.update_action(ACTIONS['IDLE'])

            self.is_sitting = dpress and not upress and self.on_ground and not self.jumpsquatting and not self.guard_broken
            if not self.is_sitting and self.block_meter > 0:
                self.block_meter -= BLOCK_METER_DECREMENT
                if self.block_meter <= 0:
                    self.block_meter = 0
                    self.guard_broken = False


            if not self.guard_broken:
                self.is_sitting = dpress and not upress and self.on_ground and not self.jumpsquatting
                if self.is_sitting:
                    self.v_x = 0
                    self.update_action(ACTIONS['CROUCH'])
            else:
                self.is_sitting = False


            if upress and not dpress and self.on_ground and not self.jumpsquatting and not self.is_sitting:
                self.jumpsquatting = True
                self.jumpsquatframes = 0
                self.update_action(ACTIONS['JUMPSQUAT'])

        if self.jumpsquatting:

            self.jumpsquatframes += 1
            if self.jumpsquatframes >= JUMPSQUAT_FRAMES:
                self.jump()


    def _apply_physics(self, width_limit, height_limit):
        """Apply physics calculations and boundary checks"""
        self.v_y += GRAVITY
        self.y += self.v_y
        self.x += self.v_x

        if self.hit_stunned or self.block_stunned:
            self.v_x *= 0.6  
        # Boundary checks
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
        self.update_action(ACTIONS['JUMP'])

    def update_action(self, new_action):
        if new_action != self.action or self.hit_stunned or self.block_stunned:
            self.action = new_action
            self.offset = OFFSET_VALUES[self.action]
            self.frame_index = 0
            self.update_time = py.time.get_ticks()

    def update_animation(self):
        animation_cooldown = 1000 // framespeed[self.action]
        current_time = py.time.get_ticks()
        
        if current_time - self.update_time > animation_cooldown:
            self.frame_index += 1
            frames_in_action = len(self.animation_list[self.action])
            
            if self.frame_index >= frames_in_action:
                self.frame_index = 0
                if self.action in (ACTIONS['ATTACK'], ACTIONS['CROUCH_ATTACK']):
                    self.is_attacking = False
                    self.hitbox = None
                    self.forward_crouch = False
                    if self.action == ACTIONS['ATTACK']:
                        self.has_hit = False  # Reset only for normal attack
                    self.update_action(ACTIONS['CROUCH'] if self.is_sitting else ACTIONS['IDLE'])
                elif self.action == ACTIONS['HIT_STUN']:
                    self.hit_stunned = False
                    self.v_x = 0
                    self.update_action(ACTIONS['IDLE'])
                elif self.action == ACTIONS['BLOCKSTUN']:
                    self.block_stunned = False
                    self.v_x = 0
                    self.update_action(ACTIONS['IDLE'])
                    
            self.update_time = current_time

        self.image = self.animation_list[self.action][self.frame_index]

    def _update_hitbox(self):
        """Update hitbox based on current animation and frame"""
        if self.action == ACTIONS['ATTACK'] and self.frame_index == 5 and not self.has_hit:
            if self.direction == 1:
                self.hitbox = py.Rect(self.hurtbox.right, 
                                     self.hurtbox.centery - HITBOX_HEIGHT*self.image_scale // 2,
                                     HITBOX_WIDTH*self.image_scale, HITBOX_HEIGHT*self.image_scale)
            else:
                self.hitbox = py.Rect(self.hurtbox.left - HITBOX_WIDTH*self.image_scale, 
                                     self.hurtbox.centery - HITBOX_HEIGHT*self.image_scale // 2,
                                     HITBOX_WIDTH*self.image_scale, HITBOX_HEIGHT*self.image_scale)
        elif (self.action == ACTIONS['CROUCH_ATTACK'] and 
              self.frame_index in (2, 3, 4, 5)):  # Hitbox active on frames 2, 3, 4, 5
            if self.direction == 1:
                self.hitbox = py.Rect(self.hurtbox.right, 
                                     self.hurtbox.bottom - CROUCH_HITBOX_HEIGHT*self.image_scale,
                                     CROUCH_HITBOX_WIDTH*self.image_scale, CROUCH_HITBOX_HEIGHT*self.image_scale)
            else:
                self.hitbox = py.Rect(self.hurtbox.left - CROUCH_HITBOX_WIDTH*self.image_scale, 
                                     self.hurtbox.bottom - CROUCH_HITBOX_HEIGHT*self.image_scale,
                                     CROUCH_HITBOX_WIDTH*self.image_scale, CROUCH_HITBOX_HEIGHT*self.image_scale)
        else:
            self.hitbox = None

    def _update_hurtbox(self):
        if self.action != ACTIONS['CROUCH'] and self.action != ACTIONS['CROUCH_ATTACK'] :self.hurtbox=py.Rect(self.x,self.y,P_WIDTH*self.image_scale,P_HEIGHT*self.image_scale)
        else: self.hurtbox= py.Rect(self.x,self.y+(P_HEIGHT-PCROUCH_HEIGHT)*self.image_scale,P_WIDTH*self.image_scale,PCROUCH_HEIGHT*self.image_scale)

    def draw(self, screen: py.Surface):
        if self.direction == -1:
            flipped_image = py.transform.flip(self.image, True, False)
        else:
            flipped_image = self.image
            
        screen.blit(
            flipped_image,
            (self.x - self.offset[0] * self.image_scale, 
             self.y - self.offset[1] * self.image_scale)
        )
        

        meter_width = 50
        meter_height = 5
        meter_x = self.x + (P_WIDTH * self.image_scale - meter_width) // 2
        meter_y = self.y - 10
        py.draw.rect(screen, (255, 255, 255), (meter_x, meter_y, meter_width, meter_height))  # Nền trắng
        filled_width = (self.block_meter / BLOCK_METER_MAX) * meter_width
        py.draw.rect(screen, (0, 0, 255), (meter_x, meter_y, filled_width, meter_height))    # Thanh xanh
        if self.guard_broken:
            py.draw.rect(screen, (255, 0, 0), (meter_x, meter_y, meter_width, meter_height), 2)  # Viền đỏ khi vỡ khiên

    def update(self, screen: py.Surface, opponent=None):
        self._update_hurtbox()
        self.update_animation()
        self._update_hitbox()
    def handle_collision(self, opponent):
        if self.action == ACTIONS['ATTACK'] and not self.has_hit:
            # Normal attack: Hit once and set flag
            if opponent.is_sitting and opponent.action != ACTIONS['CROUCH_ATTACK']:
                opponent.block_stun(self.direction, 5)
            else:
                opponent.hit_stun(self.direction, 22)
                opponent.health -= self.attackdamage
            self.has_hit = True  # Prevent further hits this attack
        elif self.action == ACTIONS['CROUCH_ATTACK']:
            # Crouch attack: Hit every time on frames 2, 3, 4, 5
            if opponent.is_sitting and opponent.action != ACTIONS['CROUCH_ATTACK']:
                opponent.block_stun(self.direction,2.5)
            else:
                opponent.hit_stun(self.direction,8)
                opponent.health -= self.crouch_attackdamage
    def hit_stun(self, attack_direction,knockback):
            self.hit_stunned = True
            self.is_attacking = False
            self.v_x = knockback * attack_direction 
            self.update_action(ACTIONS['HIT_STUN'])


    def block_stun(self, attack_direction, knockback):
            self.block_stunned = True
            self.v_x = knockback * attack_direction  
            self.update_action(ACTIONS['BLOCKSTUN'])
            self.block_meter += BLOCK_METER_INCREMENT  
            if self.block_meter >= BLOCK_METER_MAX:  
                self.guard_broken = True
                self.block_meter = BLOCK_METER_MAX     
            self.update_action(ACTIONS['BLOCKSTUN'])
