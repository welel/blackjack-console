"""This module implements the game Blackjack. 

The game is designed in such a way that it is trying to repeat all
the processes of the real game. If in the real game a dealer has
his secret card from the initial deal, so here too. If in the real
game the table has a deck holder with several shuffled decks of cards,
so here too, and so on. Designed game has one principal difference with
mechanic in reality is random shuffling of cards (and decisions of the
dealer of course).

TODO:
    * Slahs Ace represent (14/3).
    * Keylook.

"""

import time

from .cards import DecksHolder, CARD_BACK_STRUCT



def ask(instraction: str, answer_type,
            answers: str='', placeholder='',
            user=None
    ):
    """Asks a user a question and returns his answer.
    
    Args:
        instraction (str): A question or an instractions for user.
        answer_type (*): Expected answer type to return. 
        answers (str): A represent of available answers.
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


class Box():
    """This class implements the hand and links it with the user.
    
    This class is parent for the dealer's box and the player's box.
    The box has the hand that collects the dealt cards. Each card has
    a value. A score stores sum of that values.
    
    Attributes:
        user (BaseUser): A user that linked to the box.
        cards (list): Dealt cards.
        score (int): A value of the hand.
    
    """

    def __init__(self, user):
        self.user = user
        self.cards = []
        self.score = 0
        
    def __getitem__(self, slice_):
        return self.cards[slice_]

    def __setitem__(self, idx, card):
        self.cards[idx] = card

    def __len__(self):
        return len(self.cards)
    
    def clear(self):
        """Clears cards from a hand and the score.""" 
        self.cards.clear()
        self.score = 0
    
    def count_score(self):
        """Counts the score of a box and updates attribute 'score'.
        
        By default the score is sum of values of hand's cards. But one
        card has multiple value that calculates in favor of a user.
        The card Ace can be 11 or 1. If the score is more than 21, then
        Ace will change its value if it in the hand.
        
        """
        score = 0
        for card in self.cards:
            score += card.value
        if score > 21:
            for card in self.cards:
                if card.rank == 'A' and card.value > 1:
                    score -= 10
                    card.value -= 10
        self.score = score
    
    def append(self, card):
        """Adds a card and calls recount score function."""
        self.score += card.value
        self.cards.append(card)
        self.count_score()
    
    def prepare_print(self):
        """Prepares list of strs for print the hand in the console."""
        show_struct = []
        for_print = []
        if len(self) == 0:
            print('Empty box')
        for card in self.cards:
            show_struct.append(card.get_repr_struct())
        if len(show_struct) == 1:
            show_struct.append(CARD_BACK_STRUCT)
        for i in range(4):
            for j,_ in enumerate(show_struct):
                for_print.append(show_struct[j][i])
            for_print.append('\n')
        for_print.append(f' Score: {self.score}')
        return for_print
        
    def __str__(self): 
        return ''.join(self.prepare_print())


class PlayerBox(Box):  
    """This class represents a player's box.
    
    """
    
    def __init__(self, player):
        super().__init__(player)


class DealerBox(Box):
    """This class represents a dealer's box.
    
    A dealer's box extends Box and has additional functionality which
    implements dealer's ability to hide his first card on initial deal.
    After player's decisions the hidden card of a dealer opens.
    
    Attributes:
        hidden_card (Card): A hidden card of a dealer.
        hide (bool): A flag, tells when show card.
    
    """

    def __init__(self, dealer):
        super().__init__(dealer)
        self.hidden_card = None
        self.hide = True
        
    def clear(self):
        """Clears cards (including hidden) and score of the box."""
        self.hidden_card = None
        self.hide = True
        super().clear()
        
    def set_hidden_card(self, card):
        self.hidden_card = card
        self.hide = True
        
    def show_hidden_card(self):
        """Appends the hidden card to countable cards."""
        self.append(self.hidden_card)
    
    def append(self, card):
        """Appends a card to dealer's box.
        
        First appened card always goes like hidden.
        
        """
        if not self.hidden_card:
            self.set_hidden_card(card)
        else:
            super().append(card)


class Game():
    """This calss implements process (logic) of the game.
    
    Attributes:
        dealer_box (PlayerBox): A dealer's box.
        player_box (DealerBox): A player's box.
        dholder (DecksHolder): A decks holder.
        delay (int): The speed of the game. Number of seconds of 
                     the delay after printing.
    
    """
    
    def __init__(self, dealer, player, decks_number: int=6):
        self.dealer_box = DealerBox(dealer)
        self.player_box = PlayerBox(player)
        self.dholder = iter(DecksHolder(decks_number))
        self.delay = 2

    def close(self):
        """Closes the game (the exit point of game)."""
        print('\nThank you for the game,',
            self.player_box.user.name + '!\n'
        )
        exit(1)

    def make_bet(self):
        """Asks user for bet and returns it."""
        while True:
            print('\n'*100 + 'Dealer have {bank} coins.\n'.format(
                bank=self.dealer_box.user.bank)
            )
            ans = ask('you have {bank} coins. Make a bet.\n'.format(
                        bank=self.player_box.user.bank), int,
                    placeholder='Bet: ', user=self.player_box.user
            )
            if ans <= self.player_box.user.bank:
                self.player_box.user.bank -= ans
                self.bet = ans
                return
            else:
                print('\n'*100+'You bet a lot, you don\'t have that much.\n',
                    'Bet less.\n')
                continue
               
    def count_winner(self, winner: str):
        """Counts the winner and changes bank accounts."""
        if winner != 'draw':
            if winner == 'dealer':
                print('You\'r lost!\n\n')
                self.dealer_box.user.bank += self.bet
                if isinstance(self.insurance, bool):
                    self.dealer_box.user.bank += self.bet // 2
            elif winner == 'player':
                print('You\'r won!\n\n')
                self.dealer_box.user.bank -= self.bet
                self.player_box.user.bank += self.bet * 2
            elif winner == 'insurance':
                self.player_box.user.bank += self.bet + self.bet // 2
            input('\nPress \'Enter\' to continue...')
            
                

    def give_card(self, box):
        """Adds one card to a user's box."""
        box.append(next(self.dholder))
        
    def print_boxes(self):
        """Prints a state of the boxes in the console."""
        print('\n'*100 + 'Dealers hand:')
        print(self.dealer_box, end='\n\n')
        print('Players hand:')
        print(self.player_box, end='\n\n')
        
    def clear_boxes_state(self):
        """Clears a state of the boxes."""
        self.dealer_box.clear()
        self.player_box.clear()
        
    def ask_insurance(self):
        """Asks the player for insurance."""
        if self.dealer_box.user.bank < (self.bet // 2):
            return
        while True:
            ans = ask('your bet is {bet}.\nDo you insure?\n'\
                      'You have {bank} coins.\n'.format(
                        bank=self.player_box.user.bank,
                        bet=self.bet
                        ), 
                        str,
                        answers='(y)es / (n)o',
                        user=self.player_box.user
            )
            if ans in ('y', 'yes'):
                self.insurance = True
                self.player_box.user.bank -= self.bet // 2
                return
            elif ans in ('n', 'no'):
                self.insurance = None
                return
           
    def player_decide(self):
        """The branch of player's decisions, (output/input) dialog.
        
        The player takes cards in a loop. The loop ends when either
        the player decided to stand, or the score of the box
        reached 21+.
        
        """
        answers = ['(h)it', '(s)tand']
        if (self.bet <= self.player_box.user.bank-self.bet and
            self.bet <= self.dealer_box.user.bank-self.bet
           ):
            answers.append('(d)double')
        while True:
            print()
            answers = answers if len(self.player_box) == 2 else answers[:2]
            ans = ask('your move:', str, 
                ' / '.join(answers), user=self.player_box.user
                ).lower()
            if ans in ('h', 'hit'):
                self.give_card(self.player_box)
            elif ans in ('s', 'stand'):
                time.sleep(self.delay)
                return 'further'
            elif ans in ('d', 'double'):
                self.player_box.user.bank -= self.bet
                self.bet *= 2
                self.give_card(self.player_box)
                if self.player_box.score > 21:
                    return 'dealer'
                return 'further'
            self.print_boxes()
            if self.player_box.score > 21:
                return 'dealer'
    
    def dealer_decide(self):
        """The branch of dealer's decisions.
        
        The dealer takes cards in a loop. The loop ends when either
        the dealer reached the box score that equals/more than player's
        box score, or the score of the dealer's box reached 21+.
        
        """
        self.dealer_box.show_hidden_card()
        self.print_boxes()
        if self.insurance and self.dealer_box.score == 21:
            return 'insurance'
        time.sleep(self.delay)
        while True:
            if self.dealer_box.score > 21:
                return 'player'
            if self.dealer_box.score > self.player_box.score:
                return 'dealer'
            if self.dealer_box.score == self.player_box.score:
                return 'draw'
            self.give_card(self.dealer_box)
            self.print_boxes()
            time.sleep(self.delay)
    
    def start(self, speed=2):
        """Main loop of the game logic."""
        
        self.delay = speed
        dealer_box = self.dealer_box
        player_box = self.player_box
        print('\n'*100,
              '='*10 + '   $   WELCOME TO   $   ' + '='*10 + '\n',
              '='*10 + ' Best Console BlackJack ' + '='*10 + '\n',
              f'\n\tHello, {self.player_box.user.name}!\t\n',
              f'\tI\'m {self.dealer_box.user.name}, your dealer for today.\n',
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
              
            self.clear_boxes_state()
            self.insurance = None
            self.make_bet()
            self.give_card(dealer_box)
            self.give_card(dealer_box)
            self.give_card(player_box)
            self.give_card(player_box)
            self.print_boxes()
            
            if dealer_box.score == 11:
                self.ask_insurance()
            
            if player_box.score == 21:
                print('Black Jack!\n')
                self.count_winner('player')
                continue
                
            if player_box.cards[0] == player_box.cards[1]:
                print('[NotImplementedYet]: ask for split\n\n')
            
            result = self.player_decide()
            if result != 'further':
                self.count_winner(result)
                continue
            
            winner = self.dealer_decide()
            self.count_winner(winner)
            
        return 0
