from turtle import *
import turtle as t
from PIL import Image
import os

# Prepare the resized image once (only if it doesn't exist)
if not os.path.exists('./asset/rocket-ship-40.gif'):
    img = Image.open('./asset/rocket-ship.gif')
    img_resized = img.resize((20, 20), Image.LANCZOS)
    img_resized.save('./asset/rocket-ship-40.gif')

# Register the shape once
t.register_shape('./asset/rocket-ship-40.gif')

class SpaceShipManager(Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.shape('./asset/rocket-ship-40.gif')
        self.penup()
        self.color('darkgreen')
        self.goto(x,y)
        self.x_move = 5
       

    def bounce_x(self):
        self.x_move *= -1
    
    def move(self):
        new_x = self.xcor() + self.x_move
        self.goto(new_x, self.ycor())


    