# FILE:/arena-of-beasts/arena-of-beasts/src/ui/hud.py

import pygame

class HUD:
    def __init__(self, screen, player_health, opponent_health):
        self.screen = screen
        self.player_health = player_health
        self.opponent_health = opponent_health
        self.font = pygame.font.Font('assets/fonts/game_font.ttf', 24)

    def draw(self):
        self.draw_health_bars()
        self.draw_scores()

    def draw_health_bars(self):
        player_health_bar = pygame.Rect(10, 10, 200, 20)
        opponent_health_bar = pygame.Rect(10, 40, 200, 20)

        # Draw player health bar
        pygame.draw.rect(self.screen, (255, 0, 0), player_health_bar)
        pygame.draw.rect(self.screen, (0, 255, 0), (10, 10, 200 * (self.player_health / 100), 20))

        # Draw opponent health bar
        pygame.draw.rect(self.screen, (255, 0, 0), opponent_health_bar)
        pygame.draw.rect(self.screen, (0, 255, 0), (10, 40, 200 * (self.opponent_health / 100), 20))

    def draw_scores(self):
        player_score_text = self.font.render(f'Score: {self.player_health}', True, (255, 255, 255))
        opponent_score_text = self.font.render(f'Score: {self.opponent_health}', True, (255, 255, 255))

        self.screen.blit(player_score_text, (10, 70))
        self.screen.blit(opponent_score_text, (10, 100))