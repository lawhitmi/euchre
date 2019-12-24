from random import randint
from table import Table
from deck import CardDeck
from hands import ComputerHand, UserHand
import time


def pickDealer():
    """

    :return:
    """
    isuserdealer = bool(randint(0, 1))
    iscomputerdealer = not isuserdealer
    return tuple((isuserdealer, iscomputerdealer))


def game():
    """

    :return:
    """
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
        maker.setMaker()
        tricks = {user: 0, computer: 0}
        trickwinner, points = trickPhase(nondealer, dealer, trumpsuit, table)
        table.tricks[trickwinner] += points
        # tricks[trickwinner] += points
        print(tricks[trickwinner])
        if tricks[trickwinner] >= 10:
            # TODO create declare winner screen
            print(trickwinner.name + 'wins!')
            break

        # Reset everything for next round
        deck.shuffle()
        user.clearHand()
        computer.clearHand()
        dealermask = pickDealer()
        if dealermask[0]:
            user.setDealer()
        else:
            computer.setDealer()
        table.clearTable()
        table.setBidcard(deck.deal(player='n'))
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
    nonDealDec = nondealer.bidDecide()
    if nonDealDec == 'order-up':
        # TODO allow dealer the option to pick up the bidcard in this case
        table.flipBidcard()
        return tuple((bidcard.suit, nondealer))
    elif nonDealDec == 'pass':
        table.showTable()
        dealerDec = dealer.bidDecide()
        if dealerDec == 'accept':
            # TODO accepted card should enter hand, and allow user to choose a card to discard (also need to call flipBidcard here
            table.flipBidcard()
            return tuple((bidcard.suit, dealer))
        elif dealerDec == 'pass':
            table.flipBidcard()
            table.showTable()
            nonDealDec = nondealer.bidDecide(rnd=2)
            if nonDealDec != 'pass':
                return tuple((nonDealDec, nondealer))
            else:
                table.showTable()
                dealerDec = dealer.bidDecide(rnd=2)
                return tuple((dealerDec, dealer))


def trickPhase(firstplayer, secondplayer, trump, table, score={}):
    if len(score) == 0:
        score = {firstplayer: 0, secondplayer: 0}
    winner = checkForWinner(score)
    if winner:
        return tuple((winner[0], winner[1]))
    # TODO BUG HERE - It's asking to play a card when all cards are played
    table.showTable(score=score)
    card1 = firstplayer.trickDecide()
    table.showTable(card1,score=score)
    card2 = secondplayer.trickDecide(card1)
    table.showTable(card1, card2, score=score)
    time.sleep(1)
    if card2 > card1:
        score[secondplayer] += 1
        trickwinner, points = trickPhase(secondplayer, firstplayer, trump, table, score)
        return tuple((trickwinner, points))
    else:
        score[firstplayer] += 1
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
            if j == 3:
                return tuple((i, 1))


if __name__ == '__main__':
    game()
