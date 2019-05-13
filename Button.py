import sys
from graphics import *
from Resources import *

class Button:
    def __init__(self, win, center, width, height, size, text, s, color):
        w = width / 2.0
        h = height / 2.0
        x = center.getX()
        y = center.getY()
        self.x_max = x+w
        self.x_min = x-w
        self.y_max = y+h
        self.y_min = y-h
        p1 = Point(self.x_min, self.y_min)
        p2 = Point(self.x_max, self.y_max)
        self.rect = Rectangle(p1,p2)
        self.rect.setFill(color)
        self.rect.draw(win)
        self.text = Text(center, text)
        self.text.setSize(size)
        self.text.draw(win)
        self.update(s)

        
    def clicked(self, p):
        return (self.active and
                self.x_min <= p.getX() <= self.x_max and
                self.y_min <= p.getY() <= self.y_max)

    def update(self, enable = True):
        self.rect.setWidth(1)
        if enable:
            self.text.setFill('black')
            self.active = True
        else:
            self.text.setFill('grey')
            self.active = False

    def alter(self, colorFill, colorText, colorOutline, active):
        self.active = active
        self.rect.setFill(colorFill)
        self.text.setFill(colorText)
        self.rect.setOutline(colorOutline)
        self.active = active







