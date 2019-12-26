from random import randint
from .table import Table
from .deck import CardDeck
from .hands import ComputerHand, UserHand
import time


def pickDealer():
    """

    :return:
    """
    isuserdealer = bool(randint(0, 1))
    iscomputerdealer = not isuserdealer
    return tuple((isuserdealer, iscomputerdealer))


def game():
    deck = CardDeck()
    dealermask = pickDealer()
    user = UserHand(dealerflag=dealermask[0], cards=deck.deal(player='y'))
    computer = ComputerHand(dealerflag=dealermask[1], cards=deck.deal(player='y'))
    bidcard = deck.deal(player='n')
    table = Table(user, computer, bidcard)

    while True:

        if user.dealer:
            dealer = user
            nondealer = computer
        else:
            dealer = computer
            nondealer = user

        trumpsuit, maker = bidPhase(nondealer, dealer, bidcard, table)
        table.setTrumpSuit(trumpsuit)
        user.setValues(basevaluereset=True)
        computer.setValues(basevaluereset=True)
        user.setValues(trumpsuit=trumpsuit, evaltrumpsuit=True)
        computer.setValues(trumpsuit=trumpsuit, evaltrumpsuit=True)
        maker.setMaker()

        trickwinner, points = trickPhase(nondealer, dealer, trumpsuit, table)
        table.tricks[trickwinner] += points
        if table.tricks[trickwinner] >= 10:
            print(str(trickwinner.name) + ' wins!')
            break

        # Reset everything for next round
        deck.shuffle()
        userdealer = user.dealer
        user.clearHand()
        computer.clearHand()
        if not userdealer:
            user.setDealer()
        else:
            computer.setDealer()
        table.clearTable()
        bidcard = deck.deal(player='n')
        table.setBidcard(bidcard)
        user.setCards(deck.deal(player='y'))
        computer.setCards(deck.deal(player='y'))


def bidPhase(nondealer, dealer, bidcard, table):
    """

    :param nondealer:
    :param dealer:
    :param bidcard:
    :param table:
    :return:
    """
    table.showTable()
    nonDealDec = nondealer.bidDecide(bidcard=bidcard)
    if nonDealDec == 'order-up':
        table.flipBidcard()
        dealer.pickUpBidcard(bidcard)
        return tuple((bidcard.suit, nondealer))
    elif nonDealDec == 'pass':
        table.showTable()
        dealerDec = dealer.bidDecide(bidcard=bidcard)
        if dealerDec == 'accept':
            table.flipBidcard()
            return tuple((bidcard.suit, dealer))
        elif dealerDec == 'pass':
            table.flipBidcard()
            table.showTable()
            nonDealDec = nondealer.bidDecide(rnd=2, excludesuit=bidcard.getSuit())
            if nonDealDec != 'pass':
                return tuple((nonDealDec, nondealer))
            else:
                table.showTable()
                dealerDec = dealer.bidDecide(rnd=2, excludesuit=bidcard.getSuit())
                return tuple((dealerDec, dealer))


def trickPhase(firstplayer, secondplayer, trump, table, score={}):

    if len(score) == 0:
        score = {firstplayer: 0, secondplayer: 0}
    winner = checkForWinner(score)

    if winner:
        return tuple((winner[0], winner[1]))

    firstplayer.setValues(trumpsuit=trump, resetval=True)
    secondplayer.setValues(trumpsuit=trump, resetval=True)

    table.showTable(score=score)

    card1 = firstplayer.trickDecide()

    firstplayer.setValues(trumpsuit=trump, leadsuit=card1.getSuit())
    card1.setValue(trumpsuit=trump, leadsuit=card1.getSuit())
    secondplayer.setValues(trumpsuit=trump, leadsuit=card1.getSuit())

    table.showTable(card1, score=score)

    card2 = secondplayer.trickDecide(playedcard=card1)

    if card2 > card1:
        score[secondplayer] += 1
        table.showTable(card1, card2, score=score)
        time.sleep(1)
        trickwinner, points = trickPhase(secondplayer, firstplayer, trump, table, score)
        return tuple((trickwinner, points))
    else:
        score[firstplayer] += 1
        table.showTable(card1, card2, score=score)
        time.sleep(1)
        trickwinner, points = trickPhase(firstplayer, secondplayer, trump, table, score)
        return tuple((trickwinner, points))


def checkForWinner(score):
    for i, j in score.items():
        if not i.maker:
            if j == 3:
                return tuple((i, 2))  # Euchred opponent
        else:
            if j == 5:
                return tuple((i, 2))  # Maker took all 5

    if sum(score.values()) == 5:
        for i, j in score.items():
            if j >= 3:
                return tuple((i, 1))


if __name__ == "__main__":
    game()
