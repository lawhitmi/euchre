
class Table:
    """

    """

    def __init__(self, user, computer, bidcard=None):

        self.computer = computer
        self.user = user
        self.bidcard = bidcard
        self.trumpSuit = ""
        self.tricks = {self.user:0, self.computer: 0}

    def showTable(self, playedcard1="", playedcard2="", score=None):
        """
        Prints the playing table, Computer Hand, Field, User Hand
        :return:
        """
        print("*"*80)
        print("Score: User " + str(self.tricks[self.user]) + " Computer " + str(self.tricks[self.computer])
              + " Trump Suit: " + str(self.trumpSuit))
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

    def flipBidcard(self):
        self.bidcard = ""

    def setBidcard(self,card):
        self.bidcard = card

    def setTrumpSuit(self, suit):
        self.trumpSuit = suit

    def clearTable(self):
        self.trumpSuit = ""
        self.bidcard = ""

