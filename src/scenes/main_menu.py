class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load('assets/menus/main_menu.png')
        self.font = pygame.font.Font(None, 74)
        self.title = self.font.render('2D Fighting Game', True, (255, 255, 255))
        self.start_text = self.font.render('Press Enter to Start', True, (255, 255, 255))
        self.running = True

    def display(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.start_game()

            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.title, (100, 100))
            self.screen.blit(self.start_text, (150, 300))
            pygame.display.flip()

    def start_game(self):
        self.running = False
        # Transition to the character selection scene or game scene here.