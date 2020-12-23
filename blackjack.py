class Handler:
    sheet = {
        0: 0,
        1: 1
    }
    
    answer_code = {
        'S': 1, # start
        'L': 0, # leave
    }
    
    def convert(self, answer):
        return self.answer_code[answer]
    
    def get_code(self, answer):
        code = self.convert(answer)
        return self.sheet[code]
        
    


class Player:
    bank = 0
    
    def __init__(self, bank):
        self.bank = bank
        
    def ask_start(self):
        print('Start game or leave? (S\L)\n')
        answer = input()
        return answer
        
    def ask_yes(self):
        print('Yes or no?\n')
        answer = input()
        return answer
        
    def ask_bet(self):
        print('Input bet: ')
        bet = int(input())
        return bet



class Game:
    handler = None
    
    dealer = None
    player = None
    table = None
    
    min_ = 500
    max_ = 10000
    
    def __init__(self, handler, player):
        self.handler = handler
        self.player = player
    
    def close(self):
        print('Do you really wanna close game?\n')
        answer = player.ask_yes()
        if answer == 'Yes':
            # save statements
            print('Thanks for game')
            exit(1)
        else:
            return True
    
    
    def run(self):
        print('Game is started.\n')
        
        while True:
            while True:
                answer = player.ask_start()
                code = handler.get_code(answer)
                if code == 1:
                    break
                self.close()

            while True:
                bet = player.ask_bet()
                if self.min_ > bet or bet > self.max_:
                    print(f'{self.min_} > {bet} > {self.max_}')
                    print('You\'r in wrong limits! Bet right.\n') 
                elif bet > player.bank:
                    print('You\'r out of money! Bet less.\n')
                else:
                    player.bank -= bet
                    break

        print('Game is ended.\n')
        

if __name__ == '__main__':
    handler = Handler()
    player = Player(50000)
    
    game = Game(handler, player)
    game.run()


