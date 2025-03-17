import pygame as py

# Hằng số từ Godot
SPEED = 75
JUMP_POWER = -230
DOUBLE_JUMP_POWER = -200
FALL_SPEED = 11
PERSONALJUMPSQUATFRAMES = 6  # 6 frame ở 60 FPS = 100 ms
MAXHP = 130

class Player:
    def __init__(self, position: tuple[int, int], player: int, sprite_sheet, animation_steps):
        # Cài đặt cơ bản
        self.x = position[0]
        self.y = position[1]
        self.player = player
        self.health = MAXHP
        self.direction = 1 if self.player == 1 else -1  # Hướng mặc định
        self.flip = False  # Lật hình ảnh

        # Trạng thái nhân vật
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = True
        self.jumpsquatting = False
        self.jumpsquatframes = 0
        self.doublejumps = 1
        self.is_sitting = False
        self.attacking = False

        # Animation
        self.size = 64  # Kích thước mỗi frame trong sprite sheet (giả định)
        self.image_scale = 2  # Tỷ lệ phóng to hình ảnh
        self.offset = (0, 0)  # Offset để căn chỉnh hình ảnh
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0  # 0: idle, 1: walk, 2: jumpsquat, 3: jump, 4: fall, 5: crouch
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = py.time.get_ticks()
        self.rect = py.Rect(self.x, self.y, 80, 180)  # Hitbox nhân vật

    def load_images(self, sprite_sheet, animation_steps):
        """Tải hình ảnh từ sprite sheet giống Fighter"""
        animation_list = []
        for y, steps in enumerate(animation_steps):
            temp_img_list = []
            for x in range(steps):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                scaled_img = py.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale))
                temp_img_list.append(scaled_img)
            animation_list.append(temp_img_list)
        return animation_list

    def update_action(self, new_action):
        """Cập nhật hành động và reset frame"""
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = py.time.get_ticks()

    def update_animation(self, fps):
        """Cập nhật animation dựa trên FPS thực tế"""
        # Tính animation_cooldown động dựa trên số frame và thời gian mong muốn
        if self.action == 2:  # jumpsquat
            total_time = PERSONALJUMPSQUATFRAMES / 60 * 1000  # 100 ms ở 60 FPS
            animation_cooldown = total_time / len(self.animation_list[self.action])
        else:  # Các hành động khác (idle, walk, jump, fall, crouch)
            animation_cooldown = 1000 / 20  # Mặc định 20 FPS (50 ms mỗi frame)

        # Cập nhật frame
        if py.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = py.time.get_ticks()
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0
                if self.action == 2:  # Khi jumpsquat hoàn tất
                    self.jump()

        self.image = self.animation_list[self.action][self.frame_index]

    def movement(self, screen: py.Surface, key: py.key.ScancodeWrapper, fps: int):
        """Xử lý di chuyển, nhảy, ngồi"""
        width_limit = (0, screen.get_width() - self.rect.width)
        height_limit = (0, screen.get_height() - self.rect.height)
        ground_level = screen.get_height() - 110  # Mức mặt đất

        # Input
        lpress = key[py.K_LEFT] if self.player == 2 else key[py.K_a]
        rpress = key[py.K_RIGHT] if self.player == 2 else key[py.K_d]
        upress = key[py.K_UP] if self.player == 2 else key[py.K_w]
        dpress = key[py.K_DOWN] if self.player == 2 else key[py.K_s]

        # Di chuyển trái/phải
        if lpress and not rpress and not self.is_sitting and self.on_ground and not self.jumpsquatting:
            self.velocity_x = -SPEED
            self.update_action(1)  # walk
            self.flip = True
        elif rpress and not lpress and not self.is_sitting and self.on_ground and not self.jumpsquatting:
            self.velocity_x = SPEED
            self.update_action(1)  # walk
            self.flip = False
        else:
            if self.on_ground and not self.is_sitting and not self.jumpsquatting:
                self.velocity_x = self.velocity_x * 0.6  # Ma sát
                if abs(self.velocity_x) < 0.2:
                    self.velocity_x = 0
                self.update_action(0)  # idle

        # Ngồi
        if dpress and self.on_ground and not self.jumpsquatting:
            self.is_sitting = True
            self.velocity_x = 0
            self.update_action(5)  # crouch
        else:
            self.is_sitting = False

        # Nhảy
        if upress and self.on_ground and not self.jumpsquatting and not self.is_sitting:
            self.jumpsquatting = True
            self.jumpsquatframes = 0
            self.update_action(2)  # jumpsquat

        # Xử lý jumpsquat
        if self.jumpsquatting:
            self.jumpsquatframes += 1
            if self.jumpsquatframes >= PERSONALJUMPSQUATFRAMES:
                self.jump()

        # Nhảy đôi
        if upress and not self.on_ground and self.doublejumps > 0:
            self.velocity_y = DOUBLE_JUMP_POWER
            self.doublejumps -= 1
            self.update_action(3)  # jump

        # Áp dụng trọng lực
        self.velocity_y += FALL_SPEED
        self.y += self.velocity_y / fps * 10  # Điều chỉnh dựa trên FPS
        self.x += self.velocity_x / fps * 10

        # Giới hạn vị trí
        if self.x < width_limit[0]:
            self.x = width_limit[0]
            self.velocity_x = 0
        if self.x > width_limit[1]:
            self.x = width_limit[1]
            self.velocity_x = 0
        if self.y > ground_level:
            self.y = ground_level
            self.velocity_y = 0
            self.on_ground = True
            self.doublejumps = 1
            if not self.is_sitting and not self.jumpsquatting:
                self.update_action(0)  # idle
        else:
            self.on_ground = False
            self.update_action(4 if self.velocity_y > 0 else 3)  # fall hoặc jump

        self.rect.topleft = (self.x, self.y)

    def jump(self):
        """Thực hiện nhảy cơ bản"""
        self.velocity_y = JUMP_POWER
        self.jumpsquatting = False
        self.jumpsquatframes = 0
        self.on_ground = False
        self.update_action(3)  # jump

    def draw(self, screen: py.Surface):
        """Vẽ nhân vật"""
        img = py.transform.flip(self.image, self.flip, False)
        screen.blit(img, (self.rect.x - self.offset[0] * self.image_scale, self.rect.y - self.offset[1] * self.image_scale))

    def update(self, screen: py.Surface, fps: int):
        """Cập nhật trạng thái"""
        key = py.key.get_pressed()
        self.movement(screen, key, fps)
        self.update_animation(fps)

# Ví dụ sử dụng
if __name__ == "__main__":
    py.init()
    screen = py.display.set_mode((640, 480))
    clock = py.time.Clock()

    # Giả lập sprite sheet (thay bằng asset thật của bạn)
    sprite_sheet = py.Surface((256, 384)).convert_alpha()  # 4x6 grid, 64x64 mỗi frame
    animation_steps = [4, 4, 4, 4, 4, 4]  # 6 hành động: idle, walk, jumpsquat, jump, fall, crouch
    player1 = Player((100, 370), 1, sprite_sheet, animation_steps)

    running = True
    while running:
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False

        fps = max(1, int(clock.get_fps()))
        screen.fill((255, 255, 255))
        player1.update(screen, fps)
        player1.draw(screen)
        py.display.flip()
        clock.tick(120)  # Chạy ở 120 FPS

    py.quit()