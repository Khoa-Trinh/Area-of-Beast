class Player:
    def __init__(self, character_sprites):
        self.character_sprites = character_sprites
        self.state = 'idle'  # idle, moving, attacking
        self.position = [100, 100]  # Starting position
        self.speed = 5

    def move(self, direction):
        if direction == 'left':
            self.position[0] -= self.speed
            self.state = 'moving'
        elif direction == 'right':
            self.position[0] += self.speed
            self.state = 'moving'
        else:
            self.state = 'idle'

    def attack(self):
        self.state = 'attacking'

    def update(self):
        # Update the player's sprite based on the current state
        if self.state == 'idle':
            return self.character_sprites['idle']
        elif self.state == 'moving':
            return self.character_sprites['move']
        elif self.state == 'attacking':
            return self.character_sprites['attack']

    def reset(self):
        self.state = 'idle'
        self.position = [100, 100]  # Reset to starting position