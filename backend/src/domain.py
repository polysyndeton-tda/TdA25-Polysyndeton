from dataclasses import dataclass
from collections import namedtuple
from typing import List
from uuid import uuid4
from enum import Enum

class Symbols(Enum):
    CROSSES = "X"
    NOUGHTS = "O"


Point = namedtuple("Point", ['x', 'y'])

@dataclass
class Match:
    room_name: str
    board: List[List[str]]
    player1_time: int
    player2_time: int
    player1_uuid: str
    player2_uuid: str

@dataclass
class Move:
    player_uuid: str
    move: Point
    symbol: Symbols
