from functions.helpers.move import move
from functions.helpers.lock_in import lock_in
from components.button import Button
from constants.characters import text_character, text


def create_buttons(self, positions, side):
    return [
        Button(
            pos,
            text,
            lambda: lock_in(self, side),
            lambda: move(self, -1, side),
            lambda: move(self, 1, side),
            boxtext,
            side,
        )
        for pos, text, boxtext in zip(positions, text, text_character)
    ]
