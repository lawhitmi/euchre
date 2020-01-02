from src.euchre.deck import CardDeck
from src.euchre.card import Card


def test_deal():
    test_deck = CardDeck()
    deck_size = len(test_deck.card_dict)
    # Check length of hand dealt to player
    assert len(test_deck.deal(player='y')) == 5
    # Check length of 'hand' dealt as the bidding card
    assert isinstance(test_deck.deal(player='n'), Card)
    # Check that num of cards dealt above reflects the number of cards remaining in the deck
    assert len(test_deck.card_dict) == (deck_size - 5 - 1)

    del test_deck


def test_build_deck():
    test_deck = CardDeck()
    assert isinstance(test_deck.build_deck(), dict)
    assert len(test_deck.build_deck()) == 24



