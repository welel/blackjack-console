"""This module starts the game blackjack.

You can fill the constants below (player name, and dealer name).
SPEED is a delay (sec) between printing of states of hands.

Note:
    Than more SPEED than game is slower. The best values is 0-4.

"""

from core.blackjack import Game
from core.users import Dealer, Player



PLAYER_NAME = 'Jesse'
DEALER_NAME = 'Walter'
SPEED = 2


if __name__ == '__main__':
    dealer = Dealer(DEALER_NAME)
    player = Player(PLAYER_NAME)
    game = Game(dealer, player)
    game.start(speed=SPEED)
