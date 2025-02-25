class Character:
    def __init__(self, name, idle_image, move_image, attack_image):
        self.name = name
        self.idle_image = idle_image
        self.move_image = move_image
        self.attack_image = attack_image
        self.state = 'idle'
        self.position = (0, 0)

    def update(self):
        if self.state == 'moving':
            self.move()
        elif self.state == 'attacking':
            self.attack()
        else:
            self.idle()

    def move(self):
        # Logic for moving the character
        pass

    def attack(self):
        # Logic for attacking
        pass

    def idle(self):
        # Logic for idle state
        pass

    def set_position(self, x, y):
        self.position = (x, y)

    def get_position(self):
        return self.position

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state