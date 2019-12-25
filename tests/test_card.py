from src.euchre.card import Card


def test_Card():
    cardinstance_9_spades = Card('9', 'Spades', 1)
    assert cardinstance_9_spades.getColor() == 'black'

    # Check initial value
    assert cardinstance_9_spades.getValue() == 1

    # Change value of card based on trumpsuit
    cardinstance_9_spades.setValue(trumpsuit='Spades', evaltrumpsuit=True)
    assert cardinstance_9_spades.getValue() == 15

    # reset value of card back to basevalue
    cardinstance_9_spades.setValue(trumpsuit='Clubs', resetval=True)
    assert cardinstance_9_spades.getValue() == 1

    # test the valuation of cards based on leadsuit played
    cardinstance_10_diamonds = Card('10', 'Diamonds', 2)
    cardinstance_10_diamonds.setValue(trumpsuit='Spades', leadsuit='Diamonds')
    assert cardinstance_10_diamonds.getValue() == 9

    # test the reset of the value of the card for the next trick
    cardinstance_10_diamonds.setValue(trumpsuit='Spades', resetval=True)
    assert cardinstance_10_diamonds.getValue() == 2

    # Check value of left bower
    cardinstance_J_Spades = Card('J', 'Spades', 3)
    cardinstance_J_Spades.setValue(trumpsuit='Clubs', evaltrumpsuit=True)
    assert cardinstance_J_Spades.getValue() == 21

    # Check value of right bower
    cardinstance_J_Clubs = Card('J', 'Clubs', 3)
    cardinstance_J_Clubs.setValue(trumpsuit='Clubs', evaltrumpsuit=True)
    assert cardinstance_J_Clubs.getValue() == 22

    # Ensure that the value of the trump cards aren't changed when a lead card of the trump suit is played
    cardinstance_J_Clubs.setValue(trumpsuit='Clubs', leadsuit='Clubs')
    assert cardinstance_J_Clubs.getValue() == 22


