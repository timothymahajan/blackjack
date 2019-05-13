import random, time
from Resources import *

class Gambler():

    def __init__(self):
        self.hands_won = 0
        self.hasAce = 0
        self.hand = []
        self.score = 0
        self.atSplit = 0
        self.splitHand1 = ""
        self.splitHand2 = ""

    def getHandValue(self):
        if self.score < BLACKJACK:
            return [str(val), val]
        elif self.score == BLACKJACK:
            return ['BLACKJACK', BLACKJACK]
        else:
            return ['BUST', BUST]

    def isSplit(self):
        if len(self.hand) == 2 and self.hand[0].getValue() == self.hand[1].getValue():
            return True
        return False

    def resetScore(self):
        self.score = 0

    def startSplit(self, sleep):
        self.resetScore()
        self.splitHand1 = self.hand[0].value
        self.splitHand2 = self.hand[1].value


    def updateHand(self, card, sleep):
        self.hand.append(card)
        if card.isAce():
            self.hasAce += 1
        self.score += card.getValue()
        if self.score > BLACKJACK and self.hasAce > 0:
            self.score -= 10
            self.hasAce -= 1
        time.sleep(sleep)

    def whoAmI(self):
        pass

class Dealer(Gambler):

    def __init__(self):
        Gambler.__init__(self)


class Player(Gambler):

    def __init__(self, amount):
        Gambler.__init__(self)
        self.budget = amount
        self.bet = 0

    # Gets the current budget of a player
    # Return: an integer representing the current budget
    def getBudget(self):
        return self.budget

    # Sets the budget of a player to the given amount
    # Params: amount - the new value of the budget
    def setBudget(self, amount):
        self.budget = amount

    # Gets the current bet of a player
    # Return: an integer representing the current budget
    def getBet(self):
        return self.bet

    # Sets the bet of a player to the given amount
    # Params: amount - the new value of the budget
    def setBet(self, amount):
        self.bet = amount

    def canDouble(self):
        if self.getBudget() >= self.getBet() and len(self.hand) == 2:
            return True
        else:
            return False

    def canSplit(self):
        if self.isSplit() and self.getBudget() >= self.getBet() and len(self.hand) == 2 and self.atSplit == 0:
            return True
        else:
            return False

    def whoAmI(self):
        return "player"
     

