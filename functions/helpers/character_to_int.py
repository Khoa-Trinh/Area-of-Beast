def match_character(character: str):
    character_dict = {
        "sword_man": 0,
        "archer": 1,
        "wizard": 2,
        "assassin": 3,
        "tank": 4,
        "witch": 5,
        "ninja": 6,
        "spammer": 7,
        "chill_guy": 8,
        "sigma_boy": 9,
    }
    return character_dict.get(character.lower(), None)
