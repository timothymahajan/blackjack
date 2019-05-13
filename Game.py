import time, random, Colors
from graphics import *
from Deck import *
from Button import *
from Resources import *

class Game():

    def __init__(self, win, player, ai, dealer):

        win.setBackground(COLOR_BLACK)

        self.message_communication = Point(MESSAGE_COMMUNICATIONS_H, MESSAGE_COMMUNICATIONS_V)
        message_op = Point(MESSAGE_COMMUNICATIONS_H, 3 * MESSAGE_COMMUNICATIONS_V)

        self.dealer = dealer
        self.player = player
        self.ai = ai
        self.ai_face = ""

        light_colors = [color for color in Colors.colors if color[0] > 120 and color[1] > 120 and  color[2] > 120]
        time.sleep(SLEEP_4)
        for i in range(20):
            color = random.choice(light_colors)
            self.blinkTitle(win,  MESSAGE_WELCOME, SLEEP_BRIEFLY, color_rgb(color[0], color[1], color[2]), MESSAGE_SIZE_XL)
        self.stopBlinking(win,  MESSAGE_WELCOME, color_rgb(color[0], color[1], color[2]), MESSAGE_SIZE_XL)

        color = random.choice(light_colors)
        message = Text(message_op, "Please pick your AI")
        message.setFace("arial")
        message.setFill(color_rgb(color[0], color[1], color[2]))
        message.setSize(MESSAGE_SIZE_XL)
        message.draw(win)
        time.sleep(SLEEP_4)

        Card.playerFaceCard(win, "easy", Point(140, 350))
        easy = Button(win, Point(140, 440), 80, 40, 12, "Simpleton", True, COLOR_BUTTON)
        time.sleep(SLEEP_4)
        Card.playerFaceCard(win, "medium", Point(300, 350))
        meduim = Button(win, Point(300, 440), 80, 40, 12, "Neophyte", True, COLOR_BUTTON)
        time.sleep(SLEEP_4)
        Card.playerFaceCard(win, "hard", Point(460, 350))
        hard = Button(win, Point(460, 440), 80, 40, 12, "Egghead", True, COLOR_BUTTON)
        time.sleep(SLEEP_4)
        Card.playerFaceCard(win, "expert", Point(620, 350))
        expert = Button(win, Point(620, 440), 80, 40, 12, "Virtuoso", True, COLOR_BUTTON)

        p = win.getMouse()

        #while not (easy.clicked(p) or meduim.clicked(p) or hard.clicked(p) or expert.clicked(p)):
        while True:
            if easy.clicked(p):
                self.ai.level = EASY
                self.ai_face = "easy"
                break
            elif meduim.clicked(p):
                self.ai.level = MEDIUM
                self.ai_face = "medium"
                break
            elif hard.clicked(p):
                self.ai.level = HARD
                self.ai_face = "hard"
                break
            else:
                self.ai.level = EXPERT
                self.ai_face = "expert"
                break
        
        easy.alter(COLOR_BLACK, COLOR_BLACK, COLOR_BLACK, False)
        meduim.alter(COLOR_BLACK, COLOR_BLACK, COLOR_BLACK, False)
        hard.alter(COLOR_BLACK, COLOR_BLACK, COLOR_BLACK, False)
        expert.alter(COLOR_BLACK, COLOR_BLACK, COLOR_BLACK, False)
        message_op.undraw()
        cover_faces = Rectangle(Point(800,800), Point(0,0))
        cover_faces.setFill(COLOR_BLACK)
        cover_faces.draw(win)
        table_dealer = Rectangle(Point(700,300), Point(120,100))
        table_player = Rectangle(Point(700,504), Point(120,304))
        table_IA = Rectangle(Point(700,708), Point(120,508))

        table_dealer.setFill(COLOR_WHITE)
        table_dealer.draw(win)

        table_player.setFill(COLOR_WHITE)
        table_player.draw(win)

        table_IA.setFill(COLOR_WHITE)
        table_IA.draw(win)

        #create a deck of cards anf suffle it
        self.deck = Deck()
        #self.deck = testDeck()

        self.dealer = dealer
        self.player = player
        self.ai = ai

        self.back_up_dealer_score = 0
        self.back_up_bet = 0

        self.message_player = ""
        self.message_ai = ""

        #self.message_communication = Point(MESSAGE_COMMUNICATIONS_H, MESSAGE_COMMUNICATIONS_V)

        # Draw the buttons needed for the game
        #control buttons

        hit_button_split = Button(win, Point(160, 320), 52, 20, 10, "Hit", False, COLOR_BUTTON)
        stand_button_split = Button(win, Point(216, 320), 52, 20, 10, "Stand", False, COLOR_BUTTON)
        double_button_split = Button(win, Point(272, 320), 52, 20, 10, "Double", False, COLOR_BUTTON)
        surrender_button_split = Button(win, Point(332, 320), 60, 20, 10, "Surrender", False, COLOR_BUTTON)
        self.buttons_split = [hit_button_split, stand_button_split, surrender_button_split, double_button_split]
        self.split = Text(Point(520, 320), "")
        self.split_ai = Text(Point(520, 524), "")
        self.updateSplitButtons()
            

        deal_button = Button(win, Point(270, 760), 60, 40, 15, "Deal", True, COLOR_BUTTON)

        hit_button = Button(win, Point(33, 448), 52, 20, 10, "Hit", False, COLOR_BUTTON)
        stand_button = Button(win, Point(89, 448), 52, 20, 10, "Stand", False, COLOR_BUTTON)
        double_button = Button(win, Point(33, 471), 52, 20, 10, "Double", False, COLOR_BUTTON)
        split_button = Button(win, Point(89, 471), 52, 20, 10, "Split", False, COLOR_BUTTON)
        surrender_button = Button(win, Point(60, 494), 60, 20, 10, "Surrender", False, COLOR_BUTTON)

        quit_button = Button(win, Point(539, 760), 60, 40, 15, "Quit", True, COLOR_BUTTON)

        #bet selection buttons
        add1_button = Button(win, Point(498, 490), 50, 20, 10, "+ $1", True, COLOR_BET_BUTTON)
        add10_button = Button(win, Point(552, 490), 50, 20, 10, "+ $10", True, COLOR_BET_BUTTON)
        add100_button = Button(win, Point(606, 490), 50, 20, 10, "+ $100", True, COLOR_BET_BUTTON)
        all_button = Button(win, Point(660, 490), 50, 20, 10, "All In", True, COLOR_BET_BUTTON)
        self.buttons = [deal_button, hit_button, stand_button, quit_button, add1_button, add10_button, add100_button, all_button, surrender_button, double_button, split_button]


        #reserve the spots to display the hand values
        #dealer
        self.dealer_score = Text(Point(SCORE_OFFSET_H, DEALER_LEVEL), "")
        self.dealer_score.setSize(MESSAGE_SIZE_S)
        #player
        self.player_score = Text(Point(SCORE_OFFSET_H, DEALER_LEVEL + PLAYER_OFFSET), "")
        self.player_score.setSize(MESSAGE_SIZE_S)
        #AI
        self.ai_score = Text(Point(SCORE_OFFSET_H, DEALER_LEVEL + 2 * PLAYER_OFFSET), "")
        self.ai_score.setSize(MESSAGE_SIZE_S)
        
        #set a bet for player; initially 0 because player will select the amount himself
        self.budget_bet_display = Text(Point(BANK_LEVEL_H, BANK_LEVEL_V), "Budget: $" + str(self.player.budget) + "    Bet: $0" +  ' ' * (28 - len(str(self.player.budget))))
        self.budget_bet_display.setSize(MESSAGE_SIZE_S)

        #set a bet for ai
        bet = self.ai.makeBet()
        self.ai.setBudget(self.ai.getBudget() - bet)
        self.ai.setBet(bet)
        self.budget_bet_ai_display = Text(Point(BANK_LEVEL_H, BANK_LEVEL_V + PLAYER_OFFSET), "Budget: $" + str(self.ai.getBudget()) + "    Bet: $" +  str(bet) + ' ' * (28 - len(str(self.ai.getBudget()))))
        self.budget_bet_ai_display.setSize(MESSAGE_SIZE_S)
      
        self.postScores(win)
        self.postBankBet(win)

        Card.playerFaceCard(win, "dealer", Point(63, 190))
        Card.playerFaceCard(win, "player", Point(63, 380))
        Card.playerFaceCard(win, self.ai_face, Point(63, 620))

        
        light_colors = [color for color in Colors.colors if color[0] > 120 and color[1] > 120 and  color[2] > 120]
        time.sleep(SLEEP_4)
        for i in range(10):
            color = random.choice(Colors.colors)
            self.blinkTitle(win,  MESSAGE_WELCOME, SLEEP_BRIEFLY, color_rgb(color[0], color[1], color[2]), MESSAGE_SIZE_XL)
        time.sleep(SLEEP_4)
        for i in range(6):
            color = random.choice(light_colors)
            self.blinkTitle(win,  MESSAGE_PLAY_RESPONSIBLY, SLEEP_BRIEFLY, color_rgb(color[0], color[1], color[2]), MESSAGE_SIZE_L)
        time.sleep(SLEEP_4)
        for i in range(12):
            color = random.choice(light_colors)
            self.blinkTitle(win,  MESSAGE_GOOD_LUCK, SLEEP_BRIEFLY, color_rgb(color[0], color[1], color[2]), MESSAGE_SIZE_L)
        time.sleep(SLEEP_4)

        p = win.getMouse()
      
        while not quit_button.clicked(p):

            p = win.getMouse()

            #make a bet
            if add1_button.clicked(p):
                self.bet(win, 1)

            elif add10_button.clicked(p):
                self.bet(win, 10)

            elif add100_button.clicked(p):
                self.bet(win, 100)

            elif all_button.clicked(p):
                self.bet(win, self.player.budget)

            elif deal_button.clicked(p):

                if len(self.deck.deck) <= TIME_TO_SHUFFLE:
                    #start playing only if there is enough cards to finish hand
                    self.cleanUp(win, [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0])
                    self.blink(win, MESSAGE_SHUFFLING, SLEEP_1, COLOR_WHITE)
                    self.deck = Deck()
                self.cleanUp(win, [1, 0, 0, 1, 1, 1 ,1, 1, 0, 0, 0])
                if self.player.bet == 0:
                    self.blink(win, MESSAGE_BET, SLEEP_1, COLOR_WHITE, 4 * SLEEP_4)
                else:
                    #hide scores 
                    self.updateScores(win)
                    #disable all control buttons but quit
                    self.updateButtons([0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0])

                    #deal first six cards - two to each player
                    
                    #deal the first card that goes to the player
                    card = self.dealCard(win, Point(FIRST_CARD + CARD_SPACE  * len(self.player.hand), DEALER_LEVEL + PLAYER_OFFSET))
                    self.player.updateHand(card, SLEEP_4)

                    #deal the first card that goes to the ai
                    card = self.dealCard(win, Point(FIRST_CARD + CARD_SPACE  * len(self.ai.hand), DEALER_LEVEL + 2 * PLAYER_OFFSET))
                    self.ai.updateHand(card, SLEEP_4)

                    #deal the first card that goes to the dealer, place it pip down
                    card = self.dealCard(win, Point(FIRST_CARD + CARD_SPACE * len(self.dealer.hand), DEALER_LEVEL), False)
                    self.dealer.updateHand(card, SLEEP_4)

                    #deal the second card that goes to the player
                    card = self.dealCard(win, Point(FIRST_CARD + CARD_SPACE * len(self.player.hand), DEALER_LEVEL + PLAYER_OFFSET))
                    self.player.updateHand(card, SLEEP_4)

                    #deal the second card that goes to the ai
                    card = self.dealCard(win, Point(FIRST_CARD + CARD_SPACE * len(self.ai.hand), DEALER_LEVEL + 2 * PLAYER_OFFSET))
                    self.ai.updateHand(card, SLEEP_4)

                    #deal the second card that goes to the dealer
                    card = self.dealCard(win, Point(FIRST_CARD + CARD_SPACE * len(self.dealer.hand), DEALER_LEVEL))
                    self.dealer.updateHand(card, SLEEP_4)

                    self.updateScores(win, self.dealer.score - self.dealer.hand[0].getValue(), self.player.score, self.ai.score)

                    if self.dealer.score == BLACKJACK:
                        #the dealer received blackjack and opens his cards
                        self.openCards(win)
                        if self.player.score == BLACKJACK and self.ai.score == BLACKJACK:
                            #both the ai and the player also received blackjacks, push.
                            self.updatePlayer(PUSH)
                            self.updateAI(PUSH)
                            self.blink(win, MESSAGE_BLACKJACK_ALL, SLEEP_1, COLOR_WHITE)
                        elif self.player.score == BLACKJACK and self.ai.score != BLACKJACK:
                            #dealer and player received blackjack, ai did not
                            self.updatePlayer(PUSH)
                            self.updateAI(LOST)
                        elif self.player.score != BLACKJACK and self.ai.score == BLACKJACK:
                            #dealer and ai gor bacljack, player did not
                            self.updatePlayer(LOST)
                            self.updateAI(PUSH)
                        else:
                            #only the dealer had blackjack
                            self.updatePlayer(LOST)
                            self.updateAI(LOST)
                        self.blink(win,  self.message_player + self.message_ai, SLEEP_1, COLOR_WHITE)
                        if self.player.atSplit > 0:
                            self.endgamePlayerSplit(win)
                        elif self.ai.atSplit > 0:
                            self.endgameAISplit(win)
                        else:
                            self.cleanUp(win, [1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0])
                    else:
                        #the dealer did not receive blackjack
                        if self.player.score == BLACKJACK:
                            self.updatePlayer()
                            #ai keeps playing against the dealer, but firts it is checked for a blackjack
                            if self.ai.score == BLACKJACK:
                                #ai received blackjack
                                self.updateAI()
                                self.openCards(win)
                            else:
                                #AI also did not receive a blackjach and will play against the dealer
                                advise = self.playAI(win)
                                if advise ==  SURRENDER:
                                    self.updateAI(SURRENDER)
                                    self.openCards(win)
                                elif advise == DOUBLE_DOWN:
                                    self.doubleDown(win, self.ai)
                                    if self.ai.score > BLACKJACK:
                                        self.updateAI(LOST)
                                        self.openCards(win)
                                    else:
                                        #the dealer accumulates cards
                                        self.openCards(win)
                                        self.playDealer(win)
                                        self.endgame(self.ai)
                                elif advise == STAND:
                                    if self.ai.score > BLACKJACK:
                                        self.updateAI(LOST)
                                        self.openCards(win)
                                    else:
                                        #the dealer accumulates cards
                                        self.openCards(win)
                                        self.playDealer(win)
                                        self.endgame(self.ai)
                                elif advise == SPLIT:
                                    #advised to split
                                    self.ai.startSplit(SLEEP_4)
                                    self.processSplit(win, self.ai)
                                    advise = self.playAI(win)
                                    if advise ==  SURRENDER:
                                        self.updateAI(SURRENDER)
                                        self.openCards(win)
                                    elif advise == DOUBLE_DOWN:
                                        self.doubleDown(win, self.ai)
                                        if self.ai.score > BLACKJACK:
                                            self.updateAI(LOST)
                                            self.openCards(win)
                                        else:
                                            #the dealer accumulates cards
                                            self.openCards(win)
                                            self.playDealer(win)
                                            self.endgame(self.ai)
                                    elif advise == STAND:
                                        if self.ai.score > BLACKJACK:
                                            self.updateAI(LOST)
                                            self.openCards(win)
                                        else:
                                            #the dealer accumulates cards
                                            self.openCards(win)
                                            self.playDealer(win)
                                            self.endgame(self.ai)


                            self.blink(win, self.message_player + self.message_ai, SLEEP_1, COLOR_WHITE)
                            if self.player.atSplit > 0:
                                self.endgamePlayerSplit(win)
                            elif self.ai.atSplit > 0:
                                self.endgameAISplit(win)
                            else:
                                self.cleanUp(win, [1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0])      
                        else:
                            #player did not receive blackjack, the game goes on: player gets his chance to pick a strategy
                            self.updateButtons([0, 1, 1, 1, 0, 0, 0, 0, 1, int(self.player.canDouble()), int(self.player.canSplit())])
            
            elif hit_button.clicked(p):
                #Player chooses to draw more cards
                card = self.dealCard(win, Point(FIRST_CARD + CARD_SPACE * len(self.player.hand), DEALER_LEVEL + PLAYER_OFFSET))
                self.player.updateHand(card, SLEEP_4)          
                #update scores, but the first dealer's card remains hidden
                self.updateScores(win, self.dealer.score - self.dealer.hand[0].getValue(), self.player.score, self.ai.score)
                if self.player.score > BLACKJACK:
                    self.updatePlayer(LOST)
                    self.updateButtons([0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0])
                    if self.ai.score == BLACKJACK:
                        self.updateAI(BLACKJACK)
                        self.openCards(win)
                    else:
                        advise = self.playAI(win)
                        if advise ==  SURRENDER:
                            self.updateAI(SURRENDER)
                            self.openCards(win)
                        elif advise == DOUBLE_DOWN:
                            self.doubleDown(win, self.ai)
                            if self.ai.score > BLACKJACK:
                                self.updateAI(LOST)
                                self.openCards(win)
                            else:
                                self.openCards(win)
                                self.playDealer(win)
                                self.endgame(self.ai)
                        elif advise == STAND:
                            if self.ai.score > BLACKJACK:
                                self.updateAI(LOST)
                                self.openCards(win)
                            else:
                                self.openCards(win)
                                self.playDealer(win)
                                self.endgame(self.ai)
                        elif advise == SPLIT:
                            #advised to split
                            self.ai.startSplit(SLEEP_4)
                            self.processSplit(win, self.ai)
                            advise = self.playAI(win)
                            if advise ==  SURRENDER:
                                self.updateAI(SURRENDER)
                                self.openCards(win)
                            elif advise == DOUBLE_DOWN:
                                self.doubleDown(win, self.ai)
                                if self.ai.score > BLACKJACK:
                                    self.updateAI(LOST)
                                    self.openCards(win)
                                else:
                                    #the dealer accumulates cards
                                    self.openCards(win)
                                    self.playDealer(win)
                                    self.endgame(self.ai)
                            elif advise == STAND:
                                if self.ai.score > BLACKJACK:
                                    self.updateAI(LOST)
                                    self.openCards(win)
                                else:
                                    #the dealer accumulates cards
                                    self.openCards(win)
                                    self.playDealer(win)
                                    self.endgame(self.ai)
                    self.blink(win, self.message_player + self.message_ai, SLEEP_1, COLOR_WHITE)
                    if self.player.atSplit > 0:
                        self.endgamePlayerSplit(win)
                    elif self.ai.atSplit > 0:
                        self.endgameAISplit(win)
                    else:
                        self.cleanUp(win, [1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0])
                elif self.player.score == BLACKJACK:
                    self.updateButtons([0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0])
                    self.standPlayer(win)
                else:
                    #the player is below 21 and can once again draw cards or stand
                    self.updateButtons([0, 1, 1, 1, 0, 0, 0, 0, 1, int(self.player.canDouble()), int(self.player.canSplit())])

            elif hit_button_split.clicked(p):
                card = self.dealCard(win, Point(FIRST_CARD + CARD_SPACE * len(self.player.hand), DEALER_LEVEL + PLAYER_OFFSET))
                self.player.updateHand(card, SLEEP_4)
                self.player_score.undraw()
                self.player_score.setText("Player score: " + str(self.player.score))
                self.player_score.draw(win)
                if self.player.score > BLACKJACK:
                    self.updatePlayer(LOST)
                    self.blink(win, self.message_player, SLEEP_1, COLOR_WHITE)
                    if self.ai.atSplit > 0:
                        self.endgameAISplit(win)
                    else:
                        self.cleanUp(win, [1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0])
                elif self.player.score == BLACKJACK:
                    if self.back_up_dealer_score == BLACKJACK:
                        self.updatePlayer(PUSH)
                    else:
                        self.updatePlayer(WON)
                    self.blink(win, self.message_player, SLEEP_1, COLOR_WHITE)
                    if self.ai.atSplit > 0:
                        self.endgameAISplit(win)
                    else:
                        self.cleanUp(win, [1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0])
                else:
                    pass

            elif stand_button_split.clicked(p):
                if self.player.score > BLACKJACK:
                    self.updatePlayer(LOST)
                    self.blink(win, self.message_player, SLEEP_1, COLOR_WHITE)
                elif self.player.score == BLACKJACK:
                    if self.back_up_dealer_score == BLACKJACK:
                        self.updatePlayer(PUSH)
                    else:
                        self.updatePlayer(WON)
                else:
                    if self.back_up_dealer_score > BLACKJACK:
                        self.updatePlayer(WON)
                    else:
                        if self.back_up_dealer_score > self.player.score:
                            self.updatePlayer(LOST)
                        elif self.back_up_dealer_score == self.player.score:
                            self.updatePlayer(PUSH)
                        else:
                            self.updatePlayer(WON)
                self.blink(win, self.message_player, SLEEP_1, COLOR_WHITE)
                if self.ai.atSplit > 0:
                    self.endgameAISplit(win)
                else:
                    self.cleanUp(win, [1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0])

            elif surrender_button_split.clicked(p):
                self.updatePlayer(SURRENDER)
                self.blink(win, self.message_player, SLEEP_1, COLOR_WHITE)
                if self.ai.atSplit > 0:
                    self.endgameAISplit(win)
                else:
                    self.cleanUp(win, [1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0])

            elif double_button_split.clicked(p):
                self.doubleDown(win, self.player)
                if self.player.score > BLACKJACK:
                    self.updatePlayer(LOST)
                    self.blink(win, self.message_player, SLEEP_1, COLOR_WHITE)
                    if self.ai.atSplit > 0:
                        self.endgameAISplit(win)
                    else:
                        self.cleanUp(win, [1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0])
                elif self.player.score == BLACKJACK:
                    if self.back_up_dealer_score == BLACKJACK:
                        self.updatePlayer(PUSH)
                    else:
                        self.updatePlayer(WON)
                    self.blink(win, self.message_player, SLEEP_1, COLOR_WHITE)
                    if self.ai.atSplit > 0:
                        self.endgameAISplit(win)
                    else:
                        self.cleanUp(win, [1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0])


            elif surrender_button.clicked(p):
                #Player chooses to surrender and forfeit half of his winnings
                self.updatePlayer(SURRENDER)
                self.updateButtons([0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0])
                if self.ai.score == BLACKJACK:
                    self.updateAI(BLACKJACK)
                    self.openCards(win)
                else:
                    #ai accumulates cards
                    advise = self.playAI(win)
                    if advise == SURRENDER:
                        self.updateAI(SURRENDER)
                        self.openCards(win)
                    elif advise == DOUBLE_DOWN:
                            self.doubleDown(win, self.ai)
                            if self.ai.score > BLACKJACK:
                                self.updateAI(LOST)
                                self.openCards(win)
                            else:
                                self.openCards(win)
                                self.playDealer(win)
                                self.endgame(self.ai)
                    elif advise == STAND:
                        if self.ai.score > BLACKJACK:
                            self.updateAI(LOST)
                            self.openCards(win)
                        else:
                            self.openCards(win)
                            self.playDealer(win)
                            self.endgame(self.ai)
                    elif advise == SPLIT:
                        #advised to split
                        self.ai.startSplit(SLEEP_4)
                        self.processSplit(win, self.ai)
                        advise = self.playAI(win)
                        if advise ==  SURRENDER:
                            self.updateAI(SURRENDER)
                            self.openCards(win)
                        elif advise == DOUBLE_DOWN:
                            self.doubleDown(win, self.ai)
                            if self.ai.score > BLACKJACK:
                                self.updateAI(LOST)
                                self.openCards(win)
                            else:
                                #the dealer accumulates cards
                                self.openCards(win)
                                self.playDealer(win)
                                self.endgame(self.ai)
                        elif advise == STAND:
                            if self.ai.score > BLACKJACK:
                                self.updateAI(LOST)
                                self.openCards(win)
                            else:
                                #the dealer accumulates cards
                                self.openCards(win)
                                self.playDealer(win)
                                self.endgame(self.ai)
                self.blink(win, self.message_player + self.message_ai, SLEEP_1, COLOR_WHITE)
                if self.player.atSplit > 0:
                    self.endgamePlayerSplit(win)
                elif self.ai.atSplit > 0:
                    self.endgameAISplit(win)
                else:
                    self.cleanUp(win, [1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0])

            elif double_button.clicked(p):
                #Player chooses to put double down
                self.doubleDown(win, self.player)
                self.standPlayer(win)

            elif stand_button.clicked(p):
            # User chooses not to draw cards, disable all buttons but quit and let AI act
                self.standPlayer(win)

            elif split_button.clicked(p):
            # User chooses to split
                self.player.startSplit(SLEEP_4)
                self.processSplit(win, self.player)

            if self.ai.getBudget() + self.ai.getBet() == 0:
                self.cleanUp(win, [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0])
                self.blink(win, MESSAGE_AI + MESSAGE_OUT_OF_MONEY, SLEEP_1, COLOR_WHITE)
                self.blink(win, MESSAGE_GAME_OVER, SLEEP_1, COLOR_WHITE)
                win.close()
            
            if self.player.getBudget()  + self.player.getBet() == 0:
                self.updateButtons([0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0])
                self.blink(win, MESSAGE_PLAYER + MESSAGE_OUT_OF_MONEY, SLEEP_1, COLOR_WHITE)
                self.blink(win, MESSAGE_GAME_OVER, SLEEP_1, COLOR_WHITE)
                win.close()
    
        win.close()
        
    def allIn(self, win):
        """Allows the player to put down all his money"""
        self.player.bet += self.player.budget
        self.player.budget = 0
        self.updateButtons([1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0])
        self.updateBankBet(win)

    def bet(self, win, bet):
        """Allows the player to put down some amount of money provided they can fund it"""
        if self.player.budget >= bet:
            self.player.setBudget(self.player.budget - bet)
            self.player.setBet(self.player.bet + bet)
            #Check if  there is money in the bank, if there is none, disable bet selection buttons
            if self.player.budget == 0:
                self.updateButtons([1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0])
            self.updateBankBet(win)
        else:
            #nothing will happen if the player does not have enough funds in the bank
            pass

    def blink(self, win, text, sleep, color, duration = SLEEP_LONG):
        "Blinks a message"
        message = Text(self.message_communication, text)
        message.setFace("arial")
        message.setFill(color)
        message.setSize(MESSAGE_SIZE_L)
        for i in range(6):
            time.sleep(sleep)
            if i % 2 == 0:
                message.draw(win)
                if i==4:
                    time.sleep(duration)
            else:
                message.undraw()

    def blinkTitle(self, win, text, sleep, color, size):
        "Blinks a message only once"
        message = Text(self.message_communication, text)
        message.setFace("arial")
        message.setFill(color)
        message.setSize(size)
        message.draw(win)
        time.sleep(sleep)
        message.undraw()

    def stopBlinking(self, win, text, color, size):
        message = Text(self.message_communication, text)
        message.setFace("arial")
        message.setFill(color)
        message.setSize(size)
        message.draw(win)


    def clearBankBet(self):
        self.budget_bet_display.undraw()
        self.budget_bet_ai_display.undraw()

    def clearScores(self):
        self.dealer_score.undraw()
        self.player_score.undraw()
        self.ai_score.undraw()

    def clearTable(self):
        """Clears all the cards on the table"""
        for card in self.dealer.hand:
            card.undrawCard()
        for card in self.player.hand:
            card.undrawCard()
        for card in self.ai.hand:
            card.undrawCard()

    def clearTablePerson(self, person):
        """Remove either player's or ai's cards from the table"""
        time.sleep(SLEEP_4)
        for card in person.hand:
            card.undrawCard()
            time.sleep(SLEEP_4)
        del person.hand[:]
        time.sleep(2 * SLEEP_4)

    def cleanUp(self, win, instructions):
        """Updates buttons, clears cards from the table, posts correct scores, removes cards from players list for the next round, posts current scores, updats bank and bet"""
        self.split.undraw()
        self.split.setText("")
        self.split_ai.undraw()
        self.split_ai.setText("")
        self.updateSplitButtons()
        self.updateActionButtons("show")
        self.clearTable()
        self.dealer.resetScore()
        self.player.resetScore()
        self.ai.resetScore()
        del self.player.hand[:]
        del self.dealer.hand[:]
        del self.ai.hand[:]
        self.player.atSplit = 0
        self.ai.atSplit = 0
        self.player.splitHand1 = ""
        self.player.splitHand2 = ""
        self.ai.splitHand1 = ""
        self.ai.splitHand2 = ""
        self.back_up_dealer_score = 0
        self.back_up_bet = 0
        self.message_player = ""
        self.message_ai = ""
        self.ai.turn = 0
        self.player.hasAce = 0
        self.dealer.hasAce = 0
        self.ai.hasAce = 0
        self.updateScores(win)
        self.updateBankBet(win)
        self.updateButtons(instructions)

    def dealCard(self, win, location, face_up = True):
        """Returns one card from the top of the deck"""
        return Card(win, self.deck.Deal(), location, face_up)
        time.sleep(SLEEP_4)

    def doubleDown(self, win, person):
        person.setBudget(person.getBudget() - person.getBet())
        person.setBet(2 * person.getBet())
        self.updateBankBet(win)
        offset = 1
        if person.whoAmI() == "ai":
            offset = 2
            person.turn += 1
        card = self.dealCard(win, Point(FIRST_CARD + CARD_SPACE * len(person.hand), DEALER_LEVEL + offset * PLAYER_OFFSET))
        person.updateHand(card, SLEEP_4)  
        if person.atSplit < 2:
            self.updateScores(win, self.dealer.score - self.dealer.hand[0].getValue(), self.player.score, self.ai.score)
        else:
            if person.whoAmI() == "player":
                self.player_score.undraw()
                self.player_score.setText("Player score: " + str(self.player.score))
                self.player_score.draw(win)
            else:
                self.ai_score.undraw()
                self.ai_score.setText("AI score: " + str(self.ai.score))
                self.ai_score.draw(win)

    def endgame(self, person):
        if person.whoAmI() == "player":
            action = self.updatePlayer
        else:
            action = self.updateAI
        if person.score > BLACKJACK:
            action(LOST)
        else:
            if self.dealer.score > BLACKJACK:
                action(WON)
            else:
                if person.score > self.dealer.score: 
                    action(WON)
                elif person.score == self.dealer.score:
                    action(PUSH)
                else:
                    action(LOST)

    def endgamePlayerSplit(self, win):
        self.back_up_dealer_score = self.dealer.score
        self.updateActionButtons()
        self.budget_bet_ai_display.undraw()
        self.split.undraw()
        self.split.setText("")
        self.split.draw(win)
        self.ai_score.undraw()
        self.clearTable()
        self.dealer.resetScore()
        self.player.resetScore()
        self.ai.resetScore()
        del self.player.hand[:]
        del self.dealer.hand[:]
        del self.ai.hand[:]
        self.message_player = ""
        self.message_ai = ""
        self.ai.turn = 0
        self.player.hasAce = 0
        self.dealer.hasAce = 0
        self.ai.hasAce = 0
        self.processSplit(win, self.player)
        

    def endgameAISplit(self, win):
        self.back_up_dealer_score = self.dealer.score
        self.updateActionButtons()
        self.budget_bet_display.undraw()
        self.split_ai.undraw()
        self.split_ai.setText("")
        self.split_ai.draw(win)
        self.player_score.undraw()
        self.clearTable()
        self.dealer.resetScore()
        self.player.resetScore()
        self.ai.resetScore()
        del self.player.hand[:]
        del self.ai.hand[:]
        self.message_player = ""
        self.message_ai = ""
        self.player.hasAce = 0
        self.dealer.hasAce = 0
        self.ai.hasAce = 0
        self.processSplit(win, self.ai)
        advise = self.playAI(win)
        if self.ai.score > BLACKJACK:
            self.updateAI(LOST)
        elif self.ai.score == BLACKJACK:
            self.updateAI(WON)
        else:
            if advise ==  SURRENDER:
                self.updateAI(SURRENDER)
            elif advise ==  STAND:
                if self.back_up_dealer_score > BLACKJACK:
                    self.updateAI(WON)
                else:
                    if self.back_up_dealer_score > self.ai.score:
                        self.updateAI(LOST)
                    elif self.back_up_dealer_score == self.ai.score:
                        self.updateAI(PUSH)
                    else:
                        self.updateAI(WON)
            elif advise == DOUBLE_DOWN:
                self.doubleDown(win, self.ai)
                if self.back_up_dealer_score > BLACKJACK:
                    self.updateAI(WON)
                else:
                    if self.back_up_dealer_score > self.ai.score:
                        self.updateAI(LOST)
                    elif self.back_up_dealer_score == self.ai.score:
                        self.updateAI(PUSH)
                    else:
                        self.updateAI(WON)
        self.blink(win, self.message_ai, SLEEP_1, COLOR_WHITE)
        if self.player.atSplit > 0:
            self.endgamePlayerSplit(win)
        self.cleanUp(win, [1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0])


    def openCards(self, win):
        """When the player is done drawing cards, dealer opens his cards"""
        for card in self.dealer.hand:
            card.undrawCard()
        self.dealer.hand[0].flipCard()
        self.dealer.hand[0].drawCard()
        time.sleep(SLEEP_4)
        self.dealer.hand[1].drawCard()
        time.sleep(SLEEP_4)
        self.updateScores(win, self.dealer.score, self.player.score, self.ai.score)

    def playDealer(self, win):
        #dealer hits cards until he has at least 17
        while self.dealer.score < 17 or (self.dealer.score < 17 and self.dealer.hasAce > 0):
            card = self.dealCard(win, Point(FIRST_CARD + CARD_SPACE * len(self.dealer.hand), DEALER_LEVEL))
            self.dealer.updateHand(card, SLEEP_4)
            self.updateScores(win, self.dealer.score, self.player.score, self.ai.score)

    def playAI(self, win):
        #ia furst gets an advise
        advise = self.ai.makeMove(self.dealer.hand[0].getValue())
        self.updateScoresAI(win, self.translate(advise))
        while advise == HIT and self.ai.score < BLACKJACK:
            card = self.dealCard(win, Point(FIRST_CARD + CARD_SPACE * len(self.ai.hand), DEALER_LEVEL + 2 * PLAYER_OFFSET))
            self.ai.turn += 1
            self.ai.updateHand(card, 3 * SLEEP_4)
            self.updateScores(win, self.dealer.score - self.dealer.hand[0].getValue(), self.player.score, self.ai.score)
            time.sleep(4 * SLEEP_4)
            advise = self.ai.makeMove(self.dealer.hand[0].getValue())
            if self.ai.score < BLACKJACK:
                self.updateScoresAI(win, self.translate(advise))
        if self.ai.score >= BLACKJACK:
            advise = STAND
        self.ai_score.undraw()
        self.ai_score.setText("AI score: " + str(self.ai.score))
        self.ai_score.draw(win)
        return advise

    def processSplit(self, win, person):
        person.atSplit += 1
        person.resetScore()
        if person.whoAmI() == "player":
            offset = 1
        else:
            offset = 2
        #clean up and empty player's hand
        self.clearTablePerson(person)
        if person.atSplit == 1:
            message_split = "Split: playing first hand"
            face = person.splitHand1
        else:
            message_split = "Split: playing second hand"
            face = person.splitHand2
            if person.whoAmI() == "player":
                self.player_score.undraw()
                self.player_score.setText("")
                self.player_score.draw(win)
            else:
                self.ai_score.undraw()
                self.ai_score.setText("")
                self.ai_score.draw(win)
            time.sleep(SLEEP_4)
        if person.whoAmI() == "player":
            self.split.undraw()
            self.split.setText(message_split)
            self.split.draw(win)
        else:
            self.split_ai.undraw()
            self.split_ai.setText(message_split)
            self.split_ai.draw(win)
        time.sleep(SLEEP_4)
        if person.atSplit == 1:
            person.setBudget(person.getBudget() - person.getBet())
            self.back_up_bet = person.getBet()
            if person.whoAmI() == "player":
                self.budget_bet_display.undraw()
                self.budget_bet_display.setText("Bank: $" + str(self.player.getBudget()) + "    Bet: $" +  str(self.player.getBet()) + ' ' * (29 - len(str(self.player.getBudget())) - len(str(self.player.getBudget()))))
                self.budget_bet_display.draw(win)
            else:
                self.budget_bet_ai_display.undraw()
                self.budget_bet_ai_display.setText("Bank: $" + str(self.ai.getBudget()) + "    Bet: $" +  str(self.ai.getBet()) + ' ' * (29 - len(str(self.ai.getBudget())) - len(str(self.ai.getBudget()))))
                self.budget_bet_ai_display.draw(win)
            time.sleep(SLEEP_4)
            self.updateScores(win, self.dealer.score - self.dealer.hand[0].getValue(), self.player.score, self.ai.score)
        else:
            person.setBet(self.back_up_bet)
            if person.whoAmI() == "player":
                self.budget_bet_display.undraw()
                self.budget_bet_display.setText("Bank: $" + str(self.player.getBudget()) + "    Bet: $" +  str(self.player.getBet()) + ' ' * (29 - len(str(self.player.getBudget())) - len(str(self.player.getBudget()))))
                self.budget_bet_display.draw(win)
            else:
                self.budget_bet_ai_display.undraw()
                self.budget_bet_ai_display.setText("Bank: $" + str(self.ai.getBudget()) + "    Bet: $" +  str(self.ai.getBet()) + ' ' * (29 - len(str(self.ai.getBudget())) - len(str(self.ai.getBudget()))))
                self.budget_bet_ai_display.draw(win)
            time.sleep(SLEEP_4)
        card = Card(win, face, Point(FIRST_CARD + CARD_SPACE  * len(person.hand), DEALER_LEVEL + offset * PLAYER_OFFSET))
        time.sleep(SLEEP_4)
        person.updateHand(card, SLEEP_4)
        #deal the second card that goes to the person
        card = self.dealCard(win, Point(FIRST_CARD + CARD_SPACE * len(person.hand), DEALER_LEVEL +  offset * PLAYER_OFFSET))
        person.updateHand(card, SLEEP_4)
        if person.whoAmI() == "player":
            self.player_score.undraw()
            self.player_score.setText("Player score: " + str(self.player.score))
            self.player_score.draw(win)
        else:
            self.ai_score.undraw()
            self.ai_score.setText("AI score: " + str(self.ai.score))
            self.ai_score.draw(win)
        time.sleep(SLEEP_4)
        if person.atSplit == 1:
            if person.whoAmI() == "player":
                self.updateButtons([0, 1, 1, 1, 0, 0, 0, 0, 1, person.canDouble(), 0])
            person.setBet(self.back_up_bet)
        else:
            if person.whoAmI() == "player":
                self.updateSplitButtons("show")
                if not self.player.canDouble():
                    self.buttons_split[3].active = False
                       
    def postBankBet(self, win):
        self.budget_bet_display.draw(win)   
        self.budget_bet_ai_display.draw(win)

    def postScores(self, win):
        self.dealer_score.draw(win)
        self.player_score.draw(win)
        self.ai_score.draw(win)

    def standAI(self, win):
        if self.ai.score > BLACKJACK:
            self.updateAI(LOST)
            #dealer opens cards
            self.openCards(win)
            self.playDealer(win)
            self.endgame(self.player)
        else:
            self.openCards(win)
            self.playDealer(win)
            if self.dealer.score > BLACKJACK:
                self.updatePlayer(WON)
                self.updateAI(WON)
            else:
                if self.player.score > self.dealer.score: 
                    self.updatePlayer(WON)
                elif self.player.score == self.dealer.score: 
                    self.updatePlayer(PUSH)
                else:
                    self.updatePlayer(LOST)
                if self.ai.score > self.dealer.score: 
                    self.updateAI(WON)
                elif self.ai.score == self.dealer.score: 
                    self.updateAI(PUSH)
                else:
                    self.updateAI(LOST)
        
    def standPlayer(self, win):
    # User chooses not to draw cards, disable all buttons but quit and let AI act
        self.updateButtons([0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0])
        if self.ai.score == BLACKJACK:
            self.updateAI(BLACKJACK)
            self.openCards(win)
            self.playDealer(win)
            self.endgame(self.player)
        else:
            #ai accumulates cards
            advise = self.playAI(win)
            if advise == SURRENDER:
                self.updateAI(SURRENDER)
                self.openCards(win)
                self.playDealer(win)
                self.endgame(self.player)
            elif advise == DOUBLE_DOWN:
                self.doubleDown(win, self.ai)
                self.standAI(win)
            elif advise == STAND:
                self.standAI(win)
            elif advise == SPLIT:
                #advised to split
                self.ai.startSplit(SLEEP_4)
                self.processSplit(win, self.ai)
                advise = self.playAI(win)
                if advise ==  SURRENDER:
                    self.updateAI(SURRENDER)
                    self.openCards(win)
                elif advise == DOUBLE_DOWN:
                    self.doubleDown(win, self.ai)
                    if self.ai.score > BLACKJACK:
                        self.updateAI(LOST)
                        self.openCards(win)
                    else:
                        #the dealer accumulates cards
                        self.openCards(win)
                        self.playDealer(win)
                        self.endgame(self.ai)
                elif advise == STAND:
                    if self.ai.score > BLACKJACK:
                        self.updateAI(LOST)
                        self.openCards(win)
                    else:
                        #the dealer accumulates cards
                        self.openCards(win)
                        self.playDealer(win)
                        self.endgame(self.ai)
        self.blink(win, self.message_player + self.message_ai, SLEEP_1, COLOR_WHITE)
        if self.player.atSplit > 0:
            self.endgamePlayerSplit(win)
        elif self.ai.atSplit > 0:
            self.endgameAISplit(win)
        else:
            self.cleanUp(win, [1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0])

    def translate(self, word):
        if word == 0:
            return "STAND"
        elif word == 1:
            return "HIT"
        elif word == 2:
            return "DOUBLE DOWN"
        elif word == 3:
            return "SPLIT"
        elif word == 4:
            return "SURRENDER"
        else:
            return "DUNNO..."

    def updateAI(self, outcome = BLACKJACK):
        if outcome == SURRENDER:
            self.ai.setBudget(self.ai.getBudget() + int(self.ai.getBet()/2))
            self.ai.form = 0
            self.message_ai = MESSAGE_AI + MESSAGE_SURRENDER
        elif outcome == WON:
            self.ai.setBudget(self.ai.getBudget() + 2 * self.ai.getBet())
            self.ai.form += 2
            self.message_ai = MESSAGE_AI + MESSAGE_WON
        elif outcome == PUSH:
            self.ai.setBudget(self.ai.getBudget() + self.ai.getBet())
            self.message_ai = MESSAGE_AI + MESSAGE_PUSH
        elif outcome == LOST:
            self.ai.form = 0
            self.message_ai = MESSAGE_AI + MESSAGE_LOST
        else:
            #Blackjack
            self.ai.setBudget(self.ai.getBudget() + int(2.5 * self.ai.getBet()))
            self.ai.form += 2
            self.message_ai = MESSAGE_AI + MESSAGE_BLACKJACK
        if self.ai.atSplit == 1:
            self.ai.setBet(self.back_up_bet)
        else:
            bet = self.ai.makeBet()
            self.ai.setBudget(self.ai.getBudget() - bet)
            self.ai.setBet(bet)

    def updatePlayer(self, outcome = BLACKJACK):
        if outcome == SURRENDER:
            self.player.setBudget(self.player.getBudget() + int(self.player.getBet()/2))
            self.message_player = MESSAGE_PLAYER + MESSAGE_SURRENDER
        elif outcome == WON:
            self.player.setBudget(self.player.getBudget() + 2 * self.player.getBet())
            self.message_player = MESSAGE_PLAYER + MESSAGE_WON
        elif outcome == PUSH:
            self.message_player = MESSAGE_PLAYER + MESSAGE_PUSH
            self.player.setBudget(self.player.getBudget() + self.player.getBet())
        elif outcome == LOST:
            self.message_player = MESSAGE_PLAYER + MESSAGE_LOST
        elif outcome == BLACKJACK:
            #Blackjack
            self.player.setBudget(self.player.getBudget() + int(2.5 * self.player.getBet()))
            self.message_player = MESSAGE_PLAYER + MESSAGE_BLACKJACK
        else:
            pass
        if self.player.atSplit == 1:
            self.player.setBet(self.back_up_bet)
        else:
            self.player.setBet(0)

    def updateBankBet(self, win):
        self.clearBankBet()
        self.budget_bet_display.setText("Bank: $" + str(self.player.getBudget()) + "    Bet: $" +  str(self.player.getBet()) + ' ' * (29 - len(str(self.player.getBudget())) - len(str(self.player.getBudget()))))
        self.budget_bet_ai_display.setText("Bank: $" + str(self.ai.getBudget()) + "    Bet: $" +  str(self.ai.getBet()) + ' ' * (29 - len(str(self.ai.getBudget())) - len(str(self.ai.getBudget()))))
        self.postBankBet(win)
        
    def updateButtons(self, instructions):
        """Enable the buttons that need to be enabled, disable the buttons that need to be disabled"""
        for i in range(len(self.buttons)):
            if instructions[i] == 0:
                self.buttons[i].update(False)
            elif instructions[i] == 1:
                self.buttons[i].update()
            else:
                pass

    def updateActionButtons(self, action = "hide"):
        if action == "hide":
            for i in [1, 2, 8, 9, 10]:
                self.buttons[i].alter(COLOR_BLACK, COLOR_BLACK, COLOR_BLACK, False)
        else:
            for i in [1, 2, 8, 9, 10]:
                self.buttons[i].alter(COLOR_BUTTON, COLOR_BLACK, COLOR_BLACK, True)


    def updateSplitButtons(self, action = "hide"):
        if action == "hide":
            for button in self.buttons_split:
                button.alter(COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, False)
        else:
            self.updateActionButtons()
            for button in self.buttons_split:
                button.alter(COLOR_BUTTON, COLOR_BLACK, COLOR_BLACK, True)


    def updateScores(self, win, dealer_score = "", player_score = "", ai_score = ""):
        self.clearScores()
        if dealer_score == "":
            self.dealer_score.setText("")
        else:
            self.dealer_score.setText("Dealer score: " + str(dealer_score))
        if player_score == "":
            self.player_score.setText("")
        else:
            self.player_score.setText("Player score: " + str(player_score))
        if ai_score == "":
            self.ai_score.setText("")
        else:
            self.ai_score.setText("AI score: " + str(ai_score))
        self.postScores(win)

    def updateScoresAI(self, win, message):
        self.ai_score.setText(message)
        self.ai_score.undraw()
        for i in range (5):
            self.ai_score.draw(win)
            time.sleep(SLEEP_2)
            self.ai_score.undraw()
            time.sleep(SLEEP_2)
        



         