import pygame as py


def wait_then_execute(delay, action):
    start_time = py.time.get_ticks()

    def check():
        if py.time.get_ticks() - start_time >= delay:
            action()
            return True
        return False

    return check
