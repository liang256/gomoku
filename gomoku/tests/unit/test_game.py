from gomoku.domain import model


def test_next_player():
    players = [model.Player("bob"), model.Player("Amy"), model.Player("John")]
    game = model.Game(5, 5, 3, players)
    assert game.curr_player == players[0]
    assert game.next_player() == players[1]
    assert game.next_player() == players[2]
    assert game.next_player() == players[0]
    assert game.next_player() == players[1]


def test_can_play_turn():
    # 0 0 0 0 0
    # 0 0 a 0 0
    # 0 a b 0 0
    # 0 0 0 b 0
    # 0 0 0 0 b
    bob = model.Player("Bob")
    amy = model.Player("Amy")
    game = model.Game(5, 5, 3, players=[bob, amy])
    positions = [
        [bob, (2, 2)],
        [amy, (1, 2)],
        [bob, (3, 3)],
        [amy, (2, 1)],
        [bob, (4, 4)],
    ]
    expected = [
        "Player Amy's turn.",
        "Player Bob's turn.",
        "Player Amy's turn.",
        "Player Bob's turn.",
        "Player Bob wins!",
    ]
    res = []
    for player, vec in positions:
        assert game.curr_player == player
        res.append(game.play_turn(model.Position(*vec)))
    assert res == expected


def test_can_play_turn_draw_case():
    # 1a 7b 4a
    # 6a 0b 5b
    # 3b 8a 9b
    bob = model.Player("Bob")
    amy = model.Player("Amy")
    game = model.Game(3, 3, 3, players=[bob, amy])
    positions = [
        [bob, (1, 1)],
        [amy, (0, 0)],
        [bob, (2, 0)],
        [amy, (0, 2)],
        [bob, (1, 2)],
        [amy, (1, 0)],
        [bob, (0, 1)],
        [amy, (2, 1)],
        [bob, (2, 2)],
    ]
    expected = [
        "Player Amy's turn.",
        "Player Bob's turn.",
        "Player Amy's turn.",
        "Player Bob's turn.",
        "Player Amy's turn.",
        "Player Bob's turn.",
        "Player Amy's turn.",
        "Player Bob's turn.",
        "It's a draw.",
    ]
    res = []
    for player, vec in positions:
        assert game.curr_player == player
        res.append(game.play_turn(model.Position(*vec)))
    assert res == expected


def test_cannot_play_turn_due_to_invalid_move():
    bob = model.Player("Bob")
    amy = model.Player("Amy")
    game = model.Game(5, 5, 3, players=[bob, amy])
    positions = [
        [bob, (-1, 2)],  # out of bound
        [bob, (1, 2)],
        [amy, (1, 2)],  # already occupied
    ]
    expected = ["Invalid move (-1, 2).", "Player Amy's turn.", "Invalid move (1, 2)."]
    res = []
    for player, vec in positions:
        assert game.curr_player == player
        res.append(game.play_turn(model.Position(*vec)))
    assert res == expected
