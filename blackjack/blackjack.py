'''This module implemets blackjack game.
'''

import time
from cards import DecksHolder, Card
from users import Dealer, Player



class Box(object):

    def __init__(self, user):
        self.user = user
        self.cards = []
        self.score = 0
        
    def __getitem__(self, slice_): return self.cards[slice_]
    def __setitem__(self, idx, card): self.cards[idx] = value
    
    def append(self, card):
        self.score += card.score
        self.cards.append(card)
        
    def __str__(self, secret=False): 
        if len(self.cards) == 0:
            return 'Empty box'
        show_struct = []
        for_print = []
        if secret:
            show_struct.append(Card.get_show_secret_struct())
            cards = self.cards[1:]
            score = self.score - self.cards[0].score
        else:
            cards = self.cards
            score = self.score
        for card in cards:
            show_struct.append(card.get_show_struct())
        for i in range(4):
            for j,_ in enumerate(show_struct):
                for_print.append(show_struct[j][i])
            for_print.append('\n')
        for_print.append(f' Score: {score}') 
        return ''.join(for_print)


class PlayerBox(Box):  

    def __init__(self, player):
        super().__init__(player)


class DealerBox(Box):

    def __init__(self, dealer):
        super().__init__(dealer)


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
        
    def start(self):
        print('\n\n\nGame is started...\n'\
              f'Hello, {self.player_box.user.name}!\n'\
              f'I\'m {self.dealer_box.user.name}, your dealer for today.\n'\
              'Let\'s have some fun!\n\n'
              )
        time.sleep(1)
        while True:
            ans = Dialog.ask('Press \'Enter\' to play the next hand'\
                             ' or exit.', str,
                             answers='[Press \'Enter\' / (e)xit]'
                             )
            if ans.lower() in ('exit', 'e'): break
            elif ans: continue 
              
            while True:
                self.give_card(self.dealer_box)
                self.give_card(self.dealer_box)
                self.give_card(self.player_box)
                self.give_card(self.player_box)
                
                print('Dealers hand:')
                print(self.dealer_box.__str__(True))
                print('Players hand:')
                print(self.player_box)
                time.sleep(100)
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
    dealer = Dealer('Jack', 1000000)
    player = Player('Nick', 50000)

    glogic = GameLogic(dealer, player)
    glogic.start()
