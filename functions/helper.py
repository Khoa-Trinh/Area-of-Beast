def minmax(value: float, min_max_tuple: tuple[float]):
    return min(max(value, min_max_tuple[0]), min_max_tuple[1])
