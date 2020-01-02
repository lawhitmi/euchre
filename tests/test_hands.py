
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

    c = create_computer_hand
    bidcard = create_card
    # Check that computer passes on bidcard
    assert c.bidDecide(bidcard=bidcard) == 'pass'
    # Check that computer chooses 'Clubs'
    assert c.bidDecide(rnd=2, excludesuit='Hearts') == 'Clubs'

    # Set to nondealer
    c.dealer = False
    c.setValues(basevaluereset=True)
    # Should pass on bidcard
    assert c.bidDecide(bidcard=bidcard) == 'pass'
    # Then choose a suit
    assert c.bidDecide(rnd=2, excludesuit='Hearts') == 'pass'
    # If clubs is excluded, should pass
    assert c.bidDecide(rnd=2, excludesuit='Clubs') == 'pass'

    # TODO Add case for handvalue > 65 and nondealer
    # TODO Add case for order-up and accepts


def test_set_dealer(create_computer_hand_nondealer):
    c = create_computer_hand_nondealer
    assert c.dealer is False

    c.setDealer()
    assert c.dealer is True

