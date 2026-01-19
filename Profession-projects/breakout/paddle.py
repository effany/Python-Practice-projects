from turtle import Turtle


class Paddle(Turtle):
    def __init__(self):
        super().__init__()
        self.shape('square')
        self.shapesize(1,10)
        self.penup()
        self.color('grey')
        self.goto(0, -250)

    def left(self):
        current_x = self.xcor()
        new_x = current_x - 60
        if new_x - 100 >= -400:  
            self.goto(new_x, self.ycor())

    def right(self):
        current_x = self.xcor()
        new_x = current_x + 60
        if new_x + 100 <= 400: 
            self.goto(new_x, self.ycor())
    