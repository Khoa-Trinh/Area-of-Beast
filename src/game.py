import pygame
from characters.player import Player
from core.input_handler import InputHandler
from core.collision import handle_collisions
from ui.hud import HUD
from utils.constants import FPS

class Game:
    def __init__(self,screen):
        self.screen = screen
        pygame.display.set_caption("Arena of Beasts")
        self.clock = pygame.time.Clock()
        self.running = True
        self.player1 = Player(100, 300)
        self.player2 = Player(600, 300)
        self.score=[0,0]
        self.input_handler = InputHandler()
        self.hud = HUD(self.screen, self.player1.health, self.player2.health,self.score[0],self.score[1]) 

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

    def handle_events(self):
        self.input_handler.handle_input()
        keys = self.input_handler.get_keys()
        if keys['player1']['left']:
            self.player1.walk(-1)
        if keys['player1']['right']:
            self.player1.walk(1)
        if keys['player1']['jump']:
            self.player1.jump()
        if keys['player1']['attack']:
            self.player1.attack()
        if keys['player1']['sit']:
            self.player1.sit()
        else:
            self.player1.stand()
            
        if keys['player2']['left']:
            self.player2.walk(-1)
        if keys['player2']['right']:
            self.player2.walk(1)
        if keys['player2']['jump']:
            self.player2.jump()
        if keys['player2']['attack']:
            self.player2.attack()
        if keys['player2']['sit']:
            self.player2.sit()
        else:
            self.player2.stand()

    def update(self):
        self.player1.face_direction(self.player2)
        self.player2.face_direction(self.player1)
        self.player1.update()
        self.player2.update()
        handle_collisions(self.player1, self.player2)
        self.hud.P1_health = self.player1.health
        self.hud.P2_health = self.player2.health

    def render(self):
        self.screen.fill((0, 0, 0))  # Clear screen with black
        self.player1.draw(self.screen)
        self.player2.draw(self.screen)
        self.hud.draw()
        pygame.display.flip()

    def start(self):
        pygame.init()
        self.run()
        pygame.quit()