"""Classes of: playing card, card deck, deck holder, hand with cards. 

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
        """Generates next card, reshuffle the stack when end reached."""
        i = len(self) - 1
        while True:
            if i < 0:
                i = len(self) - 1
                random.shuffle(self)
            yield self[i] 
            i -= 1


class InvalidHandInitializationError(Exception):
    """Exception for invalid hand of initialization.
    
    The class Hand takes only `Card` type.
    
    """
    
    def __init__(self, message):
        Exception.__init__(self, message)


class Hand(list):
    """Represents a hand with cards of an user.
    
    The class Hand represents a hand that collects dealt cards.
    Each card has a value. A score stores sums of that values.
    
    By default the score is sum of values of hand's cards. But one
    card has multiple value that calculates in favor of a user.
    The card Ace can be 11 or 1. An attribute `score` stores two
    calculated scores of hand (with Ace = 11 and Ace = 1). And actual
    score equals:
           `max(score1, score2) if score1 > 21 else min(score1, score2)`.
    
    Attributes:
        cards (self): Dealt cards.
        score (list): Scores of the hand.

    """
    
    def __init__(self, *args):
        for card in args:
            if not isinstance(card, Card):
                raise InvalidHandInitializationError(
                    f'The class Hand takes only {Card} type '\
                    f'but {type(card)} was given.'
                )
        if args:
            super().__init__(args)
        self.score = [0, 0]
        self._count_score()
        
    def _count_score(self):
        """Counts the score of a hand and updates attribute `score`."""
        score = 0
        for card in self:
            score += card.value
        self.score[0] = score
        for card in self:
            if card.rank == RANKS[0]:
                score -= 10
        self.score[1] = (int(score))
        
    def score_str(self):
        if (self.score[0] != self.score[1]) and\
            (self.score[0] < 21 and self.score[1] < 21):
            return f'{self.score[0]}/{self.score[1]}'
        elif self.score[0] == 21:
            return self.score[0]
        else:
            return str(min(self.score))
            
    def get_score(self):
        if self.score[0] > 21:
            return min(self.score)
        else:
            return self.score[0]
    
    def append(self, card):
        """Adds a card and calls recount score function."""
        super().append(card)
        self._count_score()
    
    def _prepare_print(self):
        """Prepares list of strs for print the hand in the console."""
        show_struct = []
        for_print = []
        if len(self) == 0:
            return 'Empty hand.'
        for card in self:
            show_struct.append(card.get_repr_struct())
        if len(show_struct) == 1:   # condition for dealer hand
            show_struct.append(CARD_BACK_STRUCT)
        for i in range(4):
            for j,_ in enumerate(show_struct):
                for_print.append(show_struct[j][i])
            for_print.append('\n')
        for_print.append(f' Score: {self.score_str()}')
        return for_print
    
    def to_str(self):
        return ''.join(self._prepare_print())
    
    def clear(self):
        """Clears cards from a hand and the score.""" 
        super().clear()
        self.score = [0, 0]    


class PlayerHand(Hand):
    """Player's hand with cards.
    
    """
    
    def __init__(self, *args):
        super().__init__(*args)
    
    
class DealerHand(Hand):
    """Dealer's hand with a hidden card and others cards.
    
    The DealerHand extends Hand and has additional functionality which
    implements dealer's ability to hide his first card on initial deal.
    After player's decisions the hidden card of a dealer opens.
    
    Additional attributes:
        hidden_card (Card): A hidden card of a dealer.
        hide (bool): A flag, tells when show card.
        
    """
    
    def __init__(self, *args):
        super().__init__(*args)
        self.hidden_card = None
        self.hide = True
        
    def clear(self):
        """Clears cards (including hidden) and score of the hand."""
        super().clear()
        self.hidden_card = None
        self.hide = True
        
    def set_hidden_card(self, card):
        self.hidden_card = card
        self.hide = True
        
    def show_hidden_card(self):
        """Appends the hidden card to countable cards."""
        self.append(self.hidden_card)
    
    def append(self, card):
        """Appends a card to dealer's hand.
        
        First appended card always goes like hidden.
        
        """
        if not self.hidden_card:
            self.set_hidden_card(card)
        else:
            super().append(card)
