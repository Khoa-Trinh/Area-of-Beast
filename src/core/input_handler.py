import pygame

class InputHandler:
    def __init__(self):
        self.keys = {
            'player1': {
                'left': False,
                'right': False,
                'jump': False,
                'attack': False,
                'sit': False,
                'dash': False,
                'parry': False
            },
            'player2': {
                'left': False,
                'right': False,
                'jump': False,
                'attack': False,
                'sit': False,
                'dash': False,
                'parry': False
            }
        }

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.keys['player1']['left'] = True
                if event.key == pygame.K_d:
                    self.keys['player1']['right'] = True
                if event.key == pygame.K_w:  # Jump
                    self.keys['player1']['jump'] = True
                if event.key == pygame.K_SPACE:  # Attack
                    self.keys['player1']['attack'] = True
                if event.key == pygame.K_s:  # Sit
                    self.keys['player1']['sit'] = True

                if event.key == pygame.K_LEFT:
                    self.keys['player2']['left'] = True
                if event.key == pygame.K_RIGHT:
                    self.keys['player2']['right'] = True
                if event.key == pygame.K_UP:  # Jump
                    self.keys['player2']['jump'] = True
                if event.key == pygame.K_RETURN:
                    self.keys['player2']['attack'] = True
                if event.key == pygame.K_DOWN:  # Sit
                    self.keys['player2']['sit'] = True
                if event.key == pygame.K_RSHIFT:  # Dash
                    self.keys['player2']['dash'] = True
                if event.key == pygame.K_p:  # Parry
                    self.keys['player2']['parry'] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.keys['player1']['left'] = False
                if event.key == pygame.K_d:
                    self.keys['player1']['right'] = False
                if event.key == pygame.K_w:
                    self.keys['player1']['jump'] = False
                if event.key == pygame.K_SPACE:
                    self.keys['player1']['attack'] = False
                if event.key == pygame.K_s:
                    self.keys['player1']['sit'] = False

                if event.key == pygame.K_LEFT:
                    self.keys['player2']['left'] = False
                if event.key == pygame.K_RIGHT:
                    self.keys['player2']['right'] = False
                if event.key == pygame.K_UP:
                    self.keys['player2']['jump'] = False
                if event.key == pygame.K_RETURN:
                    self.keys['player2']['attack'] = False
                if event.key == pygame.K_DOWN:
                    self.keys['player2']['sit'] = False
    def get_keys(self):
        return self.keys