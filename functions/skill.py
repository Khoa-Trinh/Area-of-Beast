import pygame as py


class Skill1:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.current_step = 0  # Track the current step
        self.last_step_time = 0  # Track when the last step happened
        self.step_delay = 50

    def action(self, screen: py.Surface, x, y):
        current_time = py.time.get_ticks()
        if current_time - self.last_step_time >= self.step_delay:
            self.current_step += 1  # Move to the next step
            self.last_step_time = current_time  # Reset the timer

            # Define step functions
            step_functions = {1: self.step_1, 2: self.step_2, 3: self.step_1}
            step_function = step_functions.get(self.current_step, None)

            # If a valid step exists, execute it
            if step_function:
                return step_function(screen, x, y)
            else:
                self.current_step = 0  # Reset step sequence after the last step

        return x, y

    def step_1(self, screen: py.Surface, x, y):
        x = max(0, min(x + 5, screen.get_width() - self.width))
        y = max(0, min(y + 50, screen.get_height() - self.height))
        return x, y

    def step_2(self, screen: py.Surface, x, y):
        x = max(0, min(x + 5, screen.get_width() - self.width))
        y = max(0, min(y - 100, screen.get_height() - self.height))
        return x, y
