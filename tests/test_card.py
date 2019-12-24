from src.euchre.card import Card


def test_Card():
    cardinstance_9_spades = Card('9', 'Spades', 1)
    assert cardinstance_9_spades.getColor() == 'black'

    # Check initial value
    assert cardinstance_9_spades.getValue() == 1

    # Change value of card based on trumpsuit
    cardinstance_9_spades.setValue(trumpsuit='Spades')
    assert cardinstance_9_spades.getValue() == 15

    # reset value of card back to basevalue
    cardinstance_9_spades.setValue(resetval=True)
    assert cardinstance_9_spades.getValue() == 1

    # test the valuation of cards based on leadsuit played
    cardinstance_10_diamonds = Card('10', 'Diamonds', 2)
    cardinstance_10_diamonds.setValue(leadsuit='Diamonds')
    assert cardinstance_10_diamonds.getValue() == 9

    # Check value of left bower
    cardinstance_J_Spades = Card('J', 'Spades', 3)
    cardinstance_J_Spades.setValue(trumpsuit='Clubs')
    assert cardinstance_J_Spades.getValue() == 21

    # Check value of right bower
    cardinstance_J_Spades.setValue(resetval=True)
    assert cardinstance_J_Spades.getValue() == 3
    cardinstance_J_Spades.setValue(trumpsuit='Spades')
    assert cardinstance_J_Spades.getValue() == 22


