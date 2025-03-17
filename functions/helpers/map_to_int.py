def match_map(map: str):
  map_dict = {
    "city": 0,
    "forest": 1,
    "desert": 2,
    "mountain": 3,
    "lake": 4,
    "cave": 5
  }
  return map_dict.get(map.lower(), None)
