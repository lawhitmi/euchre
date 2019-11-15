class Hand:
    """Superclass"""

    def __init__(self, cards={}, dealerflag=False, makerflag=False):
        self.cards = cards
        self.dealer = dealerflag
        self.maker = makerflag

    def setValues(self, trumpsuit):
        """Recalculates the value of each card based on lead card and trump suit"""
        for i in self.cards:
            self.cards[i].setValue(trumpsuit=trumpsuit)

    def setCards(self, carddict):
        self.cards = carddict

    def setMaker(self):
        self.maker = True

    def playCard(self, cardindex):
        """Plays card from the `cards` removes from deck, and returns the Card instance
        
        Input:
        cardindex: key value in `cards` dict
        """
        return self.cards.pop(cardindex)

    def __repr__(self):
        """Overloads str() operator
        """
        cardString = ""
        for i in self.cards:
            cardString = cardString + str(self.cards[i])
        return cardString


class UserHand(Hand):
    """Controls the Player's hand
    """

    def __init__(self, cards={}, dealerflag=False, makerflag=False):
        super().__init__(cards, dealerflag, makerflag)

    def bidDecide(self, rnd=1):
        if rnd == 1:
            if not self.dealer:
                while True:
                    try:
                        decision = int(input('Press (1) to Order Up or (2) to Pass: '))
                        if decision not in [1, 2]:
                            raise ValueError
                    except ValueError:
                        print('Sorry, please provide a valid input...')
                        continue
                    else:
                        break

                if decision == 1:
                    return 'order-up'
                elif decision == 2:
                    return 'pass'

            elif self.dealer:
                while True:
                    try:
                        decision = int(input('Press (1) to Accept or (2) to Pass: '))
                        if decision not in [1, 2]:
                            raise ValueError
                    except ValueError:
                        print('Sorry, please provide a valid input...')
                        continue
                    else:
                        break

                if decision == 1:
                    return 'accept'
                elif decision == 2:
                    return 'pass'
        elif rnd == 2:
            if not self.dealer:
                while True:
                    try:
                        # TODO THIS needs to be updated to work dynamically since you cannot choose the trump suit from the first round of bidding
                        decision = int(input(
                            'Input (1) to Pass, or choose a trump suit (2):Hearts, (3):Diamonds, (4):Spades, (5):Clubs'))
                        if decision not in [1, 2, 3, 4, 5]:
                            raise ValueError
                    except ValueError:
                        print('Sorry, please provide a valid input...')
                        continue
                    else:
                        break
                respDict = {2: 'Hearts', 3: 'Diamonds', 4: 'Spades', 5: 'Clubs'}
                if decision == 1:
                    return 'pass'
                else:
                    return respDict[decision]
            elif self.dealer:
                while True:
                    try:
                        # TODO THIS needs to be updated to work dynamically since you cannot choose the trump suit from the first round of bidding
                        decision = int(input('Choose a trump suit (1):Hearts, (2):Diamonds, (3):Spades, (4):Clubs'))
                        if decision not in [1, 2, 3, 4, 5]:
                            raise ValueError
                    except ValueError:
                        print('Sorry, please provide a valid input...')
                        continue
                    else:
                        break
                respDict = {1: 'Hearts', 2: 'Diamonds', 3: 'Spades', 4: 'Clubs'}
                return respDict[decision]


class ComputerHand(Hand):
    """Controls the Computer's Hand
    """

    def __init__(self, cards={}, dealerflag=False, makerFlag=False, mode='norm'):
        super().__init__(cards, dealerflag, makerFlag)
        self.playMode = mode

    def calcHandVal(self):
        handVal = 0
        for i in self.cards:
            handVal += self.cards[i].roundvalue
        return handVal

    def bidDecide(self, rnd=1):
        handVal = self.calcHandVal()
        print("Handval:"+str(handVal))
        if rnd == 1:
            if not self.dealer:
                if handVal >= 35:
                    print('Computer Orders Up')
                    return 'order-up'
                else:
                    print('Computer passes')
                    return 'pass'
            elif self.dealer:
                if handVal >= 48:
                    print('Computer accepts')
                    return 'accept'
                else:
                    print('Computer passes')
                    return 'pass'
        elif rnd == 2:
            if not self.dealer:
                # TODO method to evaluate hand for each remaining suit
                return 'Spades'

    # TODO Implement a __repr__ method for computer to hide cards
