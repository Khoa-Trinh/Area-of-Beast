import pygame
import sys
from src.scenes.main_menu import MainMenu
from src.scenes.character_select import CharacterSelect
from src.scenes.game_scene import GameScene

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("2D Fighting Game")
        self.clock = pygame.time.Clock()
        self.current_scene = MainMenu(self)

    def change_scene(self, scene):
        self.current_scene = scene

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.current_scene.update()
            self.current_scene.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()