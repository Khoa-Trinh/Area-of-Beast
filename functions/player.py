import pygame as pygame
from components.damage_counter import DamageCounter
from functions.helper import minmax, approach_angle, get_box


class Player:
    def __init__(
        self,
        position: tuple[int, int],
        clock: py.time.Clock,
        player: int,
        character: int,
        health: int
    ):
        # Player settings
        self.x = position[0]
        self.y = position[1]
        self.height = size[0]#constant
        self.width = size[1]#constant
        self.clock = clock
        self.player = player
        self.health = health
        self.direction = 1 if self.player == 1 else 0
        self.action = 0  # 0: idle, 1: walk, 2: jumpsquat, 3: jump, 4: fall, 5: crouch
         # Animation
        self.size = 64  # Kích thước mỗi frame trong sprite sheet (giả định)
        self.image_scale = 2  # Tỷ lệ phóng to hình ảnh
        self.offset = (0, 0)  # Offset để căn chỉnh hình ảnh
        sprite_sheet = py.image.load("assets/characters/character.png").convert_alpha()
        animation_steps = [4,4,4,4]
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0  # 0: idle, 1: crouch, 2: walk, 3: jumpsquat,4: jump, 5: crouch
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = py.time.get_ticks()

        # Player damage counter
        self.damage_counter = DamageCounter(position, size)

    def load_images(self, sprite_sheet, animation_steps,rc: tuple[int,int]):
        animation_list = []
        target_size = (64, 68)
        for y, steps in enumerate(animation_steps):
            temp_img_list = []
            for x in range(steps):
                frame_width = sprite_sheet.get_width() // rc[0]
                frame_height = sprite_sheet.get_height() // rc[1]
                temp_img = sprite_sheet.subsurface(x * frame_width, y * frame_height, frame_width, frame_height)
                scaled_img = py.transform.scale(temp_img, target_size)
                temp_img_list.append(scaled_img)
            animation_list.append(temp_img_list)
        return animation_list
    def hurt_box(self):
        return get_box((self.x, self.y), (self.width, self.height), 4)
    def attack_hitbox(self):
        if self.direction == 0:
            return py.Rect(
                self.rect.
            )
    def lose_health(self, damage: int):
        self.health = max(0, self.health - damage)
        self.damage_counter.trigger(damage)

    def draw(self, screen: py.Surface):
        self.damage_counter.draw(screen, self.x, self.y)
        py.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def action(self, screen: py.Surface):
        key = py.key.get_pressed()
        fps = max(1, int(self.clock.get_fps()))
        self.movement(screen, key, fps)
        self.skill(screen, key, fps)

    def handle_input(self,key: py.key.ScancodeWrapper):
        if key[py.K_s] and self.is_jumping == False and self.is_attacking == False:
            self.is_sitting = True
            
    def movement(self, screen: py.Surface, key: py.key.ScancodeWrapper, fps: int):
        width_limit = (0, screen.get_width() - self.width)
        height_limit = (0, screen.get_height() - self.height)
    def jumping
        
    def draw(self, screen: py.Surface):
        self.damage_counter.draw(screen, self.x, self.y)
        py.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    # def skill(self, screen: py.Surface, key: py.key.ScancodeWrapper, fps: int):
    #     # Variables
    #     width_limit = (0, screen.get_width() - self.width)
    #     height_limit = (0, screen.get_height() - self.height)
    #     current_time = py.time.get_ticks()

    #     skill_keys = {
    #         "wasd": (py.K_c, py.K_v),
    #         "arrow": (py.K_COMMA, py.K_PERIOD),
    #     }

    #     if self.move in skill_keys:
    #         keys = skill_keys[self.move]
    #         skills = [self.skill1, self.skill2]
    #         speeds = [fps / skill.skill_speed for skill in skills]

    #     for i, skill in enumerate(skills):
    #         key_code = keys[i]
    #         speed = speeds[i]
    #         self.cooldown_percent[i] = min(
    #             1, (current_time - skill.skill_last) / skill.skill_cooldown
    #         )

    #         if (
    #             key[key_code]
    #             and current_time - skill.skill_last >= skill.skill_cooldown
    #             and self.can_use_skill
    #             and skill.skill_repeat_times == 0
    #         ):
    #             skill.skill_repeat_times = speed
    #             skill.reset()

    #         if skill.skill_repeat_times > 0:
    #             self.x, self.y, stop = skill.action(
    #                 self.x,
    #                 self.y,
    #                 self.direction,
    #                 skill.skill_distance,
    #                 speed,
    #                 speed - skill.skill_repeat_times if i == 1 else 0,
    #                 (width_limit, height_limit),
    #             )
    #             self.draw(screen)
    #             skill.skill_activate = True
    #             skill.skill_last = current_time
    #             skill.skill_repeat_times = max(
    #                 0, skill.skill_repeat_times - 1 if not stop else 0
    #             )
    #         if skill.skill_repeat_times == 0:
    #             skill.skill_activate = False

    #         self.can_move = all(skill.skill_repeat_times == 0 for skill in skills)
    #         self.can_use_skill = self.can_move
