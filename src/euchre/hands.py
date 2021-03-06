def get_user_response(question, valid_responses, error_message=None):
    """
    Function to obtain input from the user.
    :param question: string Question to ask user
    :param valid_responses: list of valid responses to use in error catching
    :param error_message: string Message to display if an exception occurs
    :return: user decision
    """
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
        :param trumpsuit: current suit of trumpcard
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
        """
        Sets the maker flag to True
        """
        self.maker = True

    def set_dealer(self):
        """
        Sets the dealer flag to True
        """
        self.dealer = True

    def clear_hand(self):
        """
        Resets hand for the next round.
        """
        self.cards = ""
        self.dealer = False
        self.maker = False

    def play_card(self, cardindex):
        """Pops and returns the card at the given index"""
        return self.cards.pop(cardindex)

    def get_cards_matching_suit(self, suit):
        """
        Determines if any cards in hand match the played suit
        :param suit: string suit of played card i.e. 'Spades'
        :return: list of keys in hand that match the passed suit
        """
        mustplaykeys = []
        for i, j in self.cards.items():
            if j.suit == suit:  # TODO update this so that the left bower matches the suit
                mustplaykeys.append(i)
        return mustplaykeys

    def __repr__(self):
        """Overloads str() operator"""
        card_string = ""
        for i in self.cards:
            card_string = card_string + str(i) + str(self.cards[i])
        return card_string


class UserHand(Hand):
    """Controls the Player's hand"""

    def __init__(self, cards={}, dealerflag=False, makerflag=False):
        super().__init__(cards, dealerflag, makerflag)
        self.name = "Player"

    def bid_decide(self, bidcard=None, rnd=1, excludesuit=None):
        """
        Defines user's bid phase
        :param bidcard: Card type for decision
        :param rnd: int Which round of bidding
        :param excludesuit: string suit of bid card which can no longer be selected
        :return: string User decision
        """
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
        """
        Controls user's trick phase.
        :param playedcard: Card type Card played by other 'hand' if applicable
        :return: Card type Card to play
        """
        if playedcard:
            mustplaykeys = self.get_cards_matching_suit(playedcard.get_suit())
        else:
            mustplaykeys = []

        if len(mustplaykeys) > 0:
            card_to_play = get_user_response("Which card would you like to play? ",
                                             mustplaykeys, 'Sorry, please play card with the matching suit')
        else:
            card_to_play = get_user_response("Which card would you like to play? ", self.cards.keys())

        return self.play_card(card_to_play)

    def pickup_bidcard(self, bidcard):
        """
        Allows user to decide whether to pick up bidcard upon acceptance
        :param bidcard: Card type  Played card
        :return: None
        """
        cardtodiscard = int(input('Select a card to replace, or press (6) to leave it.'))
        if cardtodiscard != 6:
            self.cards[cardtodiscard] = bidcard


class ComputerHand(Hand):
    """Controls the Computer's Hand
    """

    def __init__(self, cards={}, dealerflag=False, makerflag=False, play_mode=False):
        super().__init__(cards, dealerflag, makerflag)
        self.playMode = play_mode
        self.name = "Computer"  # needed to make object hashable for key in dict

    def calc_hand_value(self, trumpsuit=None):
        """
        Private method which provides a sum of the values of the cards in the computer's hand
        :param trumpsuit: string If provided, re-evaluates the card value using the trumpsuit
        :return: int Sum of card values
        """
        if trumpsuit:
            self.set_values(trumpsuit=trumpsuit, evaltrumpsuit=True)
        else:
            self.set_values(basevaluereset=True)
        hand_val = 0
        for i in self.cards:
            hand_val += self.cards[i].roundvalue
        return hand_val

    def bid_decide(self, bidcard=None, rnd=1, excludesuit=None):
        """
        Controls Computer's bid phase.
        :param bidcard: Card type for decision
        :param rnd: int Which round of bidding
        :param excludesuit: string suit of bid card which can no longer be selected
        :return: string Computer decision
        """
        if bidcard:
            hand_val = self.calc_hand_value(bidcard.get_suit())
        else:
            hand_val = self.calc_hand_value()

        if rnd == 1:
            if not self.dealer:
                if hand_val >= 35:
                    print('Computer Orders Up')
                    return 'order-up'
                else:
                    print('Computer passes')
                    return 'pass'
            elif self.dealer:
                if hand_val >= 48:
                    print('Computer accepts')
                    self.set_values(trumpsuit=bidcard.suit, evaltrumpsuit=True)
                    swap_index = self.find_lowest_card()
                    self.cards[swap_index] = bidcard
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
        Controls Computers's trick phase.
        :param playedcard: Card type Card played by other 'hand' if applicable
        :return: Card type Card to play
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
        """
        Returns the index in cards of the card with the lowest value
        """
        minval = 100
        lowcardindex = None
        for idx, card in self.cards.items():
            if card.get_value() <= minval:
                minval = card.get_value()
                lowcardindex = idx
        return lowcardindex

    def find_highest_card(self):
        """
        Returns the index in cards of the card with the highest value
        """
        maxval = 0
        highcardindex = None
        for idx, card in self.cards.items():
            if card.get_value() >= maxval:
                maxval = card.get_value()
                highcardindex = idx
        return highcardindex

    def pickup_bidcard(self, bidcard):
        """
        Method for computer to decide on picking up the bidcard
        :param bidcard: Card type on which to perform bid phase
        :return: None
        """
        self.set_values(trumpsuit=bidcard.get_suit(), evaltrumpsuit=True)
        bidcard.set_value(trumpsuit=bidcard.get_suit(), evaltrumpsuit=True)
        if self.cards[self.find_lowest_card()].roundvalue < bidcard.roundvalue:
            self.cards[self.find_lowest_card()] = bidcard

    def __repr__(self):
        if not self.playMode:
            card_string = ""
            for i in self.cards:
                card_string = card_string + str(i) + str("('*','*')")
            return card_string
        else:
            return super(ComputerHand, self).__repr__()
