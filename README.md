# Gomoku

This Python module provides a robust engine for handling generic board games. It includes classes and methods to manage player interactions, board states, and game rules.

## Features

- **Player Management:** Handles player identification and equality checks.
- **Board Management:** Supports dynamic board sizes, cell marking, and boundary checks.
- **Game Rules Enforcement:** Ensures moves are valid, positions are in bounds, and implements win condition checks.

## Classes

### `Player`
Represents a player in the game. Players are identified uniquely using an ID.

### `Position`
Represents a position on the board with row and column data. It also provides methods to convert position data into tuple format.

### `Cell`
Encapsulates the concept of a cell on the board, holding both the player occupying the cell and additional metadata.

### `Board`
Handles the main logic for board setup and gameplay. It includes methods to:
- Initialize the board with specified dimensions.
- Mark positions on the board.
- Fetch data from specific positions.
- Check if positions are within valid bounds and unoccupied.

## Usage

### Initializing the Board
```python
from main import Player, Board, Position

# Create players
player1 = Player(id="P1")
player2 = Player(id="P2")

# Initialize a 10x10 board with a win condition of 5 in a row
game_board = Board(width=10, height=10, win_condition_length=5)
```

### Making a Move
```
# Player 1 marks position at row 3, column 4
pos = Position(row=3, col=4)
game_board.mark(player=player1, position=pos)
```

## Requirements
Python 3.8 or higher


## Contributing
Contributions are welcome! Please fork the repository and submit pull requests with your features and bug fixes.