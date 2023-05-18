import random
import numpy as np
import argparse

class Player:
    def __init__(self, board, money):
        self.board = board
        self.money = money
        self.in_game = True
        self.win = False
        self.win_methode = ""
        self.ref_board = np.copy(self.board)
    
class Bingo:
    
    def __init__(self, number_of_players = 10, money = 20, entry_fee = 10, rules = ["POZIOM", "PION", "SKOS"], number_of_games = 10):
        self.number_of_players = number_of_players
        self.money = money
        self.entry_fee = entry_fee
        self.rules = rules
        self.number_of_games = number_of_games
        
    players = []
    
    def generate_players(self):
        for i in range(self.number_of_players):
            self.players.append(Player(board=self.generate_board(), money=self.money))
        
    def play_game(self):
        single_winner = False
        self.show_players_money()
        for i in range(self.number_of_games):
            self.play_round(i)
            self.show_players_money()
            
            player_state = 0
            for player in self.players:
                if player.in_game:
                    player_state += 1
            
            if player_state < 2:
                single_winner = True
                break
        
        print("")
        if single_winner:
            print("Gra się zakończyła - mamy jednego zwycięsce")
        else:
            print("Gra się zakończyła - koniec rund")        
    
    def play_round(self, number_of_round):
        win_money = 0
        for player in self.players:
            if player.money > 0 :
                player.money -= self.entry_fee
                win_money += self.entry_fee
                player.in_game = True
        
        win_flag = False
        winners_number = 0
        self.show_players_game_start(win_money=win_money)
        
        print(" ")
        print("Runda " + str(number_of_round) + " BINGO. Numery to: ")
        while(win_flag == False):
            bingo_number = random.randint(1, 75)
            print(str(bingo_number), end=" ")
            i = 0
            for player in self.players:
                if player.in_game == True:
                    if bingo_number in player.board:
                        position = np.where(player.board == bingo_number)
                        player.board[position[0], position[1]] = 0
                    
                        if "POZIOM" in self.rules:
                            if np.any(np.all(player.board == 0, axis=1)): #row
                                win_flag = True
                                player.win = True
                                player.win_methode = "POZIOM"
                                winners_number += 1
                    
                        if "PION" in self.rules: 
                            if np.any(np.all(player.board == 0, axis=0)): # collumn
                                win_flag = True
                                player.win = True
                                player.win_methode = "PION"
                                winners_number += 1
                      
                        if "SKOS" in self.rules:    
                            if np.any(np.all(np.diag(player.board) == 0)): # diag
                                win_flag = True
                                player.win = True
                                player.win_methode = "SKOS"
                                winners_number += 1
            
                            if np.any(np.all(np.diag(np.fliplr(player.board)) == 0)): #diag2
                                win_flag = True
                                player.win = True
                                player.win_methode = "SKOS"
                                winners_number += 1

                        if "PLANSZA" in self.rules:
                            if np.any(np.all(player.board == 0)): # board
                                win_flag = True
                                player.win = True
                                player.win_methode = "PLANSZA"
                                winners_number += 1
        
            for player in self.players:
                if player.win == True:
                    player.money += win_money/winners_number
        print("")
        self.show_players_winners()
        self.players_reset()
        
    def players_reset(self):
        
        for player in self.players:
            player.board = self.generate_board()
            player.ref_board = np.copy(player.board)
            player.win = False
            player.win_methode = ""
            if player.money < self.entry_fee :
                player.in_game = False
            
    def show_players_money(self):
        print("")
        print("Gra się zaczyna")
        i = 0
        for player in self.players:
            if player.in_game:
                print("Gracz " + str(i) + " posiada następujący majątek " + str(player.money))
            else:
               print("Gracz " + str(i) + " stwierdził, że to dobry czas aby przejść się na pocztę")
            i += 1
               
    def show_players_game_start(self, win_money):
        print("")
        i = 0
        for player in self.players:
            if player.in_game:
                print("Gracz " + str(i) + " posiada następujący majątek " + str(player.money))
            i += 1
        print("Gracze grają o następującą pulę pieniędzy: " + str(win_money))
    
    def show_players_winners(self):
        i = 0
        for player in self.players:
            if player.win:
                print("Gracz " + str(i) + " wygrał metodą " + str(player.win_methode) + " z następującą planszą")
                print(player.ref_board)
                print("")
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
        
def parse_list(string):
    output = []
    string = string.upper()

    if "POZIOM" in string:
        output.append("POZIOM")
    
    if "PION" in string:
        output.append("PION")
        
    if "SKOS" in string:
        output.append("SKOS")
        
    if "PLANSZA" in string:
        output.append("PLANSZA")    
        
    return output

def main():
    number_of_players = 10
    money = 100
    entry_fee = 10
    rules = ["POZIOM", "PION", "SKOS"]
    number_of_games = 10
    
    parser = argparse.ArgumentParser("Wprowadź dane do gry")
    parser.add_argument("--players", type=int, help="Liczba graczy biorąca udział w grze", required=False)
    parser.add_argument("--money", type=int, help="Portfel startowy każdego gracza", required=False)
    parser.add_argument("--entry_fee", type=int, help="Wpisowe na każdą z gier", required=False)
    parser.add_argument("--rules", type=parse_list, help="Zasady wygranie możliwe: PION, POZIOM, SKOS, PLANSZA", required=False)
    parser.add_argument("--number_of_games", type=int, help="Maksymalna liczba gier", required=False)
    
    args = parser.parse_args()
    print(args.players)
    print(args.rules)
    
    if args.players:
        number_of_players = args.players
        
    if args.money:
        money = args.money
        
    if args.entry_fee:
        entry_fee = args.entry_fee
    
    if args.rules:
        rules = args.rules
        
    if args.number_of_games:
        number_of_games = args.number_of_games
    
    bingo = Bingo(number_of_players=number_of_players,
                  money= money,
                  entry_fee= entry_fee,
                  rules= rules,
                  number_of_games= number_of_games)

    bingo.generate_players()
    bingo.play_game()

if __name__ == "__main__":
    main()
    