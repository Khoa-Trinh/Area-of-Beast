import pygame
from assets.characters.character1 import idle, move, attack
from assets.characters.character2 import idle as character2_idle, move as character2_move, attack as character2_attack

class CharacterSelect:
    def __init__(self, screen):
        self.screen = screen
        self.characters = [
            {"name": "Character 1", "sprites": {"idle": idle, "move": move, "attack": attack}},
            {"name": "Character 2", "sprites": {"idle": character2_idle, "move": character2_move, "attack": character2_attack}},
        ]
        self.selected_character = 0

    def draw(self):
        self.screen.fill((0, 0, 0))  # Clear screen
        for index, character in enumerate(self.characters):
            color = (255, 255, 255) if index == self.selected_character else (100, 100, 100)
            text = pygame.font.Font(None, 36).render(character["name"], True, color)
            self.screen.blit(text, (100, 100 + index * 40))

    def select_character(self):
        return self.characters[self.selected_character]

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_character = (self.selected_character - 1) % len(self.characters)
            elif event.key == pygame.K_DOWN:
                self.selected_character = (self.selected_character + 1) % len(self.characters)
            elif event.key == pygame.K_RETURN:
                return self.select_character()