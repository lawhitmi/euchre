class Card:
    def __init__(self, facevalue, suit, roundvalue):
        self.facevalue = facevalue
        self.suit = suit
        self.roundvalue = roundvalue
        self.basevalue = roundvalue
        self.colorCode = {'Spades': 'black', 'Clubs': 'black', 'Diamonds': 'red', 'Hearts': 'red'}
        self.color = self.setColor()

    def getValue(self):
        return self.roundvalue

    def setValue(self, trumpsuit="", leadsuit="", resetval=False):
        """

        :param trumpsuit:
        :param leadsuit:
        :param resetval:
        :return:
        """
        if resetval:
            self.roundvalue = self.basevalue

        if trumpsuit:
            if self.suit == trumpsuit:
                self.roundvalue += 14
                # Right Bower
                if self.facevalue == 'J':
                    self.roundvalue += 5
            # Left Bower
            elif self.facevalue == 'J' and self.color == self.colorCode[trumpsuit]:
                self.roundvalue += 18

        if leadsuit:
            if trumpsuit != leadsuit:
                self.roundvalue += 7

    def setColor(self):
        return self.colorCode[self.suit]

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
