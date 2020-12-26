"""This module represents classes of game personages. 

"""

class BaseUser():
    """This class serves as a parent for game pesonages.
    
    Attributes:
        name (str): A user name.
        bank (int): Amount of virtual money for stakes.
    
    """
    
    def __init__(self, name='unknown user', bank=0):
        self.name = name
        self.bankroll = bank


class Player(BaseUser):
    """This class represents the player."""
    
    def __init__(self, name='unknown player', bank=0):
        super().__init__(name, bank)


class Dealer(BaseUser):
    """This class represents the dealer."""
    
    def __init__(self, name='Dealer', bank=500000):
        super().__init__(name, bank)
