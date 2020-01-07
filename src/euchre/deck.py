from random import sample
from .card import Card


class CardDeck:
    """Controls deck and deals cards"""

    def __init__(self):
        self.card_face_values = {'9': 1, '10': 2, 'J': 3, 'Q': 4, 'K': 5, 'A': 6}
        self.card_suits = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
        self.card_dict = self.build_deck()

    def build_deck(self):
        """Builds a dictionary of Card with proper face value and suits
        :return: dict of Cards
        """
        deck_dict = {}
        i = 1
        for face_value in self.card_face_values:
            for suit in self.card_suits:
                deck_dict[i] = Card(face_value, suit, self.card_face_values[face_value])
                i += 1
        return deck_dict

    def shuffle(self):
        """
        Rebuilds deck of cards (Shuffles)
        :return: None
        """
        self.card_dict = self.build_deck()

    def deal(self, player='y'):
        """
        Selects 5 randomized cards from card_dict and returns them as a Dict
        This action removes the cards from card_dict
        :param player: string 'y' or 'n' to determine how many cards to return
        :return: dict of cards of desired length
        """
        if player == 'y':
            mask = sample(self.card_dict.keys(), 5)
        elif player == 'n':
            return self.card_dict.pop(sample(self.card_dict.keys(), 1)[0])
        hand = {}
        count = 1
        for i in mask:
            hand[count] = self.card_dict.pop(i)
            count += 1
        return hand
