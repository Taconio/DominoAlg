from typing import List, Tuple, Literal, Optional
from collections import deque
from dataclasses import dataclass, field
import random

# Domino Game imlpementation, for now just making a simple functional domino game

# TODO today:
#  - Board representation  

# Tile data types
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
    
    def place(self, oriented_tile: Tile, side: Side) -> None:
        a, b = oriented_tile
        
        #TODO start with player that has the double 6 tile if game 1
        if (self.is_empty()):
            self.chain.append(oriented_tile)
            self.left_end, self.right_end = a, b
            return
        
        
        #TODO implement further rounds
        
        return

# GM class, keep game info
class DominoGame:
    
    players: list[Player]
    board: Board = field(default_factory=Board)
    turn: int = 0
    
    def deal(self) -> None:
        tiles = make_set_double6()
        random.shuffle(tiles)
        for i, p in enumerate(self.players):
            p.hand = tiles[i*7:(i+1)*7]
            
        return
    
    # TODO play a turn        
    def play_turn() -> None :
        return
        
    



# TODO: Track games
# class Game:
    


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