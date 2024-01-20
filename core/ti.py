"""Terminal Interface for keeping converstion with user.

"""
from .users import Player, Dealer, BaseUser
from .cards import Hand



__all__ = (
    'greet',
    'ask',
    'get_answer',
    'display_bank_info',
    'ask_bet',
    'display_hands',
    'warn',
    'announce_winner',
    'stop_on_click',
    'exit_word',
)

WARNINGS = {
    'overbet': '\nYou don\'t have that much coins.\nBet less.',
    'negative_or_zero_bet': '\nYou can\'t bet zero or less coins.\nBet more.',
}


def greet(dealer, player):
    """Greets user."""
    print(str('\n'*100 + '   $   WELCOME TO   $   '.center(50, '=') + '\n' +
              ' Best Console BlackJack '.center(50, '=') +
              f'\n\tHello, {player.name}!\t\n' +
              f'\tI\'m {dealer.name}, your dealer for today.\n' +
              '\tLet\'s have some fun!\n\n' +
              ''.center(50, '=')
             ).rjust(50, '\n')
    )


def ask(instraction: str, answers: str='', user: BaseUser=None):
    """Asks an user a question.
    
    Args:
        instraction: A question or an instractions for user. 
        answers: A represent of available answers.
        user: A user who is being asked.
    
    """
    if user:
        print(user.name + ',', instraction)
    else:
        print(instraction)
    if answers:
        print('\tAnswers:' + answers)


def get_answer(type_: type, placeholder: str=''):
    """Lets user input an answer on a question.
    
    Args:
        type_: Expected answer type to return. 
        placeholder: A placeholder for input() func.
    
    Returns:
        answer(type_): An answer of user.
    
    """
    while True:
        try:
            answer = type_(input(placeholder))
            if isinstance(answer, str):
                answer = answer.lower()
        except ValueError:
            print(f'Use {type_} type for your answer.')
            continue
        return answer


def display_bank_info(user):
    """Prints state of bank of user."""
    print('\n{name} have {bank} coins.\n'.format(name=user.name, bank=user.bank))


def ask_bet(user):
    """Asks user to input a bet and returns it."""
    print('Make a bet.\n')
    return get_answer(int, placeholder='Bet: ')


def display_hands(*hands: Hand):
    """Prints a state of the hands."""
    print('\n' * 50)
    for hand in hands:
        print('{} hand:'.format(hand.__class__.__name__.replace('Hand', '\'s')))
        print(hand.to_str(), end='\n\n')


def warn(warning: str):
    """Prints warning for user."""
    print(WARNINGS[warning])


def announce_winner(user: BaseUser=None, status: str=''):
    """Prints result of one ended hand."""
    if isinstance(user, Player) and not status:
        print(user.name + ', you won!\n')
    elif isinstance(user, Dealer):
        print('Dealer ' + user.name + ' won!\n')
    elif isinstance(user, type(None))and not status:
        print('Draw!\n')
    if status == 'blackjack':
        print('BlackJack!\n')
    elif status == 'insured':
        print('You insured the hand.\n')


def stop_on_click():
    """Lets user tap Enter to continue the game."""
    input('\nPress \'Enter\' to continue...')


def exit_word(user):    
    """Prints goodbye to the user."""
    print(f'\nThank you for the game, {user.name}!\n')
