import pygame

# Khởi tạo Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Scene cơ bản
class Scene:
    def update(self):
        pass

    def render(self, screen):
        pass

    def handle_events(self, events):
        pass

# Scene Menu
class MainMenu(Scene):
    def render(self, screen):
        screen.fill((0, 0, 255))  # Màu xanh dương
        font = pygame.font.Font(None, 36)
        text = font.render("Press ENTER to Start", True, (255, 255, 255))
        screen.blit(text, (300, 250))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return "gameplay"  # Chuyển sang scene game
        return None

# Scene Game
class Gameplay(Scene):
    def render(self, screen):
        screen.fill((0, 255, 0))  # Màu xanh lá
        font = pygame.font.Font(None, 36)
        text = font.render("Playing... Press ESC to Exit", True, (255, 255, 255))
        screen.blit(text, (250, 250))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"  # Quay lại menu
        return None

# Quản lý scene
scenes = {
    "menu": MainMenu(),
    "gameplay": Gameplay(),
}
current_scene = "menu"

# Vòng lặp game
running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    new_scene = scenes[current_scene].handle_events(events)
    if new_scene:
        current_scene = new_scene

    scenes[current_scene].update()
    scenes[current_scene].render(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
