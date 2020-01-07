
class Table:
    """
    Controls the table printout and trick scoring
    """

    def __init__(self, user, computer, bidcard=None):

        self.computer = computer
        self.user = user
        self.bidcard = bidcard
        self.trumpsuit = ""
        self.tricks = {self.user: 0, self.computer: 0}

    def show_table(self, playedcard1="", playedcard2="", score=None):
        """
        Prints the playing table, Computer Hand, Field, User Hand, Scores, etc.
        :param playedcard1: Card type Card played by first player
        :param playedcard2: Card type Card played by second player
        :param score: dict Individual trick score
        :return: None
        """
        print("*"*80)
        print("Score: User " + str(self.tricks[self.user]) + " Computer " + str(self.tricks[self.computer])
              + " Trump Suit: " + str(self.trumpsuit))
        scoreline = ""
        if score:
            scoreline += "Hand Score: "
            for i, j in score.items():
                scoreline += str(i.name + ": " + str(j) + "  ")
            print(scoreline)
        print(self.computer)
        if playedcard1:
            if playedcard2:
                print(str(playedcard1) + " " + str(playedcard2))
            else:
                print(playedcard1)
        elif self.bidcard:
            print("Bidcard: " + str(self.bidcard))
        else:
            print("")
        print(self.user)

    def flip_bidcard(self):
        """
        Removes bidcard when not picked up
        :return: None
        """
        self.bidcard = ""

    def set_bidcard(self, card):
        """
        Setter method for storing the card on which to bid.
        :param card: Card type
        :return: None
        """
        self.bidcard = card

    def set_trumpsuit(self, suit):
        """
        Setter method for trick phase trumpsuit
        :param suit: string i.e. 'Spades'
        :return: None
        """
        self.trumpsuit = suit

    def clear_table(self):
        """
        Resets table for next round
        :return: None
        """
        self.trumpsuit = ""
        self.bidcard = ""

