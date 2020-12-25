import random



VALUES = ('A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2')
SUITS = ('♠', '♥', '♦', '♣')


class InvalidCardValueError(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)


class InvalidCardSuitError(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)


class Card(object):
    
    def __init__(self, value, suit):
        if value not in VALUES:
            raise InvalidCardValueError(
                f'expected values is {VALUES}, but {value} was given'
                )
        self.value = value
        if self.value.isdigit():
            self.score = int(self.value)
        elif self.value == 'A':
            self.score = 11
        else:
            self.score = 10
            
        if suit not in SUITS:
            raise InvalidCardSuitError(
                f'expected values is {SUITS}, but {suit} was given'
                )
        self.suit = suit
        
    def __str__(self): return f'[{self.value}{self.suit}]' 
    def __repr__(self): return f'Card({self.value}, {self.suit})'

    def get_show_struct(self):
        show_struct = [
            ' ____',
            f'|{self.value}  |',
            f'| {self.suit} |',
            f'|__{self.value}|'
        ]
        return show_struct

    @staticmethod
    def get_show_secret_struct():
        show_struct = [
            ' ____',
            '|?  |',
            '| ? |',
            '|__?|'
        ]
        return show_struct

    def show(self):
        for line in self.get_show_struct():
            print(line)


class CardDeck(Card):

    def __init__(self, shuffled=False):
        deck = []
        for value in VALUES:
            for suit in SUITS:
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


if __name__ == '__main__':
    deck = CardDeck()
    cards = deck[6:10]
    cards_show_struct = []
    for card in cards:
        cards_show_struct.append(card.get_show_struct())
    
    for i in range(4):
        for j,_ in enumerate(cards_show_struct):
            print(cards_show_struct[j][i], end=' ')
        print('\n', end='')