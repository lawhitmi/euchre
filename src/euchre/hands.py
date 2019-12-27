class Hand:
    """Superclass"""

    def __init__(self, cards={}, dealerflag=False, makerflag=False):
        self.cards = cards
        self.dealer = dealerflag
        self.maker = makerflag

    def setValues(self, trumpsuit=None, leadsuit=None, resetval=False, evaltrumpsuit=False, basevaluereset=False):
        """
        Iterates through the cards and sets their round value based on the input conditions.
        :param trumpsuit:
        :param leadsuit: suit of the card played by the other player in a trick
        :param resetval: 'soft' reset which doesn't affect trumpsuited cards
        :param evaltrumpsuit: triggers card valuation using trump suit
        :param basevaluereset: 'hard' reset
        """
        for i in self.cards:
            self.cards[i].setValue(trumpsuit=trumpsuit, leadsuit=leadsuit, resetval=resetval,
                                   evaltrumpsuit=evaltrumpsuit, basevaluereset=basevaluereset)

    def setCards(self, carddict):
        """
        Sets the dictionary of cards
        :param carddict: dict of Cards
        """
        self.cards = carddict

    def setMaker(self):
        self.maker = True

    def setDealer(self):
        self.dealer = True

    def clearHand(self):
        self.cards = ""
        self.dealer = False
        self.maker = False

    def playCard(self, cardindex):
        """Pops and returns the card at the given index"""
        return self.cards.pop(cardindex)

    def __repr__(self):
        """Overloads str() operator"""
        cardString = ""
        for i in self.cards:
            cardString = cardString + str(i) + str(self.cards[i])
        return cardString


class UserHand(Hand):
    """Controls the Player's hand"""

    def __init__(self, cards={}, dealerflag=False, makerflag=False):
        super().__init__(cards, dealerflag, makerflag)
        self.name = "Player"
        self.providevalidinputstring = 'Sorry, please provide a valid input...'

    def bidDecide(self, bidcard=None, rnd=1, excludesuit=None):

        if rnd == 1:
            if not self.dealer:
                while True:
                    try:
                        decision = int(input('Press (1) to Order Up or (2) to Pass: '))
                        if decision not in [1, 2]:
                            raise ValueError
                    except ValueError:
                        print(self.providevalidinputstring)
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
                        print(self.providevalidinputstring)
                        continue
                    else:
                        break
                if decision == 1:
                    cardtodiscard = int(input('Which card would you like to discard?'))
                    self.cards[cardtodiscard] = bidcard
                    return 'accept'
                elif decision == 2:
                    return 'pass'
        elif rnd == 2:
            suitlist = ['Spades', 'Clubs', "Diamonds", 'Hearts']
            suitlist.remove(excludesuit)
            suitsstring = ""
            option = 2
            for i in suitlist:
                suitsstring += '(' + str(option) + '):' + str(i) + ' '
                option += 1

            if not self.dealer:
                while True:
                    try:
                        trumpselectstring = 'Input (1) to Pass, or choose a trump suit '

                        decision = int(input(trumpselectstring+suitsstring))
                        if decision not in [1, 2, 3, 4]:
                            raise ValueError
                    except ValueError:
                        print(self.providevalidinputstring)
                        continue
                    else:
                        break
                if decision == 1:
                    return 'pass'
                else:
                    return suitlist[decision-2]
            elif self.dealer:
                while True:
                    try:
                        trumpselectstring = 'Choose a trump suit: '
                        decision = int(input(trumpselectstring+suitsstring))
                        if decision not in [2, 3, 4]:
                            raise ValueError
                    except ValueError:
                        print(self.providevalidinputstring)
                        continue
                    else:
                        break

                return suitlist[decision-2]

    def trickDecide(self, playedcard=None):
        if playedcard:
            mustplaykeys = []
            for i, j in self.cards.items():
                if j.suit == playedcard.suit:
                    mustplaykeys.append(i)
            if len(mustplaykeys) > 0:
                while True:
                    try:
                        cardToPlay = int(input("Which card would you like to play? "))
                        if cardToPlay not in mustplaykeys:
                            raise ValueError
                    except ValueError:
                        print('Sorry, please play card with the matching suit')
                        continue
                    else:
                        break
            else:
                while True:
                    try:
                        cardToPlay = int(input("Which card would you like to play? "))
                        if cardToPlay not in self.cards.keys():
                            raise ValueError
                    except ValueError:
                        print(self.providevalidinputstring)
                        continue
                    else:
                        break
        else:
            while True:
                try:
                    cardToPlay = int(input("Which card would you like to play? "))
                    if cardToPlay not in self.cards.keys():
                        raise ValueError
                except ValueError:
                    print(self.providevalidinputstring)
                    continue
                else:
                    break
        return self.playCard(cardToPlay)

    def pickUpBidcard(self, bidcard):
        cardtodiscard = int(input('Select a card to replace, or press (6) to leave it.'))
        if cardtodiscard != 6:
            self.cards[cardtodiscard] = bidcard


