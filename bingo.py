import random
import numpy as np

class Bingo:
    number_of_players = 10
    money = 100
    entry_fee = 10
    rules = ["POZIOM", "PION", "SKOS"]
    number_of_games = 10

    #each player have money, board, id
    players = []

    def populate_row(self, a, b, c):
        while(len(a) < 5):
            number = random.randint(b, c)
            flag = False

            for e in a:
                if e == number:
                    flag = True
                    break
            
            if flag == False:
                a.append(number)

    def generate_board(self):
        b = []
        i = []
        n = []
        g = []
        o = []

        self.populate_row(b, 1, 15)        
        self.populate_row(i, 16, 30)
        self.populate_row(n, 31, 45)
        self.populate_row(g, 46, 60)
        self.populate_row(o, 61, 75)
        
        print(b)
        print(i)
        print(n)
        print(g)
        print(o)
        
        p = np.array[[b[0], i[0], n[0], g[0], o[0]],
                 [b[1], i[1], n[1], g[1], o[1]],
                 [b[2], i[2], 0, g[2], o[2]],
                 [b[3], i[3], n[2], g[3], o[3]],
                 [b[4], i[4], n[3], g[4], o[4]]]

        print(p)
        
    

def main():
    bingo = Bingo()

    bingo.generate_board() 

if __name__ == "__main__":
    main()