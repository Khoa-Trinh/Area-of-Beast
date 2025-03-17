def move(self, direction):
    current_i = self.buttons.index(self.active_button)
    for btn in self.buttons:
        btn.deactivate()
    new_i = (current_i + direction) % len(self.buttons)
    self.active_button = self.buttons[new_i]
    self.active_button.activate()
