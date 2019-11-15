
class Card:
    def __init__(self, facevalue, suit, roundvalue):
        self.facevalue = facevalue
        self.suit = suit
        self.roundvalue = roundvalue
        self.basevalue = roundvalue
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
        # STILL NEED TO ADD BOWERS HERE
        if resetval:
            self.roundvalue = self.basevalue
        elif self.suit == trumpsuit:
            self.roundvalue += 7
        elif trumpsuit != leadsuit:
            self.roundvalue += 1

    def setColor(self):
        if self.suit == 'Diamonds' or self.suit == 'Hearts':
            return 'red'
        else:
            return 'black'

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