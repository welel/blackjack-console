"""This module implements the game Blackjack. 

The game is designed in such a way that it is trying to repeat all
the processes of the real game. If in the real game a dealer has
his secret card from the initial deal, so here too. If in the real
game the table has a deck holder with several shuffled decks of cards,
so here too, and so on. Designed game has one principal difference with
mechanic in reality is random shuffling of cards (and decisions of the
dealer of course).

"""
import time

from .cards import DecksHolder, PlayerHand, DealerHand
from .ti import *


class Game():
    """This calss implements process (logic) of the game.
    
    Attributes:
        dealer (Dealer): A dealer.
        player (Player): A player.
        dealer_hand (DealerHand): A dealer's hand.
        player_hand (PlayerHand): A player's hand.
        dholder (DecksHolder): A decks holder.
        delay (int): The speed of the game. Number of seconds of 
                     the delay after printing.
    
    """
    
    def __init__(self, dealer, player, decks_number: int=6):
        self.dealer, self.player = dealer, player
        self.dealer_hand, self.player_hand = DealerHand(), PlayerHand()
        self.dholder = iter(DecksHolder(decks_number))
        self.delay = 2

    def close(self):
        """Closes the game (the exit point of game)."""
        exit_word(self.player)
        exit(1)

    def make_bet(self):
        """Asks user for bet and returns it."""
        while True:
            display_bank_info(self.dealer)
            display_bank_info(self.player)
            bet = ask_bet(self.player)
            if bet <= self.player.bank:
                self.player.bank -= bet
                self.bet = bet
                return
            elif bet <= 0:
                warn('invalid bet')
                continue
            else:
                warn('overbet')
                continue
               
    def count_winner(self, result: str):
        """Counts the winner and changes bank accounts."""
        if result == 'dealer':
            announce_winner(self.dealer)
            self.dealer.bank += self.bet
            if isinstance(self.insurance, bool):
                self.dealer.bank += self.bet // 2
        elif result == 'player':
            announce_winner(self.player)
            self.dealer.bank -= self.bet
            self.player.bank += self.bet * 2
        elif result == 'insured':
            announce_winner(self.player, result)
            self.player.bank += self.bet + self.bet // 2
        elif result == 'draw':
            announce_winner()
            self.player.bank += self.bet
        elif result == 'blackjack':
            announce_winner(self.player, result)
            self.dealer.bank -= self.bet + self.bet // 2
            self.player.bank += self.bet + self.bet // 2
        stop_on_click()
            
    def give_card(self, hand):
        """Adds one card to an user's hand."""
        hand.append(next(self.dholder))

        
    def clear_hand_states(self):
        """Clears a states of the hands."""
        self.dealer_hand.clear()
        self.player_hand.clear()
        
    def offer_insurance(self):
        """Offers the player the insurance."""
        if self.player.bank < (self.bet // 2):
            return
        while True:
            ask(str('your bet is {bet}.\nDo you insure?\n'
                    'You have {bank} coins.\n'
                   ).format(bank=self.player.bank, bet=self.bet),
                answers='(y)es / (n)o',
                user=self.player
            )
            ans = get_answer(str)
            if ans in ('y', 'yes'):
                self.insurance = True
                self.player.bank -= self.bet // 2
                return
            elif ans in ('n', 'no'):
                self.insurance = None
                return
           
    def ask_continue(self):
        """Asks the player "take/continue", BJ against dealer's Ace."""
        while True:
            ask('Take the bet back or continue?', answers='(t)ake / (c)ontinue\n')
            ans = get_answer(str)
            if ans in ('t', 'take'):
                self.player.bank += self.bet
                return 'take'
            elif ans in ('c', 'continue'):
                return 'continue'
    
    def player_decide(self):
        """The branch of player's decisions, (output/input) dialog.
        
        The player takes cards in a loop. The loop ends when either
        the player decided to stand, or the score of his hand
        reached 21+.
        
        """
        answers = ['(h)it', '(s)tand']
        if (self.bet <= self.player.bank-self.bet and
            self.bet <= self.dealer.bank-self.bet
           ):
            answers.append('(d)double')
        while True:
            print()
            answers = answers if len(self.player_hand) == 2 else answers[:2]
            ask('your move:', answers=' / '.join(answers), user=self.player)
            ans = get_answer(str)
            if ans in ('h', 'hit'):
                self.give_card(self.player_hand)
            elif ans in ('s', 'stand'):
                time.sleep(self.delay)
                return 'further'
            elif ans in ('d', 'double'):
                self.player.bank -= self.bet
                self.bet *= 2
                self.give_card(self.player_hand)
                if self.player_hand.get_score() > 21:
                    return 'dealer'
                return 'further'
            display_hands(self.dealer_hand, self.player_hand)
            if self.player_hand.get_score() > 21:
                return 'dealer'
    
    def dealer_decide(self):
        """The branch of dealer's decisions.
        
        The dealer takes cards in a loop. The loop ends when either
        the dealer reached the hand score that equals/more than player's
        hand score, or the score of the dealer's hand reached 21+.
        
        """
        self.dealer_hand.show_hidden_card()
        display_hands(self.dealer_hand, self.player_hand)
        if self.insurance and self.dealer_hand.get_score() == 21:
            return 'insured'
        time.sleep(self.delay)
        while True:
            if self.dealer_hand.get_score() > 21:
                return 'player'
            if self.dealer_hand.get_score() > self.player_hand.get_score():
                return 'dealer'
            if self.dealer_hand.get_score() == self.player_hand.get_score():
                return 'draw'
            self.give_card(self.dealer_hand)
            display_hands(self.dealer_hand, self.player_hand)
            time.sleep(self.delay)
    
    def start(self, speed=2):
        """Main loop of the game logic."""
        self.delay = speed
        greet(self.dealer, self.player)
        stop_on_click()
        
        while True:
            ask('\n'*100 + 'Press \'Enter\' to play the next hand or exit.',
                    answers='[Press \'Enter\' / (e)xit]')
            ans = get_answer(str)
            if ans in ('exit', 'e'):
                self.close()
            elif ans:
                continue 
              
            self.clear_hand_states()
            self.insurance = None
            self.make_bet()
            self.give_card(self.dealer_hand)
            self.give_card(self.dealer_hand)
            self.give_card(self.player_hand)
            self.give_card(self.player_hand)
            display_hands(self.dealer_hand, self.player_hand)
            
            if self.dealer_hand.get_score() == 11:
                self.offer_insurance()
            
            if self.player_hand.get_score() == 21:
                if self.dealer_hand.get_score() == 11:
                    ans = self.ask_continue()
                    if ans == 'take': continue
                else:
                    self.count_winner('blackjack')
                    continue
                
            if self.player_hand[0] == self.player_hand[1]:
                print('[NotImplementedYet]: ask for split\n\n')
            
            result = self.player_decide()
            if result != 'further':
                self.count_winner(result)
                continue
            
            result = self.dealer_decide()
            self.count_winner(result)
            
        return 0
