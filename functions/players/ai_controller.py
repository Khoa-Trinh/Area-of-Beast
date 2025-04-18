import pygame as py
import random

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
class AIController:
    def __init__(self, player, opponent):
        self.player = player 
        self.opponent = opponent  # Human player
        self.range_inaccuracy = 15  
        self.reaction_frames = 5
        self.frame_counter = 0

        self.game_plans = ["FOOTSIES", "ZONING", "RUSHDOWN"]
        self.current_game_plan = random.choice(self.game_plans)
        self.switch_frames = random.randint(100, 300)  
        self.optimal_range = 100

        self.current_game_plan = "RUSHDOWN"

        self.normal_attack_range = HITBOX_WIDTH * self.player.image_scale  
        self.crouch_attack_range = CROUCH_HITBOX_WIDTH * self.player.image_scale  
        self.optimal_range = self.crouch_attack_range  

    def update(self, screen):

        self.frame_counter += 1
        self.switch_frames -= 1


        if self.current_game_plan == "FOOTSIES":
            self.optimal_range = 100
        elif self.current_game_plan == "ZONING":
            self.optimal_range = 150
        elif self.current_game_plan == "RUSHDOWN":
            self.optimal_range = 50


        distance = self.player.x - self.opponent.x
        abs_distance = abs(distance)

        self.player.direction = 1 if self.player.x < self.opponent.x else -1

        if self.frame_counter >= self.reaction_frames:
            self.frame_counter = 0
            self.decide_action(abs_distance, distance, screen)

    def decide_action(self, abs_distance, distance, screen):

        if not self.player.on_ground and not self.player.jumpsquatting:
            self.player.v_x = 0  

        if self.player.hit_stunned or self.player.block_stunned:
            if random.random() < 0.8:  
                self.counter_attack()
            return

        if self.opponent.is_attacking and self.opponent.hitbox:
            if self.opponent.hitbox.colliderect(self.player.hurtbox):
                if random.random() < 0.85: 
                    self.defend()
                else:
                    self.counter_attack()
                return
            elif abs_distance < self.normal_attack_range and random.random() < 0.7:
                self.counter_attack()  
                return

        if abs_distance > self.normal_attack_range + self.range_inaccuracy:
            self.move_toward_opponent(distance)  
        elif abs_distance > self.crouch_attack_range:
            if random.random() < 0.9: 
                self.attack()
            else:
                self.move_toward_opponent(distance) 
        else:  
            if random.random() < 0.95:
                self.attack()
            else:
                self.defend()  


        if not self.opponent.on_ground and random.random() < 0.8:  
            self.jump_to_approach(screen)
            self.attack()
        elif self.opponent.hit_stunned or self.opponent.block_stunned:
            self.attack()  

    def move_toward_opponent(self, distance):
        if not self.player.is_attacking and not self.player.jumpsquatting and not self.player.hit_stunned and not self.player.block_stunned:
            self.player.v_x = SPEED if distance < 0 else -SPEED
            if self.player.on_ground:
                self.player.update_action(ACTIONS['WALK'] if self.player.direction == 1 else ACTIONS['WALKBACK'])
        else:
            self.player.v_x = 0  # Reset vận tốc nếu không thể di chuyển

    def move_away_from_opponent(self, distance):
        if not self.player.is_attacking and not self.player.jumpsquatting and not self.player.hit_stunned and not self.player.block_stunned:
            self.player.v_x = -SPEED if distance < 0 else SPEED
            if self.player.on_ground:
                self.player.update_action(ACTIONS['WALKBACK'] if self.player.direction == 1 else ACTIONS['WALK'])
        else:
            self.player.v_x = 0

    def can_attack(self):
        return not self.player.is_attacking and not self.player.hit_stunned and not self.player.block_stunned and self.player.on_ground

    def attack(self):
        if not self.can_attack():
            return

        abs_distance = abs(self.player.x - self.opponent.x)
        if abs_distance <= self.crouch_attack_range:
            self.player.is_attacking = True
            self.player.v_x = 0
            self.player.update_action(ACTIONS['CROUCH_ATTACK'])
        elif abs_distance <= self.normal_attack_range:
            self.player.is_attacking = True
            self.player.v_x = 0
            self.player.update_action(ACTIONS['ATTACK'])

    def counter_attack(self):
        if self.can_attack():
            abs_distance = abs(self.player.x - self.opponent.x)
            if abs_distance <= self.crouch_attack_range:
                self.player.is_attacking = True
                self.player.v_x = 0
                self.player.update_action(ACTIONS['CROUCH_ATTACK'])
            elif abs_distance <= self.normal_attack_range * 1.2:  # Tăng tầm phản công
                self.player.is_attacking = True
                self.player.v_x = 0
                self.player.update_action(ACTIONS['ATTACK'])

    def defend(self):
        if self.player.on_ground and not self.player.jumpsquatting and not self.player.guard_broken:
            self.player.is_sitting = True
            self.player.v_x = 0
            self.player.update_action(ACTIONS['CROUCH'])

    def jump_to_approach(self, screen):
        if self.player.on_ground and not self.player.jumpsquatting:
            self.player.jumpsquatting = True
            self.player.jumpsquatframes = 0
            self.player.update_action(ACTIONS['JUMPSQUAT'])
