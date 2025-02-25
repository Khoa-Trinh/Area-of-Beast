from pygame import *
import random

class GameScene:
    def __init__(self, screen):
        self.screen = screen
        self.clock = time.Clock()
        self.running = True
        self.background = image.load('assets/backgrounds/stage1.png')
        self.player1 = None  # Placeholder for player 1
        self.player2 = None  # Placeholder for player 2

    def setup(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def handle_events(self):
        for event in event.get():
            if event.type == QUIT:
                self.running = False

    def update(self):
        self.player1.update()
        self.player2.update()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.player1.draw(self.screen)
        self.player2.draw(self.screen)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            display.flip()
            self.clock.tick(60)

    def cleanup(self):
        pass  # Add any cleanup code if necessary