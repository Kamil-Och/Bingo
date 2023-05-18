import random
import numpy as np
import argparse

#example of run command
# python bingo.py --players 20 --money 100 --entry_fee 25 --rules "plansza, pion, skos, poziom" --number_of_games 1000
class Player:
    """
    A class that represents a bingo player
    
    ...
    
    Attributes
    ----------
        board : numpy.array
            bingo board of the player, during the game changes -> the numbers that are choosen became 0
        money : int
            player money
        in_game : bool
            flag that checks whether player is still in the game or is waiting at the post office
        win : bool
            flag that indicates whether the player won the round
        win_methode : str
            method by which player won. Possibilities: PION, POZIOM, SKOS, PLANSZA
        ref_board : numpy.array
            initial board state
        
    Methods
    -------
        NONE
    """
    def __init__(self, board, money):
        """
        Generates all the necessary parameters for the bingo player

        Parameters
        ----------
            board : numpy.array
                player initial board
            money : money
                player initial money
        """
        self.board = board
        self.money = money
        
        self.in_game = True
        self.win = False
        self.win_methode = ""
        self.ref_board = np.copy(self.board) # creating copy of the board
    
class Bingo:
    """
    A class that simulates multiple rounds of bingo game
    
    ...
    
    Attributes
    ----------
        players : List of Player
            all the players that play the game
        number_of_players : int
            number of players that play the game of bingo
        money : int
            initial money of each of the player
        entry_fee : int
            entry fee for each round of the game
        rules : List of string
            set of winning rules. Possibilities: PION, POZIOM, SKOS, PLANSZA
        number_of_games : int
            maximum number of rounds
    Methods
    -------
        generate_players
            generates set of player objects
        play_game
            starts the simulation
        play_round
            starts the simulation of single round of the game
        players_reset
            ready the players for the next round
        show_players_money
            shows all the players and their current money
        show_players_game_start
            shows all the players that play current round, their money and winning prize
        show_players_winners
            shows all the winners of the current round, their board and winning method
        generate_collumn
            generate single board column
        geberate_board
            generate bingo board
    """
    def __init__(self, number_of_players= 10, money= 20, entry_fee= 10, rules= ["POZIOM", "PION", "SKOS"], number_of_games= 10):
        """
        Collecting of game parameters and then generating the players
        
        Parameters
        ----------
            number_of_players : int 
                number of players that system needs to generate
            money : int
                initial money of each of the players
            entry_fee : int
                entry fee for each of the games
            rules : list of string
                set of winning rules. Possibilities: PION, POZIOM, SKOS, PLANSZA
            number_of_games : int 
                number of games
        """
        self.number_of_players = number_of_players
        self.money = money
        self.entry_fee = entry_fee
        self.rules = rules
        self.number_of_games = number_of_games
        self.generate_players()
        
    players = []
    
    def generate_players(self):
        """Generating the required number of players"""
        for i in range(self.number_of_players):
            self.players.append(Player(board= self.generate_board(), 
                                       money= self.money))
        
    def play_game(self):
        """Simulation of the bingo game. It stops when there is single winner or the required number of rounds is played"""
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
        """
        Simulation of the single round. System draw the number and include it in the board of each of the players.
        Next it checks wheather any of the active winning conditions is active. When condition is met it selects the winners.

        Parameters
        ----------
            number_of_round : int
                current number of round
        """
        win_money = 0
        for player in self.players:
            if player.money > 0 :
                player.money -= self.entry_fee
                win_money += self.entry_fee
                player.in_game = True
        
        win_flag = False
        winners_number = 0
        self.show_players_game_start(win_money= win_money)
        
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
        """Reading the players for the next round by reseting the win flags and checking wheather they want to go to the post office"""
        for player in self.players:
            player.board = self.generate_board()
            player.ref_board = np.copy(player.board)
            player.win = False
            player.win_methode = ""
            if player.money < self.entry_fee :
                player.in_game = False
            
    def show_players_money(self):
        """printing the players and their money"""
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
        """
        Printing players for current round, their money and prize money
        
        Parameters
        ----------
            win_money : int
                Prize money
        """
        print("")
        i = 0
        for player in self.players:
            if player.in_game:
                print("Gracz " + str(i) + " posiada następujący majątek " + str(player.money))
            i += 1
        print("Gracze grają o następującą pulę pieniędzy: " + str(win_money))
    
    def show_players_winners(self):
        """Printing winners, their board and win method"""
        i = 0
        for player in self.players:
            if player.win:
                print("Gracz " + str(i) + " wygrał metodą " + str(player.win_methode) + " z następującą planszą")
                print(player.ref_board)
                print("")
            i += 1
                
    def generate_collumn(self, min, max):
        """
        Generating single collum of bingo board, the specific column is dictated by min, max parameters that specify the number range

        Parameters
        ----------
            min : int
            max : int

        Returns
        -------
            numpy.array
        """
        collumn = np.array([random.randint(min, max)])
        while(True):
            number = random.randint(min, max)
            if not number in collumn:
                collumn = np.vstack((collumn, np.array([number])))
                if collumn.size == 5:
                    break
        return collumn

    def generate_board(self):
        """
        Generating bingo board by creating corresponding columns, and placing 0 in the middle of the board

        Returns
        -------
            numpy.array
        """
        board = self.generate_collumn(1,15)
        
        for i in range(4):
            board = np.hstack((board, self.generate_collumn(16+i*15, 30+i*15)))
        
        board[2, 2] = 0
        return board
        
def parse_list(string):
    """
    Parsing the input of args --rules parameter

    Parameters
    ----------
        string : string
            args input

    Returns
    -------
        list of string
    """
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
    parser.add_argument("--players", type= int, help= "Liczba graczy biorąca udział w grze", required= False)
    parser.add_argument("--money", type= int, help= "Portfel startowy każdego gracza", required= False)
    parser.add_argument("--entry_fee", type= int, help= "Wpisowe na każdą z gier", required= False)
    parser.add_argument("--rules", type= parse_list, help= "Zasady wygranie możliwe: PION, POZIOM, SKOS, PLANSZA", required= False)
    parser.add_argument("--number_of_games", type= int, help= "Maksymalna liczba gier", required= False)
    
    args = parser.parse_args()
    
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
    
    bingo = Bingo(number_of_players= number_of_players,
                  money= money,
                  entry_fee= entry_fee,
                  rules= rules,
                  number_of_games= number_of_games)

    bingo.play_game()

if __name__ == "__main__":
    main()
