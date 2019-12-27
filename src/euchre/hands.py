def get_user_response(question, valid_responses, error_message=None):
    while True:
        try:
            decision = int(input(question))
            if decision not in valid_responses:
                raise ValueError
        except ValueError:
            if error_message:
                print(error_message)
            else:
                print('Sorry, please provide a valid input....')
            continue
        else:
            break
    return decision


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

    def get_cards_matching_suit(self, suit):
        mustplaykeys = []
        for i, j in self.cards.items():
            if j.suit == suit:
                mustplaykeys.append(i)
        return mustplaykeys

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

    def bidDecide(self, bidcard=None, rnd=1, excludesuit=None):

        if rnd == 1:
            if not self.dealer:
                decision = get_user_response('Press (1) to Order Up or (2) to Pass: ', [1, 2])
                if decision == 1:
                    return 'order-up'
                elif decision == 2:
                    return 'pass'

            elif self.dealer:
                decision = get_user_response('Press (1) to Accept or (2) to Pass: ', [1, 2])
                if decision == 1:
                    cardtodiscard = get_user_response('Which card would you like to discard?', [1, 2, 3, 4, 5])
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
                decision = get_user_response('Input (1) to Pass, or choose a trump suit ' + suitsstring, [1, 2, 3, 4])

                if decision == 1:
                    return 'pass'
                else:
                    return suitlist[decision - 2]
            elif self.dealer:
                decision = get_user_response('Choose a trump suit: ' + suitsstring, [1, 2, 3, 4])
                return suitlist[decision - 2]

    def trickDecide(self, playedcard=None):

        if playedcard:
            mustplaykeys = self.get_cards_matching_suit(playedcard.getSuit())
        else:
            mustplaykeys = []

        if len(mustplaykeys) > 0:
            cardToPlay = get_user_response("Which card would you like to play? ",
                                           mustplaykeys, 'Sorry, please play card with the matching suit')
        else:
            cardToPlay = get_user_response("Which card would you like to play? ", self.cards.keys())

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
                print('Computer chooses: ' + str(highestsuit))
                return highestsuit
            else:
                print('Computer passes')
                return 'pass'

    def trickDecide(self, playedcard=None):
        """

        :param playedcard:
        :return:
        """

        # TODO Check this logic, played a right bower on a nonsuited lead, with other lower cards in hand
        if playedcard:
            must_play_cards = self.get_cards_matching_suit(playedcard.getSuit())

            if len(must_play_cards) > 0:
                indextoplay = must_play_cards[0]
                cardtoplay = self.cards[indextoplay]
                for i in must_play_cards:
                    if (cardtoplay.roundvalue > self.cards[i].roundvalue and (
                                not (cardtoplay.roundvalue > playedcard.roundvalue)
                                or self.cards[i].roundvalue > playedcard.roundvalue)):
                        cardtoplay = self.cards[i]
                        indextoplay = i

                return self.playCard(indextoplay)
            else:
                indextoplay = list(self.cards.keys())[0]
                cardtoplay = self.cards[indextoplay]

                for i, j in self.cards.items():
                    if (j.roundvalue > playedcard.roundvalue and not (cardtoplay.roundvalue > playedcard.roundvalue)) or \
                            (j.roundvalue < cardtoplay.roundvalue and not (cardtoplay.roundvalue > playedcard.roundvalue)):
                        cardtoplay = j
                        indextoplay = i
                return self.playCard(indextoplay)
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
