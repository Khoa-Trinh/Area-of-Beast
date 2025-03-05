class AIOpponent(Character):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.health = 100
        self.speed = 5
        self.attack_range = pygame.Rect(x + 50, y, 30, 30)  # Example hitbox
        self.hurtbox = pygame.Rect(x, y, 30, 30)  # Example hurtbox
        self.state = 'idle'  # Possible states: idle, walking, attacking

    def update(self, player_position):
        # Basic AI behavior to move towards the player
        if player_position[0] < self.rect.x:
            self.rect.x -= self.speed
            self.state = 'walking'
        elif player_position[0] > self.rect.x:
            self.rect.x += self.speed
            self.state = 'walking'
        else:
            self.state = 'idle'

        # Check if the AI should attack
        if self.attack_range.colliderect(player_position):
            self.attack()

    def attack(self):
        self.state = 'attacking'
        # Logic for attacking the player
        # Play attack animation and sound
        # Check for collision with player's hurtbox

    def draw(self, screen):
        # Draw the AI opponent based on its state
        if self.state == 'idle':
            # Draw idle sprite
            pass
        elif self.state == 'walking':
            # Draw walking sprite
            pass
        elif self.state == 'attacking':
            # Draw attacking sprite
            pass

    def reset(self):
        self.health = 100
        self.rect.x = initial_x  # Set to initial position
        self.rect.y = initial_y  # Set to initial position
        self.state = 'idle'