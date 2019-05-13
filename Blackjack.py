from graphics import *
from Game import *
from Player import *
from Resources import *

       
def main():
    win = GraphWin("Blackjack", 800, 808)
   
    player = Player(1000)
    ai = AI(1000, HARD)
    dealer = Dealer()
    Game(win, player, ai, dealer)

    win.close()

if __name__ == "__main__":
    main()