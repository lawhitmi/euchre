from src.euchre.hands import UserHand, ComputerHand
from src.euchre.deck import CardDeck
from random import randint


def pickDealer():
    """

    :return:
    """
    isuserdealer = bool(randint(0, 1))
    iscomputerdealer = not isuserdealer
    return tuple((isuserdealer, iscomputerdealer))


class Euchre:
    """

    """

    def __init__(self):
        dealermask = pickDealer()
        self.user = UserHand(dealerflag=dealermask[0])
        self.computer = ComputerHand(dealerflag=dealermask[1])
        self.tricks = {}
        self.bidCard = {}
        self.trumpSuit = ""
        self.maker = ""
        self.lastWinner = ""
        self.play()

    def showTable(self):
        """
        Prints the playing table, Computer Hand, Field, User Hand
        :return:
        """
        print(str(self.computer))
        print(str(self.bidCard[1]))
        print(str(self.user))

    def play(self):
        """

        :return:
        """
        while 10 not in self.tricks.values():
            deck = CardDeck()
            self.bidCard = deck.deal(player='n')
            self.user.setCards(deck.deal(player='y'))
            self.computer.setCards(deck.deal(player='y'))
            self.trumpSuit, self.maker = self.bidPhase(self.user, self.computer)
            self.maker.setMaker()
            self.lastWinner = self.trickPhase()
            break

    def bidPhase(self, player1, player2):
        """
        Controls the bidding phase and determines the trump suit
        :param dealer:
        :param nondealer:
        :return:
        """
        if player1.dealer:
            dealer = player1
            nondealer = player2
        elif player2.dealer:
            dealer = player2
            nondealer = player1
        self.showTable()
        nondealer.setValues(self.bidCard[1].suit)
        dealer.setValues(self.bidCard[1].suit)
        nonDealDec = nondealer.bidDecide()
        if nonDealDec == 'order-up':
            return tuple((self.bidCard[1].suit, nonDealDec))
        elif nonDealDec == 'pass':
            self.showTable()
            dealerDec = dealer.bidDecide()
            if dealerDec == 'accept':
                return tuple((self.bidCard[1].suit, dealer))
            elif dealerDec == 'pass':
                self.showTable()
                nonDealDec2 = nondealer.bidDecide(rnd=2)
                if nonDealDec2 != 'pass':
                    return tuple((nonDealDec2, nondealer))
                else:
                    self.showTable()
                    dealerDec2 = dealer.bidDecide(rnd=2)
                    return tuple((dealerDec2, dealer))

    def trickPhase(self, maker, nonmaker):
        """

        :param maker:
        :param nonmaker:
        :return:
        """
        # TODO Implement trickPhase
        NotImplemented


if __name__ == '__main__':
    C = Euchre()
