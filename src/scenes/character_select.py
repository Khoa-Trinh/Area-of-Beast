class CharacterSelect:
    def __init__(self, screen):
        self.screen = screen
        self.characters = ['character1', 'character2']
        self.selected_character = 0
        self.background_image = pygame.image.load('assets/menus/character_select.png')

    def display(self):
        self.screen.blit(self.background_image, (0, 0))
        for index, character in enumerate(self.characters):
            color = (255, 0, 0) if index == self.selected_character else (255, 255, 255)
            font = pygame.font.Font(None, 74)
            text = font.render(character, True, color)
            self.screen.blit(text, (100, 100 + index * 100))

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_character = (self.selected_character - 1) % len(self.characters)
            elif event.key == pygame.K_DOWN:
                self.selected_character = (self.selected_character + 1) % len(self.characters)
            elif event.key == pygame.K_RETURN:
                return self.characters[self.selected_character]
        return None

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                selected = self.handle_input(event)
                if selected:
                    return selected

            self.display()
            pygame.display.flip()