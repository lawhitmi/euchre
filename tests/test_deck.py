from src.euchre.deck import CardDeck
from src.euchre.card import Card


def test_deal():
    testDeck = CardDeck()
    deckSize = len(testDeck.card_dict)
    # Check length of hand dealt to player
    assert len(testDeck.deal(player='y')) == 5
    # Check length of 'hand' dealt as the bidding card
    assert isinstance(testDeck.deal(player='n'), Card)
    # Check that num of cards dealt above reflects the number of cards remaining in the deck
    assert len(testDeck.card_dict) == (deckSize - 5 - 1)

    del testDeck


def test_build_deck():
    testDeck = CardDeck()
    assert isinstance(testDeck.build_deck(), dict)
    assert len(testDeck.build_deck()) == 24



