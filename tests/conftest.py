# -*- coding: utf-8 -*-
"""
    Contains fixtures for building instances required for testing.

    Read more about conftest.py under:
    https://pytest.org/latest/plugins.html
"""

import pytest
from src.euchre.card import Card
from src.euchre.table import Table
from src.euchre.hands import ComputerHand, UserHand
from src.euchre.deck import CardDeck


@pytest.fixture()
def create_computer_hand():
    j_spades = Card('J', 'Spades', 3)
    a_diamonds = Card('A', 'Diamonds', 6)
    ten_diamonds = Card('10', 'Diamonds', 2)
    king_clubs = Card('K', 'Clubs', 5)
    nine_hearts = Card('9', 'Hearts', 1)
    hand = {1: j_spades, 2: a_diamonds, 3: ten_diamonds, 4: king_clubs, 5: nine_hearts}
    computer = ComputerHand(hand, dealerflag=True, makerflag=False)
    return computer


@pytest.fixture()
def create_computer_hand_nondealer():
    q_spades = Card('Q', 'Spades', 4)
    j_diamonds = Card('J', 'Diamonds', 3)
    q_diamonds = Card('Q', 'Diamonds', 4)
    nine_spades = Card('9', 'Spades', 1)
    a_hearts = Card('A', 'Hearts', 6)
    hand = {1: q_spades, 2: j_diamonds, 3: q_diamonds, 4: nine_spades, 5: a_hearts}
    computer = ComputerHand(hand, dealerflag=False, makerflag=False)
    return computer


@pytest.fixture()
def create_user_hand():
    card_one = Card('A', 'Spades', 6)
    card_two = Card('J', 'Diamonds', 3)
    card_three = Card('10', 'Clubs', 2)
    card_four = Card('9', 'Spades', 1)
    card_five = Card('A', 'Hearts', 6)
    hand = {1: card_one, 2: card_two, 3: card_three, 4: card_four, 5: card_five}
    user = UserHand(hand, dealerflag=False, makerflag=False)
    return user


@pytest.fixture()
def create_card():
    return Card('A', 'Hearts', 6)


@pytest.fixture()
def create_card_2():
    return Card('J', 'Diamonds', 3)


@pytest.fixture()
def create_table(create_computer_hand, create_computer_hand_nondealer):
    table = Table(create_computer_hand_nondealer, create_computer_hand)
    return table


@pytest.fixture()
def create_score(create_computer_hand, create_computer_hand_nondealer):
    comp1 = create_computer_hand
    comp2 = create_computer_hand_nondealer
    score = {comp1: 2, comp2: 3}
    return score

@pytest.fixture()
def create_deck():
    deck = CardDeck()
    return deck
