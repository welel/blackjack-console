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
