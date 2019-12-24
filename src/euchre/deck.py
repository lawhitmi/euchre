from random import sample
from card import Card


class CardDeck:
    """Controls deck and deals cards"""

    def __init__(self):
        self.cardFaceValues = {'9': 1, '10': 2, 'J': 3, 'Q': 4, 'K': 5, 'A': 6}
        self.cardSuits = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
        self.CardDict = self.buildDeck()

    def buildDeck(self):
        """Builds a dictionary of Card with proper face value and suits"""
        deckDict = {}
        i = 1
        for faceValue in self.cardFaceValues:
            for suit in self.cardSuits:
                deckDict[i] = Card(faceValue, suit, self.cardFaceValues[faceValue])
                i += 1
        return deckDict

    def shuffle(self):
        self.CardDict = self.buildDeck()

    def deal(self, player='y'):
        """Selects 5 randomized cards from CardDict and returns them as a Dict
        This action removes the cards from CardDict"""
        if player == 'y':
            mask = sample(self.CardDict.keys(), 5)
        elif player == 'n':
            return self.CardDict.pop(sample(self.CardDict.keys(), 1)[0])
        hand = {}
        count = 1
        for i in mask:
            hand[count] = self.CardDict.pop(i)
            count += 1
        return hand
