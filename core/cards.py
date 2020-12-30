"""Classes repesent a playing card, a card deck, a deck holder. 

TODO:
    * Create a hand class, that will contain hand of user and
      caulculate its score.

"""

import random



RANKS = ('A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2')
SUITS = ('♠', '♥', '♦', '♣')
CARD_BACK_STRUCT = [
    ' ____ ',
    '|?  | ',
    '| * | ',
    '|__?| '
]


class InvalidCardRankError(Exception):
    """Exception for invalid rank of Card.
    
    The constant RANKS stores all valid card ranks.
    
    """
    
    def __init__(self, message):
        Exception.__init__(self, message)


class InvalidCardSuitError(Exception):
    """Exception for invalid suit of Card.
    
    The constant SUITS stores all valid card suits.
    
    """
    
    def __init__(self, message):
        Exception.__init__(self, message)


class Card():
    """Class represent single playing card.
    
    The constant RANKS contains all available ranks of a card or face
    in other words. The Blackjack use 52 cards: Ace, King, Queen,
    Jack, 10-2. Each rank has numeric representation by rule of
    The Blackjack. Ace is 11 or 1 (depends on game situation, by
    default is 11); King, Queen, Jack and 10 is 10, 9 is 9 and so 
    on to 2. A card value stores a numeric representation of a card.
    
    Also each card has a suit (all available suits are contained in
    the constant SUITS), but it added more for decoration purpose.
    Any calculations don't use suits.
    
    Attributes:
        rank (str): A rank of a card.
        suit (str): A suit of a card.
        value (int): A value of a card.
    
    """
    
    def __init__(self, rank, suit):
        """A card constructor initializes rank, suit and value of a card.
        
        The value is calculated based on card rank.
        
        Note:
            Raises exceptions if invalid value or suit was given.

        """
        if rank not in RANKS:
            raise InvalidCardRankError(
                'expected rankes is {ranks}, but {rank} was given'.format(
                ranks=RANKS, rank=rank)
                )
        self.rank = rank
        if self.rank.isdigit():
            self.value = int(self.rank)
        elif self.rank == 'A':
            self.value = 11
        else:
            self.value = 10   
        if suit not in SUITS:
            raise InvalidCardSuitError(
                'expected suites is {suits}, but {suit} was given'.format(
                suits=SUITS, suit=suit)
                )
        self.suit = suit
        
    def get_repr_struct(self):
        """Builds a list with the structure of a card for printing.
        
        Examples of painted cards in console:
              ____  ____
             |A  | |7  |
             | ♣ | | ♥ |
             |__A| |__7|
        
        Return:
            show_struct (list): A list that contains structure 
                                for printing a card in the console.
        
        """
        repr_struct = [
            ' ____ ',
            f'|{self.rank}  | ',
            f'| {self.suit} | ',
            f'|__{self.rank}| '
        ]
        return repr_struct
        
    def __repr__(self): 
        return 'Card({rank}, {suit})'.format(
            rank=self.rank, suit=self.suit
            )
        
    def __eq__(self, other): 
        return self.value == other.value

    def __str__(self):
        return '\n'.join(self.get_repr_struct())


class CardDeck(list):
    """A class represents a deck of cards.
    
    A deck is list that stores 52 non-repeating cards.
    
    """
    
    def __init__(self, shuffled=False):
        for rank in RANKS:
            for suit in SUITS:
                self.append(Card(rank, suit))
        if shuffled:
            random.shuffle(self)


class DecksHolder(list):
    """A class represents a multiple shuffled card decks in one stack.
    
    This class serves as an abstraction for real croupier decks holder.
    The holders contain several decks of cards shuffled in one stack.
    Most of the games use 4-8 decks.
    
    """
    
    def __init__(self, decks_number=6):
        for _ in range(decks_number):
            self.extend(CardDeck())
        random.shuffle(self)
        
    def __iter__(self):
        """Generates next card, reshuffle the stack when end reached.
        """
        i = len(self) - 1
        while True:
            if i < 0:
                i = len(self) - 1
                random.shuffle(self)
            yield self[i] 
            i -= 1
