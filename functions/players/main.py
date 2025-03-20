import pygame as py
from constants.characters import GRAVITY

# Constants to replace magic numbers
SPEED = 11
DEFAULT_ATTACK_DAMAGE = 10
CROUCH_ATTACK_DAMAGE = 2
PLAYER_WIDTH = 27.5 * 2
PLAYER_HEIGHT = 43.5 * 2
HITBOX_WIDTH = 160
HITBOX_HEIGHT = 40
JUMP_POWER = -60
JUMPSQUAT_FRAMES = 6
BLOCK_METER_MAX = 100
BLOCK_METER_INCREMENT = 20
BLOCK_METER_DECREMENT = 10
ANIMATION_ACTIONS = {
    'IDLE': 0, 'CROUCH': 1, 'WALK': 2, 'WALKBACK': 3, 'JUMP': 4, 
    'JUMPSQUAT': 5, 'BLOCKSTUN': 6, 'HIT_STUN': 7, 'ATTACK': 8, 
    'CROUCH_ATTACK': 9, 'AIR_ATTACK': 10
}

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
        self.attackdamage = DEFAULT_ATTACK_DAMAGE
        self.crouch_attackdamage = CROUCH_ATTACK_DAMAGE

        # Animation settings
        self.size = 64
        self.image_scale = 2
        self.offset = (19.2, 20)
        sprite_sheet = py.image.load("assets/images/character.png").convert_alpha()
        sprite_sheet_wide = py.image.load("assets/images/character_wide.png").convert_alpha()
        
        animation_steps = [4, 4, 4, 4, 4, 4, 1, 2]
        animation_steps_wide = [9, 9, 9]
        
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.animation_list.extend(self.load_images(sprite_sheet_wide, animation_steps_wide))
        
        self.action = ANIMATION_ACTIONS['IDLE']
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = py.time.get_ticks()

        # Physics and state
        self.is_sitting = False
        self.hurtbox = py.Rect(self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.hitbox = None
        self.framespeed = [12, 9]
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

    def handle_input(self, screen, opponent=None):
        width_limit = (0, screen.get_width() - PLAYER_WIDTH)
        height_limit = (0, screen.get_height() - PLAYER_HEIGHT)
        
        key = py.key.get_pressed()
        lpress = key[self.left_key]
        rpress = key[self.right_key]
        upress = key[self.up_key]
        dpress = key[self.down_key]
        attack_press = key[self.attack_key]

        # Early return for states that block most inputs
        if self.hit_stunned or self.block_stunned:
            # Physics still apply even when stunned
            self._apply_physics(width_limit, height_limit)
            return

        # Handle attacks
        if attack_press and not self.is_attacking:
            if self.is_sitting:
                self.is_attacking = True
                self.forward_crouch = rpress if self.direction == 1 else lpress
                self.update_action(ANIMATION_ACTIONS['CROUCH_ATTACK'])
            elif self.on_ground:
                self.is_attacking = True
                self.v_x=0
                self.update_action(ANIMATION_ACTIONS['ATTACK'])

        # Handle movement
        if not self.is_attacking:
            self.v_x = 0
            can_move = not self.is_sitting and not self.jumpsquatting
            
            if lpress and not rpress and can_move:
                self.v_x = -SPEED
                if self.on_ground:
                    self.update_action(ANIMATION_ACTIONS['WALKBACK'] if self.direction == 1 
                                      else ANIMATION_ACTIONS['WALK'])
            elif rpress and not lpress and can_move:
                self.v_x = SPEED
                if self.on_ground:
                    self.update_action(ANIMATION_ACTIONS['WALK'] if self.direction == 1 
                                      else ANIMATION_ACTIONS['WALKBACK'])
            elif self.on_ground and can_move:
                self.update_action(ANIMATION_ACTIONS['IDLE'])

            if not self.guard_broken:
                self.is_sitting = dpress and not upress and self.on_ground and not self.jumpsquatting
                if self.is_sitting:
                    self.v_x = 0
                    self.update_action(ANIMATION_ACTIONS['CROUCH'])
            else:
                self.is_sitting = False

            if upress and not dpress and self.on_ground and not self.jumpsquatting and not self.is_sitting:
                self.jumpsquatting = True
                self.jumpsquatframes = 0
                self.update_action(ANIMATION_ACTIONS['JUMPSQUAT'])

        if self.jumpsquatting:
            self.jumpsquatframes += 1
            if self.jumpsquatframes >= JUMPSQUAT_FRAMES:
                self.jump()

        self._apply_physics(width_limit, height_limit)

    def _apply_physics(self, width_limit, height_limit):
        """Apply physics calculations and boundary checks"""
        self.v_y += GRAVITY
        self.y += self.v_y
        self.x += self.v_x

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
        self.update_action(ANIMATION_ACTIONS['JUMP'])

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = py.time.get_ticks()

    def update_animation(self):
        animation_cooldown = 1000 // self.framespeed[0]
        current_time = py.time.get_ticks()
        
        if current_time - self.update_time > animation_cooldown:
            self.frame_index += 1
            frames_in_action = len(self.animation_list[self.action])
            
            if self.frame_index >= frames_in_action:
                self.frame_index = 0
                
                # Handle end of animation states
                if self.action in (ANIMATION_ACTIONS['ATTACK'], ANIMATION_ACTIONS['CROUCH_ATTACK']):
                    self.is_attacking = False
                    self.hitbox = None
                    self.forward_crouch = False
                    self.update_action(ANIMATION_ACTIONS['CROUCH'] if self.is_sitting else ANIMATION_ACTIONS['IDLE'])
                elif self.action == ANIMATION_ACTIONS['HIT_STUN']:
                    self.hit_stunned = False
                    self.update_action(ANIMATION_ACTIONS['IDLE'])
                elif self.action == ANIMATION_ACTIONS['BLOCKSTUN']:
                    self.block_stunned = False
                    self.update_action(ANIMATION_ACTIONS['IDLE'])
                    
            self.update_time = current_time

            # Create hitbox at the right frame of attack animations
            self._update_hitbox()

        self.image = self.animation_list[self.action][self.frame_index]

    def _update_hitbox(self):
        """Update hitbox based on current animation and frame"""
        if self.action == ANIMATION_ACTIONS['ATTACK'] and self.frame_index == 5:
            if self.direction == 1:
                self.hitbox = py.Rect(self.hurtbox.right, 
                                     self.hurtbox.centery - HITBOX_HEIGHT // 2,
                                     HITBOX_WIDTH, HITBOX_HEIGHT)
            else:
                self.hitbox = py.Rect(self.hurtbox.left - HITBOX_WIDTH, 
                                     self.hurtbox.centery - HITBOX_HEIGHT // 2,
                                     HITBOX_WIDTH, HITBOX_HEIGHT)
        elif self.action == ANIMATION_ACTIONS['CROUCH_ATTACK']:
            if self.direction == 1:
                self.hitbox = py.Rect(self.hurtbox.right, 
                                     self.hurtbox.bottom - HITBOX_HEIGHT,
                                     HITBOX_WIDTH, HITBOX_HEIGHT)
            else:
                self.hitbox = py.Rect(self.hurtbox.left - HITBOX_WIDTH, 
                                     self.hurtbox.bottom - HITBOX_HEIGHT,
                                     HITBOX_WIDTH, HITBOX_HEIGHT)
            if self.forward_crouch:
                self.v_x = 5 * self.direction
        else: self.hitbox = None
        

    def update_hurtbox(self):
        self.hurtbox.x, self.hurtbox.y = self.x, self.y

    def draw(self, screen: py.Surface):
        # Only flip if needed
        if self.direction == -1:
            flipped_image = py.transform.flip(self.image, True, False)
        else:
            flipped_image = self.image
            
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
        

    def handle_collision(self, opponent):
        if opponent.is_sitting and opponent.action != ANIMATION_ACTIONS['CROUCH_ATTACK']:
            opponent.block_stun(self.direction)
        else:
            opponent.hit_stun(self.direction)
            damage = self.crouch_attackdamage if self.action == ANIMATION_ACTIONS['CROUCH_ATTACK'] else self.attackdamage
            opponent.health -= damage

    def hit_stun(self, attack_direction):
        self.hit_stunned = True
        self.is_attacking=False
        self.v_x = 10 * attack_direction
        self.update_action(ANIMATION_ACTIONS['HIT_STUN'])
        self.block_count = 0
        self.block_meter = max(0, self.block_meter - BLOCK_METER_DECREMENT)

    def block_stun(self, attack_direction):
        self.block_stunned = True
        self.v_x = 5 * attack_direction
        self.update_action(ANIMATION_ACTIONS['BLOCKSTUN'])
        self.block_count += 1
        self.block_meter = min(BLOCK_METER_MAX, self.block_meter + BLOCK_METER_INCREMENT)
    #  #   if self.block_meter >= BLOCK_METER_MAX:
    #         self.guard_broken = True
    #         self.is_sitting = False
    #         self.block_stunned=False
    #         self.update_action(ANIMATION_ACTIONS['IDLE'])