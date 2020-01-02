from src.euchre.card import Card


def test_card():
    cardinstance_9_spades = Card('9', 'Spades', 1)
    assert cardinstance_9_spades.get_color() == 'black'

    # Check initial value
    assert cardinstance_9_spades.get_value() == 1

    # Change value of card based on trumpsuit
    cardinstance_9_spades.set_value(trumpsuit='Spades', evaltrumpsuit=True)
    assert cardinstance_9_spades.get_value() == 15

    # reset value of card back to basevalue
    cardinstance_9_spades.set_value(trumpsuit='Clubs', resetval=True)
    assert cardinstance_9_spades.get_value() == 1

    # test the valuation of cards based on leadsuit played
    cardinstance_10_diamonds = Card('10', 'Diamonds', 2)
    cardinstance_10_diamonds.set_value(trumpsuit='Spades', leadsuit='Diamonds')
    assert cardinstance_10_diamonds.get_value() == 9

    # test the reset of the value of the card for the next trick
    cardinstance_10_diamonds.set_value(trumpsuit='Spades', resetval=True)
    assert cardinstance_10_diamonds.get_value() == 2

    # Check value of left bower
    cardinstance_J_Spades = Card('J', 'Spades', 3)
    cardinstance_J_Spades.set_value(trumpsuit='Clubs', evaltrumpsuit=True)
    assert cardinstance_J_Spades.get_value() == 21

    # Check value of right bower
    cardinstance_J_Clubs = Card('J', 'Clubs', 3)
    cardinstance_J_Clubs.set_value(trumpsuit='Clubs', evaltrumpsuit=True)
    assert cardinstance_J_Clubs.get_value() == 22

    # Ensure that the value of the trump cards aren't changed when a lead card of the trump suit is played
    cardinstance_J_Clubs.set_value(trumpsuit='Clubs', leadsuit='Clubs')
    assert cardinstance_J_Clubs.get_value() == 22


