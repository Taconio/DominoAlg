from typing import Protocol, List, Tuple, Literal, Optional
from collections import deque
from dataclasses import dataclass, field
import random

# Domino Game imlpementation, for now just making a simple functional domino game

# TODO today:
#  - Implement heuristic for choosing moves  

# Tile data types
Tile = Tuple[int, int]
Side = Literal["L", "R"]
Move = Tuple[Tile, Side, Tile]

# Helpers
def make_set_double6() -> List[Tile]:
    # Unordered tiles: (a, b) where 0 <= a <= b <= 6
    return [(a, b) for a in range(7) for b in range(a, 7)]

def flip(t: Tile) -> Tile:
    return (t[1], t[0])

def pip_sum(t: Tile) -> int:
    return t[0] + t[1]

# Heuristic functions
class Heuristic(Protocol):
    def choose_move(self, player: "Player", board: "Board", legal_moves: List[Move]) -> Move: ...

@dataclass(frozen=True)
class FirstLegalHeuristic:
    def choose_move(self, player: "Player", board: "Board", legal_moves: List[Move]) -> Move:
        return legal_moves[0]

@dataclass(frozen=True)
class RandomHeuristic:
    rng: random.Random = field(default_factory=random.Random)

    def choose_move(self, player: "Player", board: "Board", legal_moves: List[Move]) -> Move:
        return self.rng.choice(legal_moves)

@dataclass(frozen=True)
class MaxPipSumHeuristic:
    def choose_move(self, player: "Player", board: "Board", legal_moves: List[Move]) -> Move:
        # pick the move whose original tile has highest pip sum
        return max(legal_moves, key=lambda m: pip_sum(m[0]))

# Used to hold info about the player and hand
@dataclass
class Player:
    name: str
    team: int
    hand: list[Tile]
    heuristic: Heuristic = field(default_factory=FirstLegalHeuristic)

# TODO: placing a piece, checking for an empty list
@dataclass
class Board:
    chain: deque = field(default_factory=deque)
    left_end: Optional[int] = None
    right_end: Optional[int] = None

    def is_empty(self) -> bool:
        return len(self.chain) == 0
    
    def legal_moves(self, hand: list[Tile]) -> List[Tuple[Tile, Side, Tile]]:
        moves = []
        
        if self.is_empty():
            # any tile can start; oriented arbitrarily
            for t in hand:
                moves.append((t, "L", t))
            return moves

        for t in hand:
            a, b = t
            # try left
            if a == self.left_end:
                moves.append((t, "L", flip(t)))
            elif b == self.left_end:
                moves.append((t, "L", t))

            # try right
            if a == self.right_end:
                moves.append((t, "R", t))
            elif b == self.right_end:
                moves.append((t, "R", flip(t)))
        return moves
    
    def place(self, oriented_tile: Tile, side: Side) -> None:
        a, b = oriented_tile
        
        #TODO start with player that has the double 6 tile if game 1
        if (self.is_empty()):
            self.chain.append(oriented_tile)
            self.left_end, self.right_end = a, b
            return
        
        if side == "L":
            if b != self.left_end:
                raise ValueError("Tile does not match left end")
            self.chain.appendleft(oriented_tile)
            self.left_end = a
                
        elif side == "R":
            if a != self.right_end:
                raise ValueError("Tile does not match right end")
            self.chain.append(oriented_tile)
            self.right_end = b
        
        return

# GM class, keep game info
@dataclass
class DominoGame:
    
    players: list[Player]
    board: Board = field(default_factory=Board)
    turn: int = 0
    consecutive_passes: int = 0
    
    def deal(self) -> None:
        tiles = make_set_double6()
        random.shuffle(tiles)
        for i, p in enumerate(self.players):
            p.hand = tiles[i*7:(i+1)*7]
            
        return
    
    def choose_first_player(self) -> int:
        # Find player with the double six
        for i, p in enumerate(self.players):
            if (6, 6) in p.hand:
                return i
        return 0  # Fallback, should not happen in standard dominoes
    
    def team_pip_total(self, team_id: int) -> int:
        return sum(pip_sum(t) for pl in self.players if pl.team == team_id for t in pl.hand)
    
    def check_end_conditions(self) -> Optional[int]:
        for pl in self.players:
            if len(pl.hand) == 0:
                return pl.team

        if self.consecutive_passes >= len(self.players):
            t0 = self.team_pip_total(0)
            t1 = self.team_pip_total(1)
            if t0 < t1:
                return 0
            if t1 < t0:
                return 1
            return -1  # tie
        return None
    
    def play_turn(self) -> None:
        pl = self.players[self.turn]
        legal_moves: List[Move] = self.board.legal_moves(pl.hand)

        if not legal_moves:
            self.consecutive_passes += 1
            self.turn = (self.turn + 1) % len(self.players)
            return

        original, side, oriented_tile = pl.heuristic.choose_move(pl, self.board, legal_moves)
        self.board.place(oriented_tile, side)
        pl.hand.remove(original)
        self.consecutive_passes = 0
        self.turn = (self.turn + 1) % len(self.players)

def main():
    #Setting plyers
    players: list[Player] = [
        Player(name="Player 1", team=0, heuristic=FirstLegalHeuristic()),
        Player(name="Player 2", team=0, heuristic=FirstLegalHeuristic()),
        Player(name="Player 3", team=1, heuristic=FirstLegalHeuristic()),
        Player(name="Player 4", team=1, heuristic=FirstLegalHeuristic()),
    ]

    #Setting Board
    GM = DominoGame(players=players)
    GM.deal()
    GM.turn = GM.choose_first_player()
    
    winner = None
    while winner is None:
        GM.play_turn()
        print(f"player: {GM.players[GM.turn].name}, board: {list(GM.board.chain)}")
        winner = GM.check_end_conditions()
        
    if winner == -1:
        print("The game is a tie!")
    else:
        print(f"Team {winner} wins! Total Pips: {GM.team_pip_total(winner)} ")

if __name__ == "__main__":
    main()