class ComputerHand(Hand):
    """Controls the Computer's Hand
    """

    def __init__(self, cards={}, dealerflag=False, makerFlag=False, mode='learn'):
        super().__init__(cards, dealerflag, makerFlag)
        self.playMode = mode
        self.name = "Computer"  # needed to make object hashable for key in dict

    def calcHandVal(self, trumpsuit=None):
        if trumpsuit:
            self.setValues(trumpsuit=trumpsuit, evaltrumpsuit=True)
        else:
            self.setValues(basevaluereset=True)
        handVal = 0
        for i in self.cards:
            handVal += self.cards[i].roundvalue
        return handVal

    def bidDecide(self, bidcard=None, rnd=1, excludesuit=None):
        if bidcard:
            handVal = self.calcHandVal(bidcard.getSuit())
        else:
            handVal = self.calcHandVal()

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
                    self.setValues(trumpsuit=bidcard.suit, evaltrumpsuit=True)
                    swapIndex = self.findLowestCard()
                    self.cards[swapIndex] = bidcard
                    return 'accept'
                else:
                    print('Computer passes')
                    return 'pass'
        elif rnd == 2:
            suitlist = ['Spades', 'Clubs', "Diamonds", 'Hearts']
            suitlist.remove(excludesuit)
            # TODO this logic works, but one bower can cause the computer to choose a suit that it only has one of.
            #  Also doesn't take into account the bidcard
            handvalforeachsuit = {}
            for i in suitlist:
                handvalforeachsuit[i] = self.calcHandVal(trumpsuit=i)
            highestsuit = max(handvalforeachsuit, key=lambda k: handvalforeachsuit[k])
            if handvalforeachsuit[highestsuit] >= 65 or self.dealer:  # magic number
                print('Computer chooses: '+str(highestsuit))
                return highestsuit
            else:
                print('Computer passes')
                return 'pass'

    def trickDecide(self, playedcard=None):
        """

        :param trumpsuit:
        :param playedcard:
        :return:
        """
        cardtoplay = 0
        # TODO Check this logic, played a right bower on a nonsuited lead, with other lower cards in hand
        if playedcard:
            for i, j in self.cards.items():
                if j.suit == playedcard.getSuit():
                    if cardtoplay != 0:
                        if cardtoplay.roundvalue > j.roundvalue:
                            if not (cardtoplay.roundvalue > playedcard.roundvalue) \
                                    or j.roundvalue > playedcard.roundvalue:
                                cardtoplay = j
                                indextoplay = i
                    elif cardtoplay == 0:
                        cardtoplay = j
                        indextoplay = i
            if cardtoplay != 0:
                return self.playCard(indextoplay)
            else:
                cardtoplay = 0
                indextoplay = 0
                for i, j in self.cards.items():
                    if not cardtoplay:
                        cardtoplay = j
                        indextoplay = i
                    elif j.roundvalue > playedcard.roundvalue and not (cardtoplay.roundvalue > playedcard.roundvalue):
                        cardtoplay = j
                        indextoplay = i
                    elif j.roundvalue < cardtoplay.roundvalue and not (cardtoplay.roundvalue > playedcard.roundvalue):
                        cardtoplay = j
                        indextoplay = i
                return  self.playCard(indextoplay)
        else:
            return self.playCard(self.findHighestCard())

    def findLowestCard(self):
        minval = 100
        lowcardindex = None
        for idx, card in self.cards.items():
            if card.getValue() <= minval:
                minval = card.getValue()
                lowcardindex = idx
        return lowcardindex

    def findHighestCard(self):
        maxval = 0
        highcardindex = None
        for idx, card in self.cards.items():
            if card.getValue() >= maxval:
                maxval = card.getValue()
                highcardindex = idx
        return highcardindex

    def pickUpBidcard(self, bidcard):
        self.setValues(trumpsuit=bidcard.getSuit(), evaltrumpsuit=True)
        bidcard.setValue(trumpsuit=bidcard.getSuit(), evaltrumpsuit=True)
        if self.cards[self.findLowestCard()].roundvalue < bidcard.roundvalue:
            self.cards[self.findLowestCard()] = bidcard

    def __repr__(self):
        if self.playMode == 'norm':
            cardString = ""
            for i in self.cards:
                cardString = cardString + str(i) + str("('*','*')")
            return cardString
        elif self.playMode == 'learn':
            return super(ComputerHand, self).__repr__()

