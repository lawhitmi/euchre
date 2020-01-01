from src.euchre.hands import UserHand, ComputerHand
from src.euchre.card import Card
from pytest import fixture


@fixture()
def create_computer_hand():
    j_spades = Card('J', 'Spades', 3)
    a_diamonds = Card('A', 'Diamonds', 6)
    ten_diamonds = Card('10', 'Diamonds', 2)
    king_clubs = Card('K', 'Clubs', 5)
    nine_hearts = Card('9', 'Hearts', 1)
    hand = {1: j_spades, 2: a_diamonds, 3: ten_diamonds, 4: king_clubs, 5: nine_hearts}
    computer = ComputerHand(hand, dealerflag=True, makerflag=False)
    return computer


@fixture()
def create_card():
    return Card('A', 'Hearts', 6)


def test_calc_hand_val(create_computer_hand):
    c = create_computer_hand
    # Check basevalue calculation
    assert c.calcHandVal() == 17
    # Check that calculation with trumpsuit is correct
    assert c.calcHandVal(trumpsuit='Spades') == 36
    # Ensure that cards are correctly reset to basevalue before recalculation
    assert c.calcHandVal() == 17


def test_get_cards_matching_suit(create_computer_hand):
    c = create_computer_hand
    assert c.get_cards_matching_suit(suit="Diamonds") == [2, 3]


def test_find_lowest_card(create_computer_hand):
    c = create_computer_hand
    # Check function with basevalue of cards
    assert c.findLowestCard() == 5
    # Recalculate value of cards and attempt again
    c.setValues(trumpsuit='Hearts', evaltrumpsuit=True)
    assert c.findLowestCard() == 3


def test_find_highest_card(create_computer_hand):
    c = create_computer_hand
    # Check function with basevalue of cards
    assert c.findHighestCard() == 2
    # Recalculate value of cards and attempt again
    c.setValues(trumpsuit='Hearts', evaltrumpsuit=True)
    assert c.findHighestCard() == 5


def test_pick_up_bidcard(create_computer_hand, create_card):
    computer = create_computer_hand
    # Save the card which should be dropped for checking later
    card_to_drop = computer.cards[3]
    bidcard = create_card
    computer.pickUpBidcard(bidcard)
    # Check card added to hand
    assert bidcard in computer.cards.values()
    # Check card removed from hand
    assert card_to_drop not in computer.cards.values()


def test_trick_decide(create_computer_hand, create_card):
    computer = create_computer_hand
    played_card = create_card
    card_to_be_played = computer.cards[2]
    # The next step is normally performed in euchre.py prior to calling trickPhase
    computer.setValues(trumpsuit="Diamonds", evaltrumpsuit=True)
    # Check that the computer leads with the correct card
    assert computer.trickDecide() == card_to_be_played
    # The next step is normally performed in euchre.py prior to calling trickDecide
    computer.setValues(trumpsuit="Diamonds", leadsuit=played_card.getSuit())
    card_to_be_played = computer.cards[5]
    # Check that the computer plays a matching suit if possible
    assert computer.trickDecide(playedcard=played_card) == card_to_be_played


def test_bid_decide(create_computer_hand, create_card):
    NotImplemented