class AI(Player):
    def __init__(self, amount, level = EASY):
        Player.__init__(self, amount)
        self.form = 0
        self.level = level
        self.turn = 0
        self.startingBudget = amount

    # Gets the current form of a player
    # Return: an integer representing the current form of the player
    def getForm(self):
        return self.form

    # Sets the form of a player to the given value
    # Params: val - the new form of the player
    def setForm(self, val):
        self.form = val

    # Makes an appropriate bet based on the player's current form and budget
    # Return: an integer representing the portion of the budget to be wagered
    def makeBet(self):
        divisor = 20 - self.form
        # if a player drops below 2/3 their original budget, bet less money
        if self.budget < self.startingBudget * (2/3):
            divisor *= 1.5
        # player can bet a maximum of half their current budget
        if divisor < 2:
            divisor = 2
        return int(self.budget / divisor)

    def makeMove(self, hole = 0):
        #Makes the decision depending op player's level
        #hole - the dealer's upcard, also known as the hole
        # Return: One of: SURRENDER, STAND, HIT, DOUBLE_DOWN, SPLIT
        if self.level == EASY:
            val = self.score
            soft = False
            # Check if the hand contains an ace
            for card in self.hand:
                if card.value[1:] == "a":
                    soft = True
            if not soft:
                if val < 12:
                    return HIT
                else:
                    return STAND
            if soft:
                if val <= 17:
                    return HIT
                else:
                    return STAND
        
        elif self.level == MEDIUM:
            val = self.score
            upval = hole
            soft = False
            # Check if the hand contains an ace
            for card in self.hand:
                if card.value[1:] == "a":
                    soft = True
                    break
            # Check if the hand can be split
            split = self.canSplit()
            # Split Case
            if split and self.turn <= 1:
                if upval <= 7:
                    return SPLIT

            # Standard Move
            if not soft:
                if val < 12:
                    return HIT
                else:
                    return STAND
            if soft:
                if val <= 17:
                    return HIT
                else:
                    return STAND

        elif self.level == HARD:
            val = self.score
            upval = hole
            # Check if the hand contains an ace
            soft = False
            for card in self.hand:
                if card.value[1:] == "a":
                    soft = True
                    break
            # Check if the hand can be split
            split = self.canSplit()
            splitVal = self.hand[0].getValue()
            # Split cases of Basic Strategy
            if split and self.turn <= 1:
                if upval <= 7:
                    if splitVal == 4:
                        if self.turn == 0 and (upval == 5 or upval == 6) and self.canDouble():
                            return DOUBLE_DOWN
                        return HIT
                    if splitVal <= 3 and upval <= 3:
                        if splitVal != 2 and upval != 3:
                            return SPLIT
                        return HIT
                    if splitVal == 6 and upval == 7:
                        return HIT
                    if splitVal == 9 and upval == 7:
                        return STAND
                    return SPLIT
                if upval >= 8:
                    if splitVal >= 8:
                        if splitVal == 9 and upval >= 10:
                            return STAND
                        return SPLIT
                    if splitVal <= 7:
                        if upval == 8 and (splitVal == 3 or splitVal == 7):
                            return HIT
                        if splitVal == 7 and upval == 10 and self.turn == 0:
                            return SURRENDER
                        if splitVal == 7 and upval == 10 and self.turn != 0:
                            return STAND
                        return HIT
            # Hard cases of Basic Strategy
            if not soft:
                if 5 <= val <= 11:
                    if self.turn > 0:
                        return HIT
                    if val == 8 and (upval == 5 or upval == 6) and self.canDouble():
                        return DOUBLE_DOWN
                    if val == 9 and upval <= 6 and self.canDouble():
                        return DOUBLE_DOWN
                    if val == 10 and upval <= 9 and self.canDouble():
                        return DOUBLE_DOWN
                    if val == 11 and self.canDouble():
                        return DOUBLE_DOWN
                if 12 <= val <= 16:
                    if upval >= 7:
                        if self.turn == 0 and val == 16:
                            return SURRENDER
                        return HIT
                    if val == 12 and upval <= 3:
                        return HIT
                    return STAND
                if val >= 17:
                    return STAND
            # Soft cases of Basic Strategy
            if soft:
                if val <= 17:
                    if self.turn == 0 and val == 17 and upval <= 6 and self.canDouble():
                        return DOUBLE_DOWN
                    if self.turn == 0 and 4 <= upval <= 6 and self.canDouble():
                        return DOUBLE_DOWN
                    return HIT
                if val >= 18:
                    if self.turn == 0 and val == 18 and 3 <= upval <= 6 and self.canDouble():
                        return DOUBLE_DOWN
                    if self.turn == 0 and val == 19 and upval == 6 and self.canDouble():
                        return DOUBLE_DOWN
                    if val == 18 and (upval == 9 or upval == 10):
                        return HIT
                    return STAND
            return HIT




        else:
            #an expert
            val = self.score
            upval = hole
            # Check if the hand contains an ace
            soft = False
            for card in self.hand:
                if card.value[1:] == "a":
                    soft = True
                    break
            # Check if the hand can be split
            split = self.canSplit()
            splitVal = self.hand[0].getValue()
            # Split cases of Basic Strategy
            if split and self.turn <= 1:
                if upval <= 7:
                    if splitVal == 4:
                        if self.turn == 0 and (upval == 5 or upval == 6) and self.canDouble():
                            return DOUBLE_DOWN
                        return HIT
                    if splitVal <= 3 and upval <= 3:
                        if splitVal != 2 and upval != 3:
                            return SPLIT
                        return HIT
                    if splitVal == 6 and upval == 7:
                        return HIT
                    if splitVal == 9 and upval == 7:
                        return STAND
                    return SPLIT
                if upval >= 8:
                    if splitVal >= 8:
                        if splitVal == 9 and upval >= 10:
                            return STAND
                        return SPLIT
                    if splitVal <= 7:
                        if upval == 8 and (splitVal == 3 or splitVal == 7):
                            return HIT
                        if splitVal == 7 and upval == 10 and self.turn == 0:
                            return SURRENDER
                        if splitVal == 7 and upval == 10 and self.turn != 0:
                            return STAND
                        return HIT
            # Hard cases of Basic Strategy
            if not soft:
                if 5 <= val <= 11:
                    if self.turn > 0:
                        return HIT
                    if val == 8 and (upval == 5 or upval == 6) and self.canDouble():
                        return DOUBLE_DOWN
                    if val == 9 and upval <= 6 and self.canDouble():
                        return DOUBLE_DOWN
                    if val == 10 and upval <= 9 and self.canDouble():
                        return DOUBLE_DOWN
                    if val == 11 and self.canDouble():
                        return DOUBLE_DOWN
                if 12 <= val <= 16:
                    if upval >= 7:
                        if self.turn == 0 and val == 16:
                            return SURRENDER
                        return HIT
                    if val == 12 and upval <= 3:
                        return HIT
                    return STAND
                if val >= 17:
                    return STAND
            # Soft cases of Basic Strategy
            if soft:
                if val <= 17:
                    if self.turn == 0 and val == 17 and upval <= 6 and self.canDouble():
                        return DOUBLE_DOWN
                    if self.turn == 0 and 4 <= upval <= 6 and self.canDouble():
                        return DOUBLE_DOWN
                    return HIT
                if val >= 18:
                    if self.turn == 0 and val == 18 and 3 <= upval <= 6 and self.canDouble():
                        return DOUBLE_DOWN
                    if self.turn == 0 and val == 19 and upval == 6 and self.canDouble():
                        return DOUBLE_DOWN
                    if val == 18 and (upval == 9 or upval == 10):
                        return HIT
                    return STAND
            return HIT

    def whoAmI(self):
        return "ai"




