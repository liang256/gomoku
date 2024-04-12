from dataclasses import dataclass
from typing import List, Dict, Optional


class OutOfBound(Exception):
    pass


@dataclass(frozen=True)
class Player:
    id: str

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Player):
            return self.id == __value.id
        return False


@dataclass(frozen=True)
class Position:
    row: int
    col: int

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.row}, {self.col})"

    def to_tuple(self):
        return (self.row, self.col)


@dataclass(frozen=True)
class Cell:
    player: Player
    data: dict

    def to_dict(self):
        return {"player": self.player, "data": self.data}


class Board:
    def __init__(self, width, height, win_condition_length) -> None:
        if width <= 0:
            raise ValueError("width must be greater than 1.")
        if height <= 0:
            raise ValueError("height must be greater than 1.")
        if not 0 < win_condition_length <= max(width, height):
            raise ValueError(
                "win_condition_length must be greater than 0 and cannot be greater than the maximum of width and height."
            )
        self.width = width
        self.height = height
        self.win_condition_length = win_condition_length
        self.grid = [[None] * self.width for _ in range(self.height)]

    def mark(
        self, player: Player, position: Position, meta_data: Dict = None
    ) -> bool:
        if not self.can_mark(position):
            return False
        self.grid[position.row][position.col] = Cell(player, meta_data)
        return True

    def get(self, position: Position) -> Optional[Cell]:
        if not self.is_in_bound(position):
            raise OutOfBound(f"({position.to_tuple()}) is out of bound.")
        return self.grid[position.row][position.col]

    def can_mark(self, position: Position) -> bool:
        return self.is_in_bound(position) and self.is_position_empty(position)

    def is_in_bound(self, position: Position) -> bool:
        return 0 <= position.row < self.height and 0 <= position.col < self.width

    def is_position_empty(self, position: Position) -> bool:
        return self.grid[position.row][position.col] is None

    def is_full(self) -> bool:
        return all(all(cell for cell in row) for row in self.grid)

    def _iterate_position_in_direction(self, position: Position, dir_x, dir_y):
        if dir_x not in (-1, 0, 1) or dir_y not in (-1, 0, 1):
            raise ValueError(f"Invalid direction ({dir_x}, {dir_y})")

        yield Position(position.row, position.col)

        for i in range(1, max(self.height, self.width)):
            new_x = position.row + i * dir_x
            new_y = position.col + i * dir_y
            if not self.is_in_bound(Position(new_x, new_y)):
                break
            yield Position(new_x, new_y)

    def get_continuous_cells(self, position: Position) -> List[Position]:
        x, y = position.row, position.col

        if self.is_position_empty(position):
            raise ValueError(f"Board ({x}, {y}) is unoccupied.")

        this_player = self.get(position).player

        def get_same_cells_in_direction(dir_x, dir_y):
            buff = []
            for p in self._iterate_position_in_direction(position, dir_x, dir_y):
                if self.is_position_empty(p) or self.get(p).player != this_player:
                    break
                buff.append(p)
            return buff

        res = set()
        dirs = [(0, 1), (1, 1), (1, 0), (1, -1)]
        for dir_x, dir_y in dirs:
            buff = get_same_cells_in_direction(dir_x, dir_y)
            reverse_buff = get_same_cells_in_direction(-dir_x, -dir_y)
            if len(buff) + len(reverse_buff) - 1 >= self.win_condition_length:
                res.update(set(buff + reverse_buff[1:]))

        return res


class Game:
    def __init__(
        self,
        width: int,
        height: int,
        win_condition_length: int,
        players: List[Player],
    ) -> None:
        if not players:
            raise ValueError("players cannot be empty.")
        self.board = Board(width, height, win_condition_length)
        self.players = tuple(players)
        self.curr_player_idx = 0
        self.winner = None

    @property
    def curr_player(self):
        return self.players[self.curr_player_idx]

    def rotate_player(self) -> Player:
        self.curr_player_idx = (self.curr_player_idx + 1) % len(self.players)
        return self.players[self.curr_player_idx]

    def play_turn(self, position: Position):
        if self.board.mark(self.curr_player, position):
            if self.board.get_continuous_cells(position):
                return f"Player {self.curr_player.id} wins!"
            elif self.board.is_full():
                return "It's a draw."
            else:
                return f"Player {self.rotate_player().id}'s turn."
        return f"Invalid move {position.to_tuple()}."
