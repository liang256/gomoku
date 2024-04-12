from gomoku.domain import model


class FakeRenderable:
    pass


def test_init_board():
    board = model.Board(5, 4, 3)
    assert len(board.grid) == 4
    assert len(board.grid[0]) == 5
    assert board.win_condition_length == 3


def test_board_can_mark_cell():
    player = model.Player("Bob")
    position = model.Position(0, 0)
    meta_data = {"color": (1, 1, 1)}
    board = model.Board(5, 5, 3)
    assert board.mark(player, position, meta_data)
    assert board.grid[0][0] is not None
    assert board.grid[0][0].player == player
    assert board.grid[0][0].data == meta_data


def test_board_can_check_in_bound():
    board = model.Board(1, 1, 1)
    assert board.is_in_bound(model.Position(0, 0))
    assert board.is_in_bound(model.Position(-1, 0)) is False
    assert board.is_in_bound(model.Position(10, 10)) is False


def test_board_cannot_mark_cell_if_out_of_bound():
    board = model.Board(5, 5, 3)
    board.mark(model.Player("bob"), model.Position(2, 2))
    assert board.can_mark(model.Position(6, 0)) is False
    assert board.can_mark(model.Position(-1, 0)) is False
    assert board.can_mark(model.Position(2, 2)) is False


def test_board_can_get_continous_cells():
    board = model.Board(4, 4, 2)
    bob = model.Player("Bob")
    positions = [[1, 1, 1, 1], [0, 1, 0, 1], [0, 0, 1, 1], [1, 1, 1, 1]]
    for row in range(len(positions)):
        for col in range(len(positions[0])):
            if positions[row][col] == 0:
                continue
            board.mark(bob, model.Position(row, col))
    positions = board.get_continuous_cells(model.Position(2, 2))
    assert len(positions) == 8
    assert {p.to_tuple() for p in positions} == set(
        [(0, 0), (1, 1), (2, 2), (3, 3), (3, 1), (1, 3), (2, 3), (3, 2)]
    )


def test_is_full():
    bob = model.Player("bob")
    board = model.Board(4, 4, 3)
    positions = [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]
    for row in range(4):
        for col in range(4):
            board.mark(bob, model.Position(row, col))
    assert board.is_full()
