# import pygame as py


# def wait_then_execute(delay, action):
#     start_time = py.time.get_ticks()

#     def check():
#         if py.time.get_ticks() - start_time >= delay:
#             action()
#             return True
#         return False

#     return check


def minmax(value: float, min_max_tuple: tuple[float]):
    return min(max(value, min_max_tuple[0]), min_max_tuple[1])
