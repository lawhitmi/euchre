from src.euchre.deck import CardDeck


def test_deal():
    testDeck = CardDeck()
    deckSize = len(testDeck.CardDict)
    # Check length of hand dealt to player
    assert len(testDeck.deal(player='y')) == 5
    # Check length of 'hand' dealt as the bidding card
    assert len(testDeck.deal(player='n')) == 1
    # Check that num of cards dealt above reflects the number of cards remaining in the deck
    assert len(testDeck.CardDict) == (deckSize-5-1)

    del testDeck


def test_buildDeck():
    testDeck = CardDeck()
    assert isinstance(testDeck.buildDeck(), dict)
    assert len(testDeck.buildDeck()) == 24


