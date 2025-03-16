import pygame as py
import re

from constants.index import text_character


def minmax(value: float, min_max_tuple: tuple[float]):
    return min(max(value, min_max_tuple[0]), min_max_tuple[1])


def capitalize(text: str):
    first = text[0].upper() + text[1:]
    second = re.sub(r"_(\w)", lambda match: " " + match.group(1).upper(), first)
    return second


def match_case_character(character: str):
    match character:
        case "sword_man":
            return 0
        case "archer":
            return 1
        case "wizard":
            return 2
        case "assassin":
            return 3
        case "tank":
            return 4
        case "witch":
            return 5
        case "ninja":
            return 6
        case "spammer":
            return 7
        case "chill_guy":
            return 8
        case "sigma_boy":
            return 9
        case _:
            return False


def get_skills(character: str):
    for cha in text_character:
        if cha[0] == character:
            return cha[2], cha[3]
    return None, None


def approach_angle(current: float, target: float, step: float) -> float:
    diff = (target - current + 180) % 360 - 180
    if diff > 0:
        current += min(step, diff)
    elif diff < 0:
        current -= min(step, -diff)
    return current % 360


def get_box(
    position: tuple[int, int],
    size: tuple[int, int],
    num: int,
    screen: py.Surface = None,
    color: tuple[int, int, int] = None,
):
    rect_size = (size[0] * num, size[1] * num)
    rect = py.Rect(
        position[0] - (rect_size[0] - size[0]) / 2,
        position[1] - (rect_size[1] - size[1]) / 2,
        rect_size[0],
        rect_size[1],
    )
    if screen is not None and color is not None:
        py.draw.rect(screen, color, rect, 1)
    return rect
