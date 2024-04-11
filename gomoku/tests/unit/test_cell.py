from gomoku.domain import model


def test_to_dict():
    cell = model.Cell(model.Player("bob"), None)
    assert cell.to_dict() == {"player": model.Player("bob"), "data": None}
