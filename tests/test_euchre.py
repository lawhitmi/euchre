from src.euchre.euchre import pick_dealer, game, check_for_winner
from src.euchre.euchre import ComputerHand, UserHand


def test_pick_dealer():
    x, y = pick_dealer()
    # Ensure only one dealer is chosen
    assert x != y


def test_check_for_winner():
    user = UserHand(makerflag=True)
    computer = ComputerHand(makerflag=False)

    # No Winner
    score = {user: 1, computer: 2}
    assert check_for_winner(score) is None
    # Maker wins with all 5
    score = {user: 5, computer: 0}
    assert check_for_winner(score) == tuple((user, 2))
    # Maker wins with less than 5
    score = {user: 4, computer: 1}
    assert check_for_winner(score) == tuple((user, 1))
    # Maker is euchred
    score = {user: 1, computer: 3}
    assert check_for_winner(score) == tuple((computer, 2))
    # End of round is reached
    score = {user: 2, computer: 3}
    assert check_for_winner(score) == tuple((computer, 2))


def test_game():
    # game()
    NotImplemented
