# FILE:/arena-of-beasts/arena-of-beasts/src/ui/hud.pyf
from utils.constants import *
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT
import pygame

class HUD:
    def __init__(self, screen, P1_health, P2_health,P1_score,P2_score):
        self.screen = screen
        self.P1_health = P1_health
        self.P2_health = P2_health
        self.P1_score = P1_score
        self.P2_score = P2_score
        self.font = pygame.font.Font('assets/fonts/game_font.ttf', 24)
        

    def draw_score(self):
        P1_img = self.font.render(f"P1: {self.P1_score}", True, RED)
        self.screen.blit(P1_img, (20, 20))
        P2_img = self.font.render(f"P2: {self.P2_score}", True, RED)
        self.screen.blit(P2_img, (SCREEN_WIDTH - 320, 20))

    def draw(self):
        self.draw_score()
        self.draw_health_bars()

    def draw_health_bars(self):
        P1_health_bar = pygame.Rect(20, 50, 300, 20)
        P2_health_bar = pygame.Rect(1920-320, 50, 300, 20)

        # Draw player health bar
        pygame.draw.rect(self.screen, RED , P1_health_bar)
        pygame.draw.rect(self.screen, GREEN, (20, 50, 300 * (self.P1_health / 100), 20))

        # Draw opponent health bar
        pygame.draw.rect(self.screen, RED, P2_health_bar)
        pygame.draw.rect(self.screen, GREEN, (SCREEN_WIDTH-320, 50, 300 * (self.P2_health / 100), 20))

