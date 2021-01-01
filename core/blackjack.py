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



def ask(instraction: str, answer_type,
            answers: str='', placeholder: str='',
            user=None
    ):
    """Asks a user a question and returns his answer.
    
    Args:
        instraction (str): A question or an instractions for user.
        answer_type (type): Expected answer type to return. 
        answers (str): A represent of available answers.
        placeholder (str): A placeholder for input() func.
        user (BaseUser): A user who is being asked.
    
    """
    while True:
        if user:
            print(user.name + ',', instraction)
        else:
            print(instraction)
        if answers:
            print('\tAnswers:' + answers)
        try:
            ans = answer_type(input(placeholder))
        except ValueError:
            print(f'Use {answer_type} type for answering.')
            continue
        return ans


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
        print(f'\nThank you for the game, {self.player.name}!\n')
        exit(1)

    def make_bet(self):
        """Asks user for bet and returns it."""
        while True:
            print('\n'*100 + 'Dealer have {bank} coins.\n'.format(
                    bank=self.dealer.bank)
            )
            ans = ask(f'you have {self.player.bank} coins. Make a bet.\n', int,
                        placeholder='Bet: ', user=self.player)
            if ans <= self.player.bank:
                self.player.bank -= ans
                self.bet = ans
                return
            else:
                print('\n'*100+'You bet a lot, you don\'t have that much.\n',
                        'Bet less.\n')
                continue
               
    def count_winner(self, winner: str):
        """Counts the winner and changes bank accounts."""
        if winner == 'dealer':
            print('You\'r lost!\n\n')
            self.dealer.bank += self.bet
            if isinstance(self.insurance, bool):
                self.dealer.bank += self.bet // 2
        elif winner == 'player':
            print('You\'r won!\n\n')
            self.dealer.bank -= self.bet
            self.player.bank += self.bet * 2
        elif winner == 'insurance':
            print('You insured the hand.\n\n')
            self.player.bank += self.bet + self.bet // 2
        elif winner == 'draw':
            print('Draw!\n\n')
            self.player.bank += self.bet
        elif winner == 'blackjack':
            print('Blackjack!\n\n')
            self.dealer.bank -= self.bet + self.bet // 2
            self.player.bank += self.bet + self.bet // 2
        input('\nPress \'Enter\' to continue...')
            
    def give_card(self, hand):
        """Adds one card to a user's hand."""
        hand.append(next(self.dholder))
        
    def print_hands(self):
        """Prints a state of the hands in the console."""
        print('\n'*100 + 'Dealers hand:')
        print(self.dealer_hand.to_str(), end='\n\n')
        print('Players hand:')
        print(self.player_hand.to_str(), end='\n\n')
        
    def clear_hand_states(self):
        """Clears a states of the hands."""
        self.dealer_hand.clear()
        self.player_hand.clear()
        
    def ask_insurance(self):
        """Asks the player for insurance."""
        if self.player.bank < (self.bet // 2):
            return
        while True:
            ans = ask('your bet is {bet}.\nDo you insure?\n'\
                      'You have {bank} coins.\n'.format(
                            bank=self.player.bank, bet=self.bet
                        ),
                        str, answers='(y)es / (n)o', user=self.player
            )
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
            ans = ask('Take back (1 to 1) or continue?', str,
                       answers='(t)ake / (c)ontinue\n'
            ).lower()
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
            ans = ask('your move:', str, 
                ' / '.join(answers), user=self.player
                ).lower()
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
            self.print_hands()
            if self.player_hand.get_score() > 21:
                return 'dealer'
    
    def dealer_decide(self):
        """The branch of dealer's decisions.
        
        The dealer takes cards in a loop. The loop ends when either
        the dealer reached the hand score that equals/more than player's
        hand score, or the score of the dealer's hand reached 21+.
        
        """
        self.dealer_hand.show_hidden_card()
        self.print_hands()
        if self.insurance and self.dealer_hand.get_score() == 21:
            return 'insurance'
        time.sleep(self.delay)
        while True:
            if self.dealer_hand.get_score() > 21:
                return 'player'
            if self.dealer_hand.get_score() > self.player_hand.get_score():
                return 'dealer'
            if self.dealer_hand.get_score() == self.player_hand.get_score():
                return 'draw'
            self.give_card(self.dealer_hand)
            self.print_hands()
            time.sleep(self.delay)
    
    def start(self, speed=2):
        """Main loop of the game logic."""
        self.delay = speed
        print('\n'*100,
              '='*10 + '   $   WELCOME TO   $   ' + '='*10 + '\n',
              '='*10 + ' Best Console BlackJack ' + '='*10 + '\n',
              f'\n\tHello, {self.player.name}!\t\n',
              f'\tI\'m {self.dealer.name}, your dealer for today.\n',
              '\tLet\'s have some fun!\n\n',
              '='*45 + '\n\n'
        )
        input('\nPress \'Enter\' to continue...')
        
        while True:
            ans = ask('\n'*100 + 'Press \'Enter\' to play the next hand'\
                             ' or exit.', str,
                             answers='[Press \'Enter\' / (e)xit]'
            ).lower()
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
            self.print_hands()
            
            if self.dealer_hand.get_score() == 11:
                self.ask_insurance()
            
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
            
            winner = self.dealer_decide()
            self.count_winner(winner)
            
        return 0
