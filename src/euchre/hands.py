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

    def set_values(self, trumpsuit=None, leadsuit=None, resetval=False, evaltrumpsuit=False, basevaluereset=False):
        """
        Iterates through the cards and sets their round value based on the input conditions.
        :param trumpsuit:
        :param leadsuit: suit of the card played by the other player in a trick
        :param resetval: 'soft' reset which doesn't affect trumpsuited cards
        :param evaltrumpsuit: triggers card valuation using trump suit
        :param basevaluereset: 'hard' reset
        """
        for i in self.cards:
            self.cards[i].set_value(trumpsuit=trumpsuit, leadsuit=leadsuit, resetval=resetval,
                                    evaltrumpsuit=evaltrumpsuit, basevaluereset=basevaluereset)

    def set_cards(self, carddict):
        """
        Sets the dictionary of cards
        :param carddict: dict of Cards
        """
        self.cards = carddict

    def set_maker(self):
        self.maker = True

    def set_dealer(self):
        self.dealer = True

    def clear_hand(self):
        self.cards = ""
        self.dealer = False
        self.maker = False

    def play_card(self, cardindex):
        """Pops and returns the card at the given index"""
        return self.cards.pop(cardindex)

    def get_cards_matching_suit(self, suit):
        mustplaykeys = []
        for i, j in self.cards.items():
            if j.suit == suit:  # TODO update this so that the left bower matches the suit
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

    def bid_decide(self, bidcard=None, rnd=1, excludesuit=None):

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

    def trick_decide(self, playedcard=None):

        if playedcard:
            mustplaykeys = self.get_cards_matching_suit(playedcard.get_suit())
        else:
            mustplaykeys = []

        if len(mustplaykeys) > 0:
            cardToPlay = get_user_response("Which card would you like to play? ",
                                           mustplaykeys, 'Sorry, please play card with the matching suit')
        else:
            cardToPlay = get_user_response("Which card would you like to play? ", self.cards.keys())

        return self.play_card(cardToPlay)

    def pickup_bidcard(self, bidcard):
        cardtodiscard = int(input('Select a card to replace, or press (6) to leave it.'))
        if cardtodiscard != 6:
            self.cards[cardtodiscard] = bidcard


class ComputerHand(Hand):
    """Controls the Computer's Hand
    """

    def __init__(self, cards={}, dealerflag=False, makerflag=False, mode='learn'):
        super().__init__(cards, dealerflag, makerflag)
        self.playMode = mode
        self.name = "Computer"  # needed to make object hashable for key in dict

    def calc_hand_value(self, trumpsuit=None):
        if trumpsuit:
            self.set_values(trumpsuit=trumpsuit, evaltrumpsuit=True)
        else:
            self.set_values(basevaluereset=True)
        handVal = 0
        for i in self.cards:
            handVal += self.cards[i].roundvalue
        return handVal

    def bid_decide(self, bidcard=None, rnd=1, excludesuit=None):
        if bidcard:
            handVal = self.calc_hand_value(bidcard.get_suit())
        else:
            handVal = self.calc_hand_value()

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
                    self.set_values(trumpsuit=bidcard.suit, evaltrumpsuit=True)
                    swapIndex = self.find_lowest_card()
                    self.cards[swapIndex] = bidcard
                    return 'accept'
                else:
                    print('Computer passes')
                    return 'pass'
        elif rnd == 2:
            suitlist = ['Spades', 'Clubs', "Diamonds", 'Hearts']
            suitlist.remove(excludesuit)
            handvalforeachsuit = {}
            for i in suitlist:
                self.set_values(basevaluereset=True)
                handvalforeachsuit[i] = self.calc_hand_value(trumpsuit=i)
            highestsuit = max(handvalforeachsuit, key=lambda k: handvalforeachsuit[k])
            if handvalforeachsuit[highestsuit] >= 65 or self.dealer:  # magic number
                print('Computer chooses: ' + str(highestsuit))
                return highestsuit
            else:
                print('Computer passes')
                return 'pass'

    def trick_decide(self, playedcard=None):
        """

        :param playedcard:
        :return:
        """

        if playedcard:
            # Chooses card with lowest value that still wins, or plays the card with the lowest value overall
            must_play_cards = self.get_cards_matching_suit(playedcard.get_suit())
            min_val = 100
            winner_min_val = 100
            winner_index = -1
            if len(must_play_cards) > 0:
                for i in must_play_cards:
                    if winner_min_val > self.cards[i].roundvalue > playedcard.roundvalue:
                        # Find lowest winning card, if available
                        winner_index = i
                        winner_min_val = self.cards[i].roundvalue
                    if self.cards[i].roundvalue < min_val:
                        # Find lowest card overall
                        min_index = i
                        min_val = self.cards[i].roundvalue

                if winner_index != -1:
                    return self.play_card(winner_index)
                else:
                    return self.play_card(min_index)

            else:
                return self.play_card(self.find_lowest_card())
        else:
            return self.play_card(self.find_highest_card())

    def find_lowest_card(self):
        minval = 100
        lowcardindex = None
        for idx, card in self.cards.items():
            if card.get_value() <= minval:
                minval = card.get_value()
                lowcardindex = idx
        return lowcardindex

    def find_highest_card(self):
        maxval = 0
        highcardindex = None
        for idx, card in self.cards.items():
            if card.get_value() >= maxval:
                maxval = card.get_value()
                highcardindex = idx
        return highcardindex

    def pickup_bidcard(self, bidcard):
        self.set_values(trumpsuit=bidcard.get_suit(), evaltrumpsuit=True)
        bidcard.set_value(trumpsuit=bidcard.get_suit(), evaltrumpsuit=True)
        if self.cards[self.find_lowest_card()].roundvalue < bidcard.roundvalue:
            self.cards[self.find_lowest_card()] = bidcard

    def __repr__(self):
        if self.playMode == 'norm':
            cardString = ""
            for i in self.cards:
                cardString = cardString + str(i) + str("('*','*')")
            return cardString
        elif self.playMode == 'learn':
            return super(ComputerHand, self).__repr__()
