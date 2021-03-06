from random import randint
from .table import Table
from .deck import CardDeck
from .hands import ComputerHand, UserHand
import time


def pick_dealer():
    """
    Randomly chooses a dealer to start the game
    :return: tuple of bool (mask)
    """
    is_user_dealer = bool(randint(0, 1))
    is_computer_dealer = not is_user_dealer
    return tuple((is_user_dealer, is_computer_dealer))


def next_round_reset(deck, user, computer, table):
    """
    Function to reset state for start of next round
    :param deck: Deck type
    :param user: Userhand type
    :param computer: ComputerHand type
    :param table: Table type
    :return: None
    """
    deck.shuffle()
    userdealer = user.dealer
    user.clear_hand()
    computer.clear_hand()
    if not userdealer:
        user.set_dealer()
    else:
        computer.set_dealer()
    table.clear_table()
    bidcard = deck.deal(player='n')
    table.set_bidcard(bidcard)
    user.set_cards(deck.deal(player='y'))
    computer.set_cards(deck.deal(player='y'))


def game():
    """
    Main Game Function
    """
    # Ask user if they'd like to play or learn
    play_mode = input("Would you like to play in learning mode? (Y or N)")
    if play_mode.lower() == 'y':
        learn = True
    elif play_mode.lower() == 'n':
        learn = False

    # Initial setup
    deck = CardDeck(learner=learn)
    dealermask = pick_dealer()
    user = UserHand(dealerflag=dealermask[0], cards=deck.deal(player='y'))
    computer = ComputerHand(dealerflag=dealermask[1], cards=deck.deal(player='y'), play_mode=learn)
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
        table.set_trumpsuit(trumpsuit)
        user.set_values(basevaluereset=True)
        computer.set_values(basevaluereset=True)
        user.set_values(trumpsuit=trumpsuit, evaltrumpsuit=True)
        computer.set_values(trumpsuit=trumpsuit, evaltrumpsuit=True)
        maker.set_maker()

        trickwinner, points = trick_phase(nondealer, dealer, trumpsuit, table)
        table.tricks[trickwinner] += points
        if table.tricks[trickwinner] >= 10:
            print(str(trickwinner.name) + ' wins!')
            break
        # Reset everything for next round
        next_round_reset(user=user, computer=computer, deck=deck, table=table)


def bid_phase(nondealer, dealer, bidcard, table):
    """
    Controls overall bid phase of game.
    :param nondealer: 'Hand' type
    :param dealer: 'Hand' type
    :param bidcard: 'Card' type
    :param table: 'Table' type
    :return: tuple (string trumpsuit, 'Hand' maker)
    """
    table.show_table()
    non_dealer_decision = nondealer.bid_decide(bidcard=bidcard)
    if non_dealer_decision == 'order-up':
        table.flip_bidcard()
        dealer.pickup_bidcard(bidcard)
        return tuple((bidcard.suit, nondealer))
    elif non_dealer_decision == 'pass':
        table.show_table()
        dealer_decision = dealer.bid_decide(bidcard=bidcard)
        if dealer_decision == 'accept':
            table.flip_bidcard()
            return tuple((bidcard.suit, dealer))
        elif dealer_decision == 'pass':
            table.flip_bidcard()
            table.show_table()
            non_dealer_decision = nondealer.bid_decide(rnd=2, excludesuit=bidcard.get_suit())
            if non_dealer_decision != 'pass':
                return tuple((non_dealer_decision, nondealer))
            else:
                table.show_table()
                dealer_decision = dealer.bid_decide(rnd=2, excludesuit=bidcard.get_suit())
                return tuple((dealer_decision, dealer))


def trick_phase(firstplayer, secondplayer, trump, table, score={}):
    """
    Controls overall trick phase of game.
    :param firstplayer: 'Hand' type  Which player leads
    :param secondplayer: 'Hand' type Which player follows
    :param trump: string suit of trump
    :param table: Table type
    :param score: dict {'Hand': int}  for trick
    :return: tuple('Hand' winner, int #points to award)
    """
    if len(score) == 0:
        score = {firstplayer: 0, secondplayer: 0}
    winner = check_for_winner(score)

    if winner:
        return tuple((winner[0], winner[1]))

    firstplayer.set_values(trumpsuit=trump, resetval=True)
    secondplayer.set_values(trumpsuit=trump, resetval=True)

    table.show_table(score=score)

    card1 = firstplayer.trick_decide()

    firstplayer.set_values(trumpsuit=trump, leadsuit=card1.get_suit())
    card1.set_value(trumpsuit=trump, leadsuit=card1.get_suit())
    secondplayer.set_values(trumpsuit=trump, leadsuit=card1.get_suit())

    table.show_table(card1, score=score)

    card2 = secondplayer.trick_decide(playedcard=card1)

    if card2 > card1:
        score[secondplayer] += 1
        table.show_table(card1, card2, score=score)
        time.sleep(1)
        trickwinner, points = trick_phase(secondplayer, firstplayer, trump, table, score)
        return tuple((trickwinner, points))
    else:
        score[firstplayer] += 1
        table.show_table(card1, card2, score=score)
        time.sleep(1)
        trickwinner, points = trick_phase(firstplayer, secondplayer, trump, table, score)
        return tuple((trickwinner, points))


def check_for_winner(score):
    """
    Evaluates score dict to see if there is a winner
    :param score: dict {'Hand':points}
    :return: tuple('Hand',points to award)
    """
    for i, j in score.items():
        if not i.maker and j == 3:
            return tuple((i, 2))  # Euchred opponent
        elif j == 5:
            return tuple((i, 2))  # Maker took all 5
        elif sum(score.values()) == 5 and j >= 3:
            return tuple((i, 1))


if __name__ == "__main__":
    game()
