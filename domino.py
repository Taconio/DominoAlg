from typing import List, Tuple, Literal


# Domino Game imlpementation, for now just making a simple functional domino game

# TODO:
#  - Tile class, tuple
#  - Player Class
#  - Board 

Tile = Tuple[int, int]
Side = Literal["L", "R"]

def make_set_double6() -> List[Tile]:
    # Unordered tiles: (a, b) where 0 <= a <= b <= 6
    return [(a, b) for a in range(7) for b in range(a, 7)]

# Used to hold info about the player and hand
class Player:
    name: str
    team: int
    hand: list[Tile]


def main():
    

if __name__ == "__main__":
    main()