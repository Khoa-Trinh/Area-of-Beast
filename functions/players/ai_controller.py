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
BLOCK_METER_DECREMENT = 10
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
        self.player = player  # AI-controlled character
        self.opponent = opponent  # Human player
        self.range_inaccuracy = 20  # Distance tolerance
        self.reaction_frames = 15  # Frames between decisions
        self.frame_counter = 0
        
        # Game plan setup
        self.game_plans = ["FOOTSIES", "ZONING", "RUSHDOWN"]
        self.current_game_plan = random.choice(self.game_plans)
        self.switch_frames = random.randint(100, 300)  # Switch plan every 100-300 frames
        self.optimal_range = 100  # Default, will be set by game plan

    def update(self, screen):
        """Update AI behavior each frame"""
        self.frame_counter += 1
        self.switch_frames -= 1
        
        # Switch game plan when timer runs out
        if self.switch_frames <= 0:
            self.current_game_plan = random.choice(self.game_plans)
            self.switch_frames = random.randint(100, 300)
        
        # Set optimal range based on game plan
        if self.current_game_plan == "FOOTSIES":
            self.optimal_range = 100
        elif self.current_game_plan == "ZONING":
            self.optimal_range = 150
        elif self.current_game_plan == "RUSHDOWN":
            self.optimal_range = 50
        
        distance = self.player.x - self.opponent.x
        abs_distance = abs(distance)

        # Update direction
        if self.player.x < self.opponent.x:
            self.player.direction = 1
        else:
            self.player.direction = -1

        # Decide action periodically
        if self.frame_counter >= self.reaction_frames:
            self.frame_counter = 0
            self.decide_action(abs_distance, distance, screen)

    def decide_action(self, abs_distance, distance, screen):
        """Decide action based on game plan, distance, and opponent state"""
        if self.current_game_plan == "FOOTSIES":
            self.footsies_logic(abs_distance, distance, screen)
        elif self.current_game_plan == "ZONING":
            self.zoning_logic(abs_distance, distance, screen)
        elif self.current_game_plan == "RUSHDOWN":
            self.rushdown_logic(abs_distance, distance, screen)

    def footsies_logic(self, abs_distance, distance, screen):
        """Maintain optimal range and react"""
        if not self.opponent.on_ground:
            if random.random() < 0.5:  # 50% chance to jump
                self.jump_to_approach(screen)
        elif self.opponent.is_attacking and self.opponent.on_ground:
            if random.random() < 0.8:  # 80% chance to block
                self.defend()
            else:
                self.attack()
        else:
            if abs_distance > self.optimal_range + self.range_inaccuracy:
                self.move_toward_opponent(distance)
            elif abs_distance < self.optimal_range - self.range_inaccuracy:
                if random.random() < 0.5:
                    self.move_away_from_opponent(distance)
                else:
                    self.attack()
            else:  # Within optimal range
                if random.random() < 0.3:
                    self.attack()
                else:  # Random small movement
                    if random.random() < 0.5:
                        self.move_toward_opponent(distance)
                    else:
                        self.move_away_from_opponent(distance)

    def zoning_logic(self, abs_distance, distance, screen):
        """Keep distance and attack when in range"""
        if not self.opponent.on_ground:
            if random.random() < 0.3:  # 30% chance to jump
                self.jump_to_approach(screen)
        elif self.opponent.is_attacking and self.opponent.on_ground:
            if random.random() < 0.9:  # 90% chance to block
                self.defend()
            else:
                self.attack()
        else:
            if abs_distance < 100:  # Too close
                self.move_away_from_opponent(distance)
            elif abs_distance < 150:  # Attack range
                self.attack()
            else:  # Beyond 150
                if abs_distance > 200:
                    self.move_toward_opponent(distance)
                elif random.random() < 0.2:  # Small chance to adjust
                    self.move_toward_opponent(distance)
                elif random.random() < 0.4:
                    self.move_away_from_opponent(distance)

    def rushdown_logic(self, abs_distance, distance, screen):
        """Get close and attack aggressively"""
        if not self.opponent.on_ground:
            if random.random() < 0.5:  # 50% chance to jump
                self.jump_to_approach(screen)
        elif self.opponent.is_attacking and self.opponent.on_ground:
            if random.random() < 0.5:  # 50% chance to block
                self.defend()
            else:
                self.attack()
        else:
            if abs_distance > 50:
                self.move_toward_opponent(distance)
            else:
                self.attack()

    def move_toward_opponent(self, distance):
        """Move towards the opponent"""
        if not self.player.is_attacking and not self.player.jumpsquatting:
            if distance > 0:  # Opponent to the right
                self.player.v_x = -SPEED
                if self.player.on_ground:
                    self.player.update_action(ACTIONS['WALKBACK'] if self.player.direction == 1 else ACTIONS['WALK'])
            else:  # Opponent to the left
                self.player.v_x = SPEED
                if self.player.on_ground:
                    self.player.update_action(ACTIONS['WALK'] if self.player.direction == 1 else ACTIONS['WALKBACK'])

    def move_away_from_opponent(self, distance):
        """Move away from the opponent"""
        if not self.player.is_attacking and not self.player.jumpsquatting:
            if distance > 0:  # Opponent to the right
                self.player.v_x = SPEED
                if self.player.on_ground:
                    self.player.update_action(ACTIONS['WALK'] if self.player.direction == 1 else ACTIONS['WALKBACK'])
            else:  # Opponent to the left
                self.player.v_x = -SPEED
                if self.player.on_ground:
                    self.player.update_action(ACTIONS['WALKBACK'] if self.player.direction == 1 else ACTIONS['WALK'])

    def can_attack(self):
        """Check if AI can attack"""
        return not self.player.is_attacking and not self.player.hit_stunned and not self.player.block_stunned

    def attack(self):
        """Perform an attack, choosing between normal and crouch attack"""
        if self.player.on_ground and self.can_attack():
            if abs(self.player.x - self.opponent.x) < 50 and self.opponent.on_ground:
                if random.random() < 0.5:  # 50% chance for crouch attack when close
                    self.player.is_attacking = True
                    self.player.v_x = 0
                    self.player.update_action(ACTIONS['CROUCH_ATTACK'])
                else:
                    self.player.is_attacking = True
                    self.player.v_x = 0
                    self.player.update_action(ACTIONS['ATTACK'])
            else:
                self.player.is_attacking = True
                self.player.v_x = 0
                self.player.update_action(ACTIONS['ATTACK'])

    def defend(self):
        """Defend by crouching"""
        if self.player.on_ground and not self.player.jumpsquatting and not self.player.guard_broken:
            self.player.is_sitting = True
            self.player.v_x = 0
            self.player.update_action(ACTIONS['CROUCH'])

    def jump_to_approach(self, screen):
        """Jump towards the opponent"""
        if self.player.on_ground and not self.player.jumpsquatting:
            self.player.jumpsquatting = True
            self.player.jumpsquatframes = 0
            self.player.update_action(ACTIONS['JUMPSQUAT'])