COLORCODE = {'Spades': 'black', 'Clubs': 'black', 'Diamonds': 'red', 'Hearts': 'red'}


class Card:
    def __init__(self, facevalue, suit, basevalue):
        self.facevalue = facevalue
        self.suit = suit
        self.basevalue = basevalue
        self.roundvalue = basevalue
        self.color = self.getColor()

    def getValue(self):
        return self.roundvalue

    def setValue(self, trumpsuit=None, leadsuit=None, resetval=False, evaltrumpsuit=False, basevaluereset=False):
        """

        :param basevaluereset:
        :param evaltrumpsuit:
        :param trumpsuit:
        :param leadsuit:
        :param resetval:
        :return:
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

        if leadsuit:
            if trumpsuit != leadsuit and leadsuit == self.suit \
                    and not (self.facevalue == 'J' and self.color == COLORCODE[trumpsuit]):
                self.roundvalue += 7

    def getColor(self):
        return COLORCODE[self.suit]

    def getSuit(self):
        """

        :return: card suit
        """
        return self.suit

    def __repr__(self):
        return str((self.facevalue, self.suit, self.roundvalue)) # TODO remove roundvalue here, just for trobleshooting

    def __gt__(self, othercard):
        return self.roundvalue > othercard.roundvalue

    def __lt__(self, othercard):
        return self.roundvalue < othercard.roundvalue

    def __ge__(self, othercard):
        return self.roundvalue >= othercard.roundvalue

    def __le__(self, othercard):
        return self.roundvalue <= othercard.roundvalue
