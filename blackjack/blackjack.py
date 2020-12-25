'''This module implemets blackjack game.
'''

import time
from cards import DecksHolder, Card
from users import Dealer, Player



PLAYER_NAME = 'Jesse'
DEALER_NAME = 'Walter'
DELAY = 2


class Box(object):

    def __init__(self, user):
        self.user = user
        self.cards = []
        self.score = 0
        
    def __getitem__(self, slice_): return self.cards[slice_]
    def __setitem__(self, idx, card): self.cards[idx] = value
    def __len__(self): return len(self.cards)
    
    def clear(self):
        self.cards.clear()
        self.score = 0
    
    def count_score(self):
        score = 0
        for card in self.cards:
            score += card.score
        if score > 21:
            for card in self.cards:
                if card.value == 'A' and card.score > 1:
                    score -= 10
                    card.score -= 10
        self.score = score
    
    def append(self, card):
        self.score += card.score
        self.cards.append(card)
        self.count_score()
    
    def prepare_print(self):
        show_struct = []
        for_print = []
        if len(self) == 0:
            print('Empty box')
        if len(self) == 1:
            show_struct.append(Card.get_hidden_suit_struct())
        for card in self.cards:
            show_struct.append(card.get_suit_struct())
        for i in range(4):
            for j,_ in enumerate(show_struct):
                for_print.append(show_struct[j][i])
            for_print.append('\n')
        for_print.append(f' Score: {self.score}')
        return for_print
        
    def __str__(self): 
        return ''.join(self.prepare_print())


class PlayerBox(Box):  

    def __init__(self, player):
        super().__init__(player)


class DealerBox(Box):

    def __init__(self, dealer):
        super().__init__(dealer)
        self.hidden_card = None
        self.hide = True
        
    def clear(self):
        self.hidden_card = None
        self.hide = True
        super().clear()
        
    def set_hidden_card(self, card):
        self.hidden_card = card
        self.hide = True
        
    def show_hidden_card(self):
        super().append(self.hidden_card)
        self.hidden_card = None
        self.hide = False
    
    def append(self, card):
        if not self.hidden_card:
            self.set_hidden_card(card)
        else:
            super().append(card)


class Dialog(object):

    @staticmethod
    def ask(instraction: str, user_answer_type,
            answers: str='', user=None
            ):
        if user:
            print(f'{user.name}, {instraction}')
        else:
            print(instraction.capitalize())
        if answers:
            print('\tAnswers:' + answers)
        return user_answer_type(input())


class GameLogic(object):
    
    def __init__(self, dealer, player, decks_number: int=6):
        self.dealer_box = DealerBox(dealer)
        self.player_box = PlayerBox(player)
        self.dholder = iter(DecksHolder(decks_number))

    def give_card(self, box):
        box.append(next(self.dholder))
        
    def show_boxes(self, delay: int=DELAY):
        print('\n'*100 + 'Dealers hand:')
        print(self.dealer_box, end='\n\n')
        print('Players hand:')
        print(self.player_box, end='\n\n')
        time.sleep(delay)
        
    def clear_boxes_state(self):
        self.dealer_box.clear()
        self.player_box.clear()
           
    def player_decide(self):
        answers = ['(h)it', '(s)tand', '(d)double']
        while True:
            answers = answers if len(self.player_box) == 2 else answers[:2]
            ans = Dialog.ask('your move:', str, 
                ' / '.join(answers), user=self.player_box.user
                ).lower()
            if ans in ('h', 'hit'):
                self.give_card(self.player_box)
            elif ans in ('s', 'stand'):
                return
            elif ans in ('d', 'double'):
                self.give_card(self.player_box)
                return
            self.show_boxes()
            if self.player_box.score > 21:
                return 'lost'
    
    def dealer_decide(self):
        self.dealer_box.show_hidden_card()
        self.show_boxes()
        while True:
            if self.dealer_box.score > 21:
                return 'lost'
            if self.dealer_box.score > self.player_box.score:
                return 'won'
            if self.dealer_box.score == self.player_box.score:
                return 'draw'
            self.give_card(self.dealer_box)
            self.show_boxes()
    
    def start(self):
        dealer_box = self.dealer_box
        player_box = self.player_box
        print('\n'*100 + '\n\n\nGame is started...\n'\
              f'Hello, {self.player_box.user.name}!\n'\
              f'I\'m {self.dealer_box.user.name}, your dealer for today.\n'\
              'Let\'s have some fun!\n\n'
              )
        time.sleep(2)
        
        while True:
            ans = Dialog.ask('\n'*100 + 'press \'Enter\' to play the next hand'\
                             ' or exit.', str,
                             answers='[Press \'Enter\' / (e)xit]'
                             ).lower()
            if ans in ('exit', 'e'): break
            elif ans: continue 
              
            self.clear_boxes_state()
            self.give_card(dealer_box)
            self.give_card(dealer_box)
            self.give_card(player_box)
            self.give_card(player_box)
            
            self.show_boxes()
            
            if dealer_box.score == 11:
                print('[NotImplementedYet]: ask for insurance\n\n')
            
            if player_box.score == 21:
                print('Black Jack!\n You\'r won!\n\n')
                input('\nPress \'Enter\' to continue...')
                continue
                
            if player_box.cards[0] == player_box.cards[1]:
                print('[NotImplementedYet]: ask for split\n\n')
            
            result = self.player_decide()
            if result == 'lost':
                print('PLAYER LOST')
                input('\nPress \'Enter\' to continue...')
                continue
            
            result = self.dealer_decide()
            if result == 'lost':
                print('DEALER LOST')
            elif result == 'won':
                print('DEALER WON')
            elif result == 'draw':
                print('DRAW')
    
            input('\nPress \'Enter\' to continue...')
        return 0


class Game(object):

    def __init__(self, logic):
        self.logic = logic
        self.menu = GameMenu()

    def close(self):
        print('Thanks for game')
        exit(1)

    def run(self):
        pass


if __name__ == '__main__':
    dealer = Dealer(DEALER_NAME, 1000000)
    player = Player(PLAYER_NAME, 50000)

    glogic = GameLogic(dealer, player)
    glogic.start()
