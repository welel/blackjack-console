'''This module implemets blackjack game.
'''
import random



class InvalidCardValueError(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)


class InvalidSuitValueError(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)


class BaseCard(object):

    values = ('A', 'K', 'Q', 'J',
        '10', '9', '8', '7', '6',
        '5', '4', '3', '2'
        )
    suits = ('d', 'c', 'h', 's')
    
    def __init__(self, value, suit):
        if value not in BaseCard.values:
            raise InvalidCardValueError(
                f'expected values is {BaseCard.values}, but yours is {value}'
                )
        self.value = value
        if self.value.isdigit():
            self.score = int(self.value)
        elif self.value == 'A':
            self.score = 11
        else:
            self.score = 10
            
        if suit not in BaseCard.suits:
            raise InvalidSuitValueError(
                f'expected values is {BaseCard.suits}, but yours is {suit}'
                )
        self.suit = suit
        
    
class Card(BaseCard):
    
    def __init__(self, value, suit):
        super().__init__(value, suit) 
        
    def __str__(self):
        return f'[{self.value}{self.suit}]'
        
    def __repr__(self):
        return f'Card({self.value}, {self.suit})'


class CardDeck(BaseCard):

    def __init__(self, shuffled=False):
        deck = []
        for value in BaseCard.values:
            for suit in BaseCard.suits:
                deck.append(Card(value, suit))
        if shuffled:
            random.shuffle(deck)
        self.deck = deck
        
    def __getitem__(self, slice_):
        return self.deck[slice_]
        
    def __str__(self):
        return f'Deck: {list(map(lambda x: str(x), self.deck))}'


class DecksHolder(CardDeck):
    
    def __init__(self, decks_number=1):
        cards = []
        for i in range(decks_number):
            cards.extend(CardDeck())
        random.shuffle(cards)
        self.cards = cards
        
    def __iter__(self):
        i = len(self.cards)
        while True:
            i -= 1
            if i < 0:
                i = len(self.cards)-1
                random.shuffle(self.cards)
            yield self.cards[i] 


class BaseUser(object):
    def __init__(self, name='unknown user', bankroll=0):
        self.name = name
        self.bankroll = bankroll
        

class Player(BaseUser):
    def __init__(self, name='unknown player', bankroll=0):
        super().__init__(name, bankroll)


class Dealer(BaseUser):
    def __init__(self, name='Dealer', bankroll=500000):
        super().__init__(name, bankroll)


class Box(object):   
    def __init__(self, user):
        self.user = user
        self.cards = []


class PlayerBox(Box):   
    def __init__(self, player):
        super().__init__(player)


class DealerBox(Box):
    def __init__(self, dealer):
        super().__init__(dealer)


class TablePlace(object):

    def __init__(self, user=BaseUser()):
        self.user = user
        self.boxes = [Box(self.user)]
  
  
class PlayerTablePlace(TablePlace):

    def __init__(self, player=Player()):
        super().__init__(player)
        self.boxes = [PlayerBox(self.user)]


class DealerTablePlace(TablePlace):

    def __init__(self, dealer=Dealer()):
        super().__init__(dealer)
        self.boxes = [DealerBox(self.user)]


class Table(object):
    
    def __init__(self):
        self.dealer_place = DealerTablePlace()
        self.player_place = PlayerTablePlace()

    def set_dealer(self, dealer):
        self.dealer_place = DealerTablePlace(dealer)
        
    def set_player(self, player):
        self.player_place = (PlayerTablePlace(player))

    def set_decks_holder(self, decks_holder):
        self.decks_holder = decks_holder
        

class Dialog(object):

    def ask(self, user, question: str,
            answers: list, instruction: str,
            user_answer_type):
        print(f'{user.name}, {question}')
        print(f'Answers: {answers}')
        print(instruction)
        return user_answer_type(input())
        
    def say(self, message):
        print(message)
        

 
class Game(object):
    
    def set_table(self, table):
        self.table = table

    def run(self):
        dialog = Dialog()
        player_answer = dialog.ask(player, 'How are you?', ['Good', 'Bad'],
                                   '(G)ood/(B)ad', str
                                   )
        print(player_answer)




if __name__ == '__main__':
    table = Table()
    
    dealer = Dealer('Dealer Jack', 1000000)
    player = Player('Nick', 50000)
    decks_holder = DecksHolder(6)
    
    table.set_dealer(dealer)
    table.set_player(player)
    table.set_decks_holder(decks_holder)
    
    game = Game()
    game.set_table = table
    
    game.run()
    
    
    
        
    
    
    