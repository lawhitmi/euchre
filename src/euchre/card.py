COLORCODE = {'Spades': 'black', 'Clubs': 'black', 'Diamonds': 'red', 'Hearts': 'red'}


class Card:
    """
    Represents an individual card in the deck. Also controls the value of the cards.
    """
    def __init__(self, facevalue, suit, basevalue):
        self.facevalue = facevalue
        self.suit = suit
        self.basevalue = basevalue
        self.roundvalue = basevalue
        self.color = self.get_color()

    def get_value(self):
        """
        Getter method which provides the value of the card
        :return: int  current value of the card
        """
        return self.roundvalue

    def set_value(self, trumpsuit=None, leadsuit=None, resetval=False, evaltrumpsuit=False, basevaluereset=False):
        """
        Sets the value of the card depending on the trumpsuit, suit of card, phase of the game, etc.
        :param trumpsuit: string i.e 'Spades'
        :param leadsuit: string representing the first card played in a trick
        :param resetval: bool 'soft' reset which doesn't change value of trumpsuited cards
        :param evaltrumpsuit: bool forces change of value of trumpsuited cards
        :param basevaluereset: bool 'hard' reset which restores all cards back to basevalue
        :return: None
        """
        if basevaluereset:
            self.roundvalue = self.basevalue

        if resetval and self.suit != trumpsuit and not (self.facevalue == 'J' and self.color == COLORCODE[trumpsuit]):
            self.roundvalue = self.basevalue

        if evaltrumpsuit:
            if self.suit == trumpsuit:
                self.roundvalue += 14
                # Right Bower
                if self.facevalue == 'J':
                    self.roundvalue += 5
            # Left Bower
            elif self.facevalue == 'J' and self.color == COLORCODE.get(trumpsuit):
                self.roundvalue += 18

        if leadsuit and trumpsuit != leadsuit and leadsuit == self.suit \
                and not (self.facevalue == 'J' and self.color == COLORCODE[trumpsuit]):
            self.roundvalue += 7

    # TODO use the methods below instead of this monstrosity above
    # def reset_to_base_value(self):
    #     self.roundvalue = self.basevalue
    #
    # def set_value_trump_cards(self, trumpsuit):
    #     if self.suit == trumpsuit:
    #         self.roundvalue += 14
    #         # Right Bower
    #         if self.facevalue == 'J':
    #             self.roundvalue += 5
    #     # Left Bower
    #     elif self.facevalue == 'J' and self.color == COLORCODE.get(trumpsuit):
    #         self.roundvalue += 18
    #
    # def set_value_lead_suit(self, leadsuit, trumpsuit):
    #     if trumpsuit != leadsuit and leadsuit == self.suit \
    #             and not (self.facevalue == 'J' and self.color == COLORCODE[trumpsuit]):
    #         self.roundvalue += 7
    #
    # def reset_non_trump_cards(self, trumpsuit):
    #     if self.suit != trumpsuit and not (self.facevalue == 'J' and self.color == COLORCODE[trumpsuit]):
    #         self.roundvalue = self.basevalue

    def get_color(self):
        """
        Getter method for color
        :return: string i.e 'black'
        """
        return COLORCODE[self.suit]

    def get_suit(self):
        """
        Getter method for card suit
        :return: string i.e. 'Spades'
        """
        return self.suit

    def __repr__(self):
        return str((self.facevalue, self.suit))

    def __gt__(self, othercard):
        return self.roundvalue > othercard.roundvalue

    def __lt__(self, othercard):
        return self.roundvalue < othercard.roundvalue

    def __ge__(self, othercard):
        return self.roundvalue >= othercard.roundvalue

    def __le__(self, othercard):
        return self.roundvalue <= othercard.roundvalue
