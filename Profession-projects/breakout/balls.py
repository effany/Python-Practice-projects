from turtle import Turtle

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape('circle')
        self.color('black')
        self.penup()
        self.x_move = 2
        self.y_move = 2
        self.move_speed = 0.1
        self.goto(0,-230)


    def move(self):
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self):
        self.y_move *= -1

    def bounce_x(self):
        self.x_move *= -1

    def reset_position(self):
        self.goto(0, -230)
    
    def increase_speed(self):
        # Increase speed by 10% in both directions
        self.x_move *= 1.1
        self.y_move *= 1.1
