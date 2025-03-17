def move(self, direction, side=None):
    if side is not None:
        buttons = self.button_left if side == "left" else self.button_right
        active_button = (
            self.active_button_left if side == "left" else self.active_button_right
        )
        new_i = (buttons.index(active_button) + direction) % len(buttons)

        if side == "left":
            if self.can_change_character[0]:
                for button in self.button_left:
                    button.deactivate()
                self.active_button_left = buttons[new_i]
                self.active_button_left.activate()
        else:
            if self.can_change_character[1]:
                for button in self.button_right:
                    button.deactivate()
                self.active_button_right = buttons[new_i]
                self.active_button_right.activate()

    else:
        current_i = self.buttons.index(self.active_button)
        for btn in self.buttons:
            btn.deactivate()
        new_i = (current_i + direction) % len(self.buttons)
        self.active_button = self.buttons[new_i]
        self.active_button.activate()
