import io
import sys


def test_clear_table(create_table, create_card):
    t = create_table
    # Setup table for clear and check setup
    t.setTrumpSuit('Spades')
    t.setBidcard(create_card)
    assert t.trumpSuit == 'Spades' and t.bidcard == create_card

    # Check clear table
    t.clearTable()
    assert not t.trumpSuit and not t.bidcard


def test_flip_and_set_bidcard(create_table, create_card):
    t = create_table
    t.setBidcard(create_card)
    assert t.bidcard == create_card
    t.flipBidcard()
    assert not t.bidcard
    t.setBidcard(create_card)
    assert t.bidcard == create_card


def test_set_trumpsuit(create_table):
    t = create_table
    assert not t.trumpSuit
    t.setTrumpSuit('Spades')
    assert t.trumpSuit == 'Spades'


def test_show_table(create_table, create_score, create_card, create_card_2, capsys):
    t = create_table
    t.showTable()
    captured = capsys.readouterr()
    # Ensure that played card area is empty if no played cards are provided, and that it's the 4th line when a score
    # isn't given
    assert captured.out.split('\n')[3].strip() == ""

    t.showTable(create_card, create_card_2)
    captured = capsys.readouterr()
    # Ensure that played cards show up on 4th line when a score isn't given
    assert captured.out.split('\n')[3] == "('A', 'Hearts') ('J', 'Diamonds')"

    t.showTable(create_card, score=create_score)
    captured = capsys.readouterr()
    # Ensure single card is displayed properly
    assert captured.out.split('\n')[4] == "('A', 'Hearts')"
    assert captured.out.split('\n')[2] == "Hand Score: Computer: 2  Computer: 3  "

    t.setBidcard(create_card)
    t.showTable()
    captured = capsys.readouterr()
    # Ensure bidcard is properly displayed
    assert captured.out.split('\n')[3] == "Bidcard: ('A', 'Hearts')"






