# FILE:/arena-of-beasts/arena-of-beasts/src/ui/menu.py

import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font('assets/fonts/game_font.ttf', 48)
        self.title = self.font.render('Arena of Beasts', True, (255, 255, 255))
        self.start_text = self.font.render('Press Enter to Start', True, (255, 255, 255))
        self.quit_text = self.font.render('Press Q to Quit', True, (255, 255, 255))
        self.running = True

    def display_menu(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.title, (self.screen.get_width() // 2 - self.title.get_width() // 2, 100))
            self.screen.blit(self.start_text, (self.screen.get_width() // 2 - self.start_text.get_width() // 2, 300))
            self.screen.blit(self.quit_text, (self.screen.get_width() // 2 - self.quit_text.get_width() // 2, 400))
            pygame.display.flip()
            self.handle_events()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.start_game()
                if event.key == pygame.K_q:
                    self.running = False

    def start_game(self):
        self.running = False
        # Here you would typically transition to the game state
        # For example, you could return a game object or state to start the game.