from typing import List, Tuple, Literal
from collections import deque

# Domino Game imlpementation, for now just making a simple functional domino game

# TODO today:
#  - Board representation  

Tile = Tuple[int, int]
Side = Literal["L", "R"]

# Helpers
def make_set_double6() -> List[Tile]:
    # Unordered tiles: (a, b) where 0 <= a <= b <= 6
    return [(a, b) for a in range(7) for b in range(a, 7)]

def flip(t: Tile) -> Tile:
    return (t[1], t[0])

# Used to hold info about the player and hand
class Player:
    name: str
    team: int
    hand: list[Tile]

# TODO: placing a piece, checking for an empty list
class Board:
    chain: deque = field(default_factory=deque)
    left_end: Optional[int] = None
    right_end: Optional[int] = None

    def is_empty(self) -> bool:
        return len(self.chain) == 0




# TODO: Track games
class Game:
    


def main():
    #Setting plyers
    players: list[Player] = []
    for i in range(4):
        p = Player()
        p.name = f"Player {i + 1}"
        p.team = 0 if i < 2 else 1
        p.hand = []
        players.append(p)

    #Setting Board
    

if __name__ == "__main__":
    main()