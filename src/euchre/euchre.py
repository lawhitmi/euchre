from random import randint
from .table import Table
from .deck import CardDeck
from .hands import ComputerHand, UserHand
import time


def pick_dealer():
    """

    :return:
    """
    is_user_dealer = bool(randint(0, 1))
    is_computer_dealer = not is_user_dealer
    return tuple((is_user_dealer, is_computer_dealer))


def next_round_reset(deck, user, computer, table):
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


def game():
    # Initial setup
    deck = CardDeck()
    dealermask = pick_dealer()
    user = UserHand(dealerflag=dealermask[0], cards=deck.deal(player='y'))
    computer = ComputerHand(dealerflag=dealermask[1], cards=deck.deal(player='y'))
    bidcard = deck.deal(player='n')
    table = Table(user, computer, bidcard)

    # main game loop
    while True:

        if user.dealer:
            dealer = user
            nondealer = computer
        else:
            dealer = computer
            nondealer = user

        trumpsuit, maker = bid_phase(nondealer, dealer, bidcard, table)
        table.setTrumpSuit(trumpsuit)
        user.setValues(basevaluereset=True)
        computer.setValues(basevaluereset=True)
        user.setValues(trumpsuit=trumpsuit, evaltrumpsuit=True)
        computer.setValues(trumpsuit=trumpsuit, evaltrumpsuit=True)
        maker.setMaker()

        trickwinner, points = trick_phase(nondealer, dealer, trumpsuit, table)
        table.tricks[trickwinner] += points
        if table.tricks[trickwinner] >= 10:
            print(str(trickwinner.name) + ' wins!')
            break
        # Reset everything for next round
        next_round_reset(user=user, computer=computer, deck=deck, table=table)


def bid_phase(nondealer, dealer, bidcard, table):
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


def trick_phase(firstplayer, secondplayer, trump, table, score={}):

    if len(score) == 0:
        score = {firstplayer: 0, secondplayer: 0}
    winner = check_for_winner(score)

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
        trickwinner, points = trick_phase(secondplayer, firstplayer, trump, table, score)
        return tuple((trickwinner, points))
    else:
        score[firstplayer] += 1
        table.showTable(card1, card2, score=score)
        time.sleep(1)
        trickwinner, points = trick_phase(firstplayer, secondplayer, trump, table, score)
        return tuple((trickwinner, points))


def check_for_winner(score):
    for i, j in score.items():
        if not i.maker and j == 3:
            return tuple((i, 2))  # Euchred opponent
        elif j == 5:
            return tuple((i, 2))  # Maker took all 5
        elif sum(score.values()) == 5 and j >= 3:
            return tuple((i, 1))


if __name__ == "__main__":
    game()
