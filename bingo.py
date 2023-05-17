import random
import numpy as np

class Player:
    def __init__(self, board, money):
        self.board = board
        self.money = money
        self.in_game = False
        self.win = False
        self.win_methode = ""
    
class Bingo:
    
    def __init__(self, number_of_players = 10, money = 100, entry_fee = 10, rules = ["POZIOM", "PION", "SKOS"], number_of_games = 10):
        self.number_of_players = number_of_players
        self.money = money
        self.entry_fee = entry_fee
        self.rules = rules
        self.number_of_games = number_of_games
        

    #each player have money, board, id
    players = []
    
    def generate_players(self):
        for i in range(self.number_of_players):
            self.players.append(Player(board=self.generate_board(), money=self.money))
        
        self.show_players()
        
    
    def play_round(self):
        win_money = 0
        for player in self.players:
            if(player.money > 0):
                player.money -= self.entry_fee
                win_money += self.entry_fee
                player.in_game = True
        
        win_flag = False
        
        while(win_flag == False):
            bingo_number = random.randint(1, 75)
            i = 0
            for player in self.players:
                if bingo_number in player.board:
                    position = np.where(player.board == bingo_number)
                    player.board[position[0], position[1]] = 0
                    
                    if "POZIOM" in self.rules:
                        if np.any(np.all(player.board == 0, axis=1)): #row
                            win_flag = True
                            player.win = True
                            player.win_methode = "POZIOM"
                    
                    if "PION" in self.rules: 
                        if np.any(np.all(player.board == 0, axis=0)): # collumn
                            win_flag = True
                            player.win = True
                            player.win_methode = "PION"
                      
                    if "SKOS" in self.rules:    
                        if np.any(np.all(np.diag(player.board) == 0)): # diag
                            win_flag = True
                            player.win = True
                            player.win_methode = "SKOS"
            
                        if np.any(np.all(np.diag(np.fliplr(player.board)) == 0)): #diag2
                            win_flag = True
                            player.win = True
                            player.win_methode = "SKOS"

                    if "PLANSZA" in self.rules:
                        if np.any(np.all(player.board == 0)): # board
                            win_flag = True
                            player.win = True
                            player.win_methode = "PLANSZA"
            
        self.show_players()
                   
    def show_players(self):
        i = 0
        for player in self.players:
            print("Player nr "+ str(i))
            print("money " + str(player.money))
            print("board")
            print(player.board)
            print("")
            print(player.in_game)
            print(player.win)
            print(player.win_methode)
            i += 1
                
    def generate_collumn(self, min, max):
        b = np.array([random.randint(min, max)])
        while(True):
            number = random.randint(min, max)
            if not number in b:
                b = np.vstack((b, np.array([number])))
                if b.size == 5:
                    break
        return b

    def generate_board(self):
        board = self.generate_collumn(1,15)
        
        for i in range(4):
            board = np.hstack((board, self.generate_collumn(16+i*15, 30+i*15)))
        
        board[2, 2] = 0
        return board
        
    

def main():
    bingo = Bingo()

    #bingo.generate_board()
    bingo.generate_players()
    bingo.play_round()

if __name__ == "__main__":
    main()
    