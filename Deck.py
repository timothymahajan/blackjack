import sys, random
from graphics import *
from Resources import *

class Deck:
    """A deck of cards"""
    def __init__(self):
        self.suit = SUITS
        self.face = FACES
        self.deck = [] 
        #put together to desc of cards
        for number_decs in range (2):
            for suit in self.suit:
                for face in self.face:
                    card = suit + face
                    self.deck.append(card)  
        for number_shuffle in range (3):
            self.Shuffle()

    def Shuffle(self):
        """Shuffles the deck"""
        random.shuffle(self.deck)

    def Deal(self):
        """Returns the first card on the top of the deck"""
        card = self.deck.pop()
        return card

class testDeck:
    def __init__(self):
        self.suit = TEST_SUITS
        self.face = TEST_FACES
        self.deck = []
        for number_decs in range (10):
            for suit in self.suit:
                for face in self.face:
                    card = suit + face
                    self.deck.append(card)

    def Shuffle(self):
        """Shuffles the deck"""
        random.shuffle(self.deck)

    def Deal(self):
        """Returns the first card on the top of the deck"""
        card = self.deck.pop()
        return card

class Card(GraphicsObject):
    """Creates a card and places a corresponding imade on the table"""
    def __init__(self, win, value, location, face_up = True):
        self.win = win
        self.location = location
        self.value = value
        self.face_up = face_up
        if face_up:
            file = IMAGE_FILE_LOCATION + str(value) + IMAGE_FILE_EXTENSION
        else:
            file = IMAGE_FILE_BACK_OF_THE_CARD
        self.card = Image(location, file)
        self.drawCard()

    def getValue(self):
        """Checks the rank of the card and returns the corresponding integer value"""
        if self.value[1:] in FACE_CARDS:
            return 10
        elif self.value[1:] == "1" or self.value[1:] == "11":
            return 11
        else:
            return int(self.value[1:])

    def drawCard(self):
        self.card.draw(self.win)
    
    def undrawCard(self):
        """Removes the card"""
        self.card.undraw()

    def flipCard(self):
        if self.face_up:
            file = IMAGE_FILE_BACK_OF_THE_CARD
        else:
            file = IMAGE_FILE_LOCATION + str(self.value) + IMAGE_FILE_EXTENSION
        self.card = Image(self.location, file)

    def isAce(self):
        return (self.value[1:] == "1" or self.value[1:] == "11")

    @staticmethod
    def playerFaceCard(win, value, location):
        if value == "easy":
            file = IMAGE_EASY
        elif value == "medium":
            file = IMAGE_MEDUIM
        elif value == "hard":
            file = IMAGE_HARD
        elif value == "expert":
            file = IMAGE_EXPERT
        elif value == "dealer":
            file = IMAGE_DEALER
        elif value == "player":
            file = IMAGE_PLAYER
        else:
            file = IMAGE_BLANK
        image = Image(location, file)
        image.draw(win)