from src.euchre.euchre import pick_dealer, game, check_for_winner, bid_phase, trick_phase, next_round_reset
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


def test_bid_phase(create_computer_hand_nondealer, create_computer_hand, create_card, create_table):
    # TODO come back to this after implementing the unit test for hte biddecide method
    c1 = create_computer_hand_nondealer
    c2 = create_computer_hand
    card = create_card
    t = create_table
    trumpsuit, maker = bid_phase(c1, c2, card, t)
    assert trumpsuit == 'Hearts'
    assert maker == c1

    c1.setDealer()
    c2.dealer = False
    trumpsuit, maker = bid_phase(c2, c1, card, t)
    assert trumpsuit == 'Hearts'
    assert maker == c2


def test_trick_phase(create_computer_hand_nondealer, create_computer_hand, create_table):
    firstplayer = create_computer_hand_nondealer
    secondplayer = create_computer_hand
    firstplayer.setMaker()
    t = create_table
    trickwinner, points = trick_phase(firstplayer, secondplayer, trump='Diamonds', table=t)
    assert trickwinner == firstplayer
    assert points == 1


def test_next_round_reset(create_computer_hand_nondealer, create_computer_hand, create_table, create_deck):
    deck = create_deck
    user = create_computer_hand_nondealer
    userdealer = user.dealer
    userhand = user.cards
    computer = create_computer_hand
    compdealer = computer.dealer
    comphand = computer.cards
    table = create_table
    table.tricks[user] += 1
    next_round_reset(deck, user, computer, table)
    # Ensure dealer swaps
    assert user.dealer != userdealer
    assert computer.dealer != compdealer
    # Ensure hand has changed
    assert user.cards != userhand
    assert computer.cards != comphand
    # Ensure score is not reset
    assert sum(table.tricks.values()) == 1


def test_game():
    # game()
    NotImplemented
