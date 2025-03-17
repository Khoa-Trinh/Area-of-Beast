def lock_in(self, side):
    if side == "left":
        self.can_change_character = (False, self.can_change_character[1])
    else:
        self.can_change_character = (self.can_change_character[0], False)
