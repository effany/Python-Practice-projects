from turtle import *
import turtle as t
import os

class Bullet(Turtle):
    def __init__(self, initial_x, initial_y):
        super().__init__()
        self.shape('circle')
        self.shapesize(0.5,0.5)
        self.color('#FF6F6F')
        self.penup()
        self.move_speed = 5
        self.initial_x = initial_x
        self.initial_y = initial_y
        self.goto(self.initial_x, self.initial_y)
        self.has_hit_obstacle = False  # Track if bullet hit an obstacle
        
    def drop(self):
        # Move bullet down one step per frame
        if self.ycor() > -380:
            new_y = self.ycor() - self.move_speed
            self.goto(self.initial_x, new_y)
        else:
            self.hideturtle()
       
            