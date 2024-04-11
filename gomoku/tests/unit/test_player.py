from gomoku.domain import model


def test_player_eq():
    player1 = model.Player("bob")
    player2 = model.Player("bob")
    assert player1 == player2
