from src.euchre.card import Card


def test_Card():
    cardinstance9 = Card('9', 'Spades', 1)
    assert cardinstance9.setColor() == 'black'

    assert cardinstance9.getValue() == 1
    # Change value of card based on trumpsuit
    cardinstance9.setValue(trumpsuit='Spades')
    assert cardinstance9.getValue() == 8
    # reset value of card back to basevalue
    cardinstance9.setValue(resetval=True)
    assert cardinstance9.getValue() == 1
    # TODO test the valuation of cards based on leadsuit played
    cardinstance9.setValue(trumpsuit='Spades', leadsuit='')
