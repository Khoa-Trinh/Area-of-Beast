import re

def minmax(value: float, min_max_tuple: tuple[float]):
    return min(max(value, min_max_tuple[0]), min_max_tuple[1])

def capitalize(text: str):
    first = text[0].upper() + text[1:]
    second = re.sub(r'_(\w)', lambda match: ' ' + match.group(1).upper(), first)
    return second